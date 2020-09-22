import pymysql
from sqlalchemy import MetaData, Table
from sqlalchemy.engine import reflection
from sqlalchemy.orm.exc import NoResultFound, StaleDataError
from sqlalchemy.exc import IntegrityError
from models.Log import Log
from sqlalchemy.orm import sessionmaker
from models.Model_Base import Base
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from models.Device import Device
from models.DeviceDatasource import DeviceDatasource
from models.Instance import Instance
from models.datasources.wincpu import WinCPU
from models.datasources.winphysicaldrive import WinPhysicalDrive


class DBController:

    def __init__(self, db_info):

        self.db_host = db_info['host']
        self.db_user = db_info['user']
        self.db_passwd = db_info['password']
        self.db_name = db_info['db']
        self.db_port = db_info['port']
        self.db_url = self.test_mysql_connection()
        self.db_engine = None
        self.db = None
        self.session = None
        self.create_db_engine()
        self.metadata = MetaData(bind=self.db_engine)
        self.configured_datasources = Table('configured_datasources', self.metadata, autoload=True)

    def __del__(self):
        self.session.close()

    def create_db(self):
        try:
            Base.metadata.create_all(self.db_engine)
        except SQLAlchemyError as e:
            print(e)

    def test_mysql_connection(self):

        host = self.db_host
        user = self.db_user
        password = self.db_passwd
        port = self.db_port
        db = self.db_name
        db_url = f'mysql+pymysql://{user}:{password}@{host}/{db}'

        try:
            connection = pymysql.connect(host, user, password, db)
            connection.close()
            return db_url
        except pymysql.err.OperationalError as e:
            return None

    def create_session(self):
        if self.db_engine is not None:
            Session = sessionmaker(bind=self.db_engine)
            self.session = Session()
        else:
            self.session = None

    def create_db_engine(self):
        if self.db_url is not None:
            self.db_engine = create_engine(self.db_url)
            self.create_db()
            self.create_session()
        else:
            return None

    def update_log(self, name, log_type, code, desc):
        self.session.add(Log(log_name=name, log_type=log_type, log_code=code,
                             log_desc=desc))

    def add_single(self, data):
        try:
            self.session.add(data)
            self.update_log(name="Insert", log_type="Info", code="100", desc="Single Row Added")
            self.session.commit()
        except IntegrityError as error:
            self.session.rollback()
            self.update_log(name="IntegrityError", log_type="Error", code=error.orig.args[0],
                            desc=error.orig.args[1])
            self.session.commit()

    def add_many(self, data):
        try:
            self.session.bulk_save_objects(data)
            self.update_log(name="Insert", log_type="Info", code="101",
                            desc="Added %s %s" % (len(data), data[0].__class__.__name__))
            self.session.commit()
        except IntegrityError as error:
            self.session.rollback()
            self.update_log(name="IntegrityError", log_type="Error", code=error.orig.args[0],
                            desc=error.orig.args[1])
            self.session.commit()

    def update_single(self, data):
        try:
            device = self.session.query(Device).filter_by(device_id=data['device_id']).one()
            if data['column'] == 'device_name':
                device.device_name = data['update']
            elif data['column'] == 'device_ip':
                device.device_ip = data['update']
            else:
                pass
            self.session.dirty
            self.update_log(name="Update", log_type="Info", code="103",
                            desc="Single Row Updated")
            self.session.commit()
        except NoResultFound as error:
            self.session.rollback()
            self.update_log(name="No Results Found", log_type="Warning", code="200",
                            desc="No Results Found for this Query")
            self.session.commit()

    def update_many(self, data):
        try:
            self.session.bulk_update_mappings(Device, data)
            self.session.dirty
            self.update_log(name="Update", log_type="Info", code="101",
                            desc="Updated '%s' devices" % len(data))
            self.session.commit()
        except StaleDataError as error:
            self.session.rollback()
            self.update_log(name="Stale Data", log_type="Error", code="220",
                            desc="Check Update Statement")
            self.session.commit()

    def check_if_row_exists(self, row):
        try:
            if isinstance(row, Device):
                check = self.session.query(Device).filter(Device.device_id == row.device_id).count()
            elif isinstance(row, DeviceDatasource):
                check = self.session.query(DeviceDatasource).filter(
                    DeviceDatasource.device_datasource_id == row.device_datasource_id).count()
            elif isinstance(row, Instance):
                check = self.session.query(Instance).filter(Instance.instance_id == row.instance_id).count()
            if check > 0:
                return True
            else:
                return False
        except SQLAlchemyError as e:
            print(e)

    def get_devices(self):
        return self.session.query(Device).all()

    def get_deviceDataSources(self, dataSourceId=''):
        if dataSourceId == '':
            return self.session.query(DeviceDatasource.device_datasource_id, DeviceDatasource.deviceId).all()
        else:
            return self.session.query(DeviceDatasource.device_datasource_id, DeviceDatasource.deviceId).filter(
                DeviceDatasource.datasource_id == dataSourceId).all()

    def get_deviceInstances(self, deviceDataSourceId=''):
        if deviceDataSourceId == '':
            return self.session.query(Instance).all()
        else:
            return self.session.query(Instance).filter(Instance.device_datasource_id == deviceDataSourceId).all()

    def get_configured_ds(self):
        return self.session.query(self.configured_datasources).all()


