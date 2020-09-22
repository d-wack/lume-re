from logicmonitor.lm_request import lm_request
from models.Instance import Instance

def getInstances(db_controller, deviceId='', deviceDatasourceId=''):
    print("Getting Instances")
    lm_fields = '?fields=id,deviceDataSourceId'
    deviceDataSources = db_controller.get_deviceDataSources() # Queries DB for deviceId and deviceDataSourceId
    instance_list = []
    for deviceDatasource in deviceDataSources:
        deviceId = str(deviceDatasource[1])
        deviceDatasourceId= str(deviceDatasource[0])
        lm_resourcePath = f'/device/devices/{deviceId}/devicedatasources/{deviceDatasourceId}/instances'
        data = lm_request(lm_resourcePath=lm_resourcePath,lm_fields=lm_fields)
        items = data['items']
        for item in items:
            instance = Instance()
            instance.instance_id = item['id']
            instance.device_datasource_id = item['deviceDataSourceId']
            if not db_controller.check_if_row_exists(row=instance):
                instance_list.append(instance)
    if len(instance_list) > 0:
        db_controller.add_many(data=instance_list)
    else:  # If instance_list = 0, that means there are no new instances
        db_controller.update_log(name="GetInstances", log_type="Info", code="300",
                                         desc="No New Instances Found")
        db_controller.session.commit()

