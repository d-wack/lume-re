#!/usr/local/bin/python3.8
from logicmonitor.getdevicedatasources import getDeviceDatasources
from logicmonitor.getdevices import getDevicesByGroup
from logicmonitor.getinstances import getInstances
from logicmonitor.getdevicedata import getDeviceData
from controllers.dbcontroller import DBController


def main():
    db_info = {
        "host":"localhost",
        "user":"reseadmin",
        "password":"adm1N0N1!",
        "port":"3306",
        "db":"re"
    }
    db_controller = DBController(db_info=db_info)
    getDevicesByGroup(db_controller=db_controller,lm_group_id='1358')
    getDeviceDatasources(db_controller=db_controller)
    getInstances(db_controller=db_controller)
    getDeviceData(db_controller=db_controller, start='1598912481', end='1600772772')


if __name__ == '__main__':
    main()
