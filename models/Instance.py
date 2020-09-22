from models.Model_Base import Base
from sqlalchemy import Column, Integer, String, DATETIME, func

class Instance(Base):
    __tablename__ = 'instances'

    instance_id = Column(Integer, primary_key=True)
    device_datasource_id = Column(Integer)
    created_on = Column(DATETIME(timezone=True), server_default=func.now())
    updated_on = Column(DATETIME(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return "Instance(instance_id='%d', device_datasource_id='%d')" % (self.instance_id,self.device_datasource_id)