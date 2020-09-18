from models.Model_Base import Base
from sqlalchemy import Column, Integer, String, DATETIME, func
class Device(Base):
    __tablename__ = 'devices'

    device_id = Column(String(25), primary_key=True)
    device_name = Column(String(50))
    device_ip = Column(String(15))
    created_on = Column(DATETIME(timezone=True), server_default=func.now())
    updated_on = Column(DATETIME(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return "Device(id='%s', name='%s', ip='%s')" % (self.device_id, self.device_name, self.device_ip)