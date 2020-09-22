from logicmonitor.lm_request_for_data import lm_request_for_data
from logicmonitor.datasources.wincpudata import processWinCPU
from logicmonitor.datasources.winphysicaldrive import processWinPhysicalDrive
from logicmonitor.datasources.winvolumeusage import processWinVolumeUsage
from logicmonitor.datasources.winmemory import processWinMemory
from logicmonitor.datasources.winprocess import processWinProcess
from logicmonitor.datasources.wininterface import processWinInterface


def getDeviceData(db_controller, start='', end=''):

    
    configured_datasources = db_controller.get_configured_ds()
    ds_count = len(configured_datasources)
    for datasource in configured_datasources:
        nextPageParams = None
        lm_resourcePath = f'/device/devices/{datasource[0]}/devicedatasources/{datasource[1]}/instances/{datasource[2]}/data'
        #lm_filter = f'?start=1598912481&end=1600610423'
        lm_filter = f'?start={start}&end={end}'

        #print("Instance:" + str(datasource[0]))
        print("--------> Instances: " + str(ds_count))
        ds_count = ds_count - 1

        while nextPageParams != '':
            #print("Instances left: " + str(ds_count))
            #ds_count = ds_count - 1
            #print(lm_resourcePath)
            #print(lm_filter)
            data = lm_request_for_data(lm_resourcePath=lm_resourcePath, lm_filter=lm_filter)
            print("Status: " + str(data['status']))
            if data == None:
                exit(1)
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
