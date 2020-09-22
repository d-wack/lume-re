from models.Model_Base import Base
from sqlalchemy import Column, Integer, String, DATETIME, func
from resouces.globals import *


class DeviceDatasource(Base):
    __tablename__ = 'device_datasources'
    # id,deviceId,dataSourceId,dataSourceName,dataSourceDescription,monitoringInstanceNumber,instanceNumber
    device_datasource_id = Column(Integer, primary_key=True)
    deviceId = Column(Integer)
    datasource_id = Column(Integer)
    datasourceName = Column(String(100))
    monitoringInstanceNumber = Column(Integer)
    instanceNumber = Column(Integer)

    created_on = Column(DATETIME(timezone=True), server_default=func.now())
    updated_on = Column(DATETIME(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return "DeviceDatasource(device_datasource_id='%d', deviceId='%d',datasource_id='%d', datasourceName='%s'," \
               "monitoringInstanceNumber='%d', instanceNumber='%d')" % (self.device_datasource_id,
                                                                        self.deviceId,
                                                                        self.datasource_id,
                                                                        self.datasourceName,
                                                                        self.monitoringInstanceNumber,
                                                                        self.instanceNumber)
