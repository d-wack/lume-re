from logicmonitor.lm_request import lm_request
from models.DeviceDatasource import DeviceDatasource
from resouces.globals import *

def getDeviceDatasources(db_controller):
    print("Getting DeviceDatasources")
    lm_filter = '?filter=instanceNumber>0'
    lm_fields = '&fields=id,deviceId,dataSourceId,dataSourceName,dataSourceDescription,monitoringInstanceNumber,instanceNumber'  # LM Filter
    devices = db_controller.get_devices()
    device_datasource_list = []
    for device in devices:
        lm_resourcePath = f'/device/devices/{device.device_id}/devicedatasources'
        lm_response = lm_request(lm_resourcePath=lm_resourcePath, lm_filter=lm_filter,lm_fields=lm_fields)  # Calls LM API Request
        for data in lm_response['items']:
            device_datasource = DeviceDatasource()
            device_datasource.device_datasource_id = int(data['id'])
            device_datasource.deviceId = int(data['deviceId'])
            device_datasource.datasource_id = int(data['dataSourceId'])
            device_datasource.datasourceName = data['dataSourceName']
            device_datasource.monitoringInstanceNumber = int(data['monitoringInstanceNumber'])
            device_datasource.instanceNumber = int(data['instanceNumber'])
            if not db_controller.check_if_row_exists(row=device_datasource):
                device_datasource_list.append(device_datasource)
    if len(device_datasource_list) > 0:
        db_controller.add_many(device_datasource_list)
    else: #If device_datasource_list = 0, that means there are no new devices
        db_controller.update_log(name="GetDevicesDatasources", log_type="Info", code="300",
                   desc="No New DeviceDatasources Found")
        db_controller.session.commit()
