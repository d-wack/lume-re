#!/usr/bin/python3
from logicmonitor.getdevicedatasources import getDeviceDatasources
from logicmonitor.getdevices import getDevicesByGroup
from logicmonitor.getinstances import getInstances
from logicmonitor.getdevicedata import getDeviceData
from controllers.dbcontroller import DBController
import json


def main():
    db_info = json.load(open("config.json","r"))
    print(db_info)
    db_controller = DBController(db_info=db_info)
    #print(db_controller)
    #db_controller.set_last_captvi app  ured_timestamp()
    #print(db_controller.get_last_captured_timestamp(datasource_id=43,instance_id=9050731))
    #getDevicesByGroup(db_controller=db_controller,lm_group_id='1358')
    #getDeviceDatasources(db_controller=db_controller)
    #getInstances(db_controller=db_controller)
    getDeviceData(db_controller=db_controller)


if __name__ == '__main__':
    main()
