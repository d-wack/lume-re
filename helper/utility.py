import requests
import json
import hashlib
import base64
import time
import hmac
import pymysql
from sqlalchemy.orm import sessionmaker
from models.Model_Base import Base
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from models.Device import Device
from models.Log import Log


with open('config.json') as config:
    config = json.load(config)


LM_URI_GETGROUPS = '/device/groups/'
RESE_SAS_GROUP = '1358'
LM_URI_GETCOLLECTORS = '/setting/collectors'
LM_URI_GETDEVICES = '/device/devices'
LM_DATASOURCES = [43, 138, 111, 29549809, 47]
LM_DS_WinPhysicalDrive = '138'
LM_DS_WinVolumeUsage = '111'
LM_DS_Windows_Process_Counts = '29549809'
LM_DS_Memory = '47'
RE_DB = 'mysql+pymysql://dotwack:redtango1@localhost/re'
ERROR_UNKNOWN_DB = 1049


Errors = {
    "DBUnknown": 1049
}

def create_session(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def handle_errors(e):
    if e.orig.args[0] == 1049:
        print(e.orig.args[1])
        exit(1)
    else:
        log_entry(Log(log_type='Error',log_name='SQL', log_code=e.orig.args[0], log_desc=e.orig.args[1]))

def create_db():
    try:
        engine = create_db_engine()
        Base.metadata.create_all(engine)
    except SQLAlchemyError as e:
        handle_errors(e)

def create_db_engine():

    db_url = test_mysql_connection()
    if db_url:
        engine = create_engine(db_url)
        return engine
    else:
        print("Could not create Engine")
        exit(1)


def test_mysql_connection():

    host = config['MySQL']['host']
    user = config['MySQL']['user']
    password = config['MySQL']['password']
    port = config['MySQL']['port']
    db = config['MySQL']['db']
    db_url = f'mysql+pymysql://{user}:{password}@{host}/{db}'

    try:
        connection = pymysql.connect(host, user, password, db)
        connection.close()
    except pymysql.err.OperationalError as e:
        return False
    return db_url







def getDevicesByGroup(filter=''):
    #session = create_session(engine=engine)
    fields = '?fields=systemProperties,customProperties'
    resourcePath = LM_URI_GETGROUPS + RESE_SAS_GROUP + '/devices'
    data = lm_request(resourcePath, filter=filter, fields=fields)
    devices = []
    for items in data['items']:
        device = Device()
        system_properties = items['systemProperties']
        custom_properties = items['customProperties']
        for properties in system_properties:
            if 'system.deviceId' in properties.values():
                device.device_id = properties['value']
            if 'system.ips' in properties.values():
                device.device_ip = properties['value'].split(',')[0]
            if 'system.displayname' in properties.values():
                device.device_name = properties['value']

        if check_if_row_exists(device):
            log_entry(Log(log_type='Warning',log_name='devices', log_code='1',
                        log_desc="'%s' exists in table 'devices" % device.device_id))
            continue
        else:
            devices.append(device)
    if len(devices) > 0:
        load_table(table_name='devices', data=devices)
    else:
        log_entry(Log(log_type='Info',log_name='Devices', log_code='3',
                      log_desc="No Devices Found"))

def check_if_row_exists(device):
    session = create_session(engine=create_db_engine())
    try:
        check = session.query(Device).filter(Device.device_id == device.device_id).count()
        if check > 0:
            return True
        else:
            return False
    except SQLAlchemyError as e:
        if e.orig.args[0] == 1049: #Unknown DB Error
            print(e.orig.args[1])
        else:
            handle_errors(e)
            session.commit()
    finally:
        session.close()

def log_entry(log):
    session = create_session(engine=create_db_engine())
    try:
        session.add(Log(log_type=log.log_type,log_name=log.log_name,log_code=log.log_code,log_desc=log.log_desc))
        session.commit()
    except SQLAlchemyError as e:
        if e.orig.args[0] == 1049: #Unknown DB Error
            print(e.orig.args[1])
        else:
            handle_errors(e)
            session.commit()
    finally:
        session.close()

def load_table(table_name, data):
    session = create_session(engine=create_db_engine())
    try:
        if table_name =='devices':
            session.add_all(data)
            session.add(Log(log_type="Info",log_name='Devices Loaded', log_code='2', log_desc="New Devices Loaded Successfully"))
            session.commit()
    except SQLAlchemyError as e:
        if e.orig.args[0] == 1049: #Unknown DB Error
            print(e.orig.args[1])
        else:
            handle_errors(e)
            session.commit()
    finally:
        session.close()




def getDeviceDatasources(devices):
    fields = '&fields=deviceId,id,dataSourceName,instanceNumber,dataSourceId,dataSourceName'
    filters = '?filter=instanceNumber>0'
    device_datasource_container = []
    for device in devices:
        device_id = device['id']
        resourcePath = f'/device/devices/{device_id}/devicedatasources'
        device_datasources_resp = lm_request(resourcePath, fields=fields, filter=filters)['items']
        device_datasources = [d for d in device_datasources_resp if d['dataSourceId'] in LM_DATASOURCES]
        device_datasource_container += [device_datasources]

    return device_datasource_container


def getDeviceDataSourceInstances(deviceDatasources):
    print(deviceDatasources)


def lm_request(resourcePath, filter='', fields='', size=''):

    AccessId = config["AccessId"]
    AccessKey = config["AccessKey"]
    Company = config["Company"]

    # Request Info
    httpVerb = 'GET'
    data = ''

    # Construct URL
    url = 'https://' + Company + '.logicmonitor.com/santaba/rest' + resourcePath + filter + fields + size

    # Get current time in milliseconds
    epoch = str(int(time.time() * 1000))

    # Concatenate Request details
    requestVars = httpVerb + epoch + data + resourcePath

    # Construct signature
    new_hmac = hmac.new(AccessKey.encode(), msg=requestVars.encode(), digestmod=hashlib.sha256).hexdigest()
    signature = base64.b64encode(new_hmac.encode())

    # Construct headers
    auth = 'LMv1 ' + AccessId + ':' + signature.decode() + ':' + epoch
    headers = {'Content-Type': 'application/json', 'Authorization': auth}

    # Make request
    response = requests.get(url, data=data, headers=headers)

    # Print status and body of response
    # print(response.status_code)

    json_data = json.loads(response.content)
    # pprint.pprint(json_data['data'])
    return json_data['data']



