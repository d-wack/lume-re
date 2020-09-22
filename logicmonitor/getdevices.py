from logicmonitor.lm_request import lm_request
from models.Device import Device


def getDevicesByGroup(db_controller, lm_group_id, lm_filter=''):
    '''GetDevicesByGroup pulls all devices in a specific group.  Devices must be located within the group and not
    nested in another group.'''
    print("Getting Devices")
    lm_resourcePath = f'/device/groups/{lm_group_id}/devices' #LM API URI
    lm_fields = '?fields=systemProperties,customProperties' #LM Filter
    data = lm_request(lm_resourcePath, lm_filter=lm_filter, lm_fields=lm_fields) #Calls LM API Request
    devices = []
    for items in data['items']:
        device = Device()
        system_properties = items['systemProperties'] #Pulling data from SystemProperties
        for properties in system_properties:
            if 'system.deviceId' in properties.values():
                device.device_id = properties['value'][0:24]
            if 'system.ips' in properties.values():
                device.device_ip = properties['value'][0:499]
            if 'system.displayname' in properties.values():
                device.device_name = properties['value'][0:99]
        if not db_controller.check_if_row_exists(row=device):
            devices.append(device)
    if len(devices) > 0:
        db_controller.add_many(data=devices)
    else: #If devices = 0, that means there are no new devices
        db_controller.update_log(name="GetDevices", log_type="Info", code="300",
                   desc="No New Devices Found")
        db_controller.session.commit()