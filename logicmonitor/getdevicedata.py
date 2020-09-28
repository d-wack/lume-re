from logicmonitor.lm_request_for_data import lm_request_for_data
from logicmonitor.datasources.wincpudata import processWinCPU
from logicmonitor.datasources.winphysicaldrive import processWinPhysicalDrive
from logicmonitor.datasources.winvolumeusage import processWinVolumeUsage
from logicmonitor.datasources.winmemory import processWinMemory
from logicmonitor.datasources.winprocess import processWinProcess
from logicmonitor.datasources.wininterface import processWinInterface
from datetime import datetime, timedelta
from calendar import timegm
from time import strptime

def get_start_date(days=180):
    m_today = datetime.now()
    target_date = m_today - timedelta(days=days)
    return str(timegm(strptime(str(target_date), "%Y-%m-%d %H:%M:%S.%f")))

def get_end_date():
    return str(timegm(strptime(str(datetime.now()-timedelta(minutes=5)), "%Y-%m-%d %H:%M:%S.%f")))

def getDeviceData(db_controller):

    configured_datasources = db_controller.get_configured_ds()

    for datasource in configured_datasources:
        data = None
        nextPageParams = None
        print(datasource)
        lastCapturedTime = db_controller.get_last_captured_timestamp(datasource_id=datasource[3], instance_id=datasource[2])
        print(lastCapturedTime)
        if lastCapturedTime is not None:
            start = str(int(lastCapturedTime/1000))
        else:
           start = get_start_date()
        end = get_end_date()

        lm_resourcePath = f'/device/devices/{datasource[0]}/devicedatasources/{datasource[1]}/instances/{datasource[2]}/data'
        lm_filter = f'?start={start}&end={end}'

        #print("Instance:" + str(datasource[0]))
        print("---------------------------------->Initial: " + lm_filter)
        while nextPageParams != '':
            #print(lm_resourcePath)
            print("nextParamFitler: " + lm_filter)
            print("nextParam: " + str(nextPageParams))
            data = lm_request_for_data(lm_resourcePath=lm_resourcePath, lm_filter=lm_filter)
            nextPageParams = data['nextPageParams']
            if data['data']['dataSourceName'] == 'WinCPU':
                processWinCPU(db_controller=db_controller, dataPoints=zip(data['data']['time'], data['data']['values']),
                              instance_id=datasource[2])
            elif data['data']['dataSourceName'] == 'WinPhysicalDrive-':
                processWinPhysicalDrive(db_controller=db_controller,
                                        dataPoints=zip(data['data']['time'], data['data']['values']), instance_id=datasource[2])
            elif data['data']['dataSourceName'] == 'WinVolumeUsage-':
                processWinVolumeUsage(db_controller=db_controller,
                                      dataPoints=zip(data['data']['time'], data['data']['values']), instance_id=datasource[2])
            elif data['data']['dataSourceName'] == 'WinOS':
                processWinMemory(db_controller=db_controller, dataPoints=zip(data['data']['time'], data['data']['values']),
                                 instance_id=datasource[2])
            elif data['data']['dataSourceName'] == 'Windows_Process_Counts':
                processWinProcess(db_controller=db_controller, dataPoints=zip(data['data']['time'], data['data']['values']),
                                  instance_id=datasource[2])
            elif data['data']['dataSourceName'] == 'WinIf-':
                processWinInterface(db_controller=db_controller,
                                    dataPoints=zip(data['data']['time'], data['data']['values']), instance_id=datasource[2])
            else:
                db_controller.update_log(name="Datasource Not Configured", log_type="Warning", code="200",
                                         desc="Please Configure the Datasource in order to save to database")
                db_controller.session.commit()
                break
            if nextPageParams != '':
                lm_filter = '?' + nextPageParams
