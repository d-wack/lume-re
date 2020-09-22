from models.Model_Base import Base
from sqlalchemy import Column, Integer, String, DATETIME, func
from resouces.globals import *

class Device(Base):
    __tablename__ = 'devices'

    device_id = Column(Integer, primary_key=True)
    device_name = Column(String(100))
    device_ip = Column(String(500))
    created_on = Column(DATETIME(timezone=True), server_default=func.now())
    updated_on = Column(DATETIME(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return "Device(id='%s', name='%s', ip='%s')" % (self.device_id, self.device_name, self.device_ip)

    @staticmethod
    def get_device(session, device_id):
        return session.query(Device).get(device_id=device_id)

    @staticmethod
    def get_all_devices(session):
        return session.query(Device).all()

