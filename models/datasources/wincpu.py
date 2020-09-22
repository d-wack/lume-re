from models.Model_Base import Base
from sqlalchemy import Column, Integer,BIGINT, Float, String, DATETIME, TIMESTAMP, func


class WinCPU(Base):
    __tablename__ = 'ds_wincpu'

    seq_id = Column(Integer, primary_key=True, autoincrement=True)
    instance_id = Column(Integer)
    ds_timestamp = Column(BIGINT)
    ds_datetime = Column(DATETIME)
    ProcessorQueueLength = Column(Float)
    CPUBusyPercent = Column(Float)
    Frequency_Sys100NS = Column(Float)
    PercentProcessorTime = Column(Float)

    def __repr__(self):
        return "WinCPU(instance_id='%s', CPUBusyPercent='%s', ds_timestamp='%s', ProcessorQueueLength='%4f'," \
               "Frequency_Sys100NS='%4f', PercentProcessorTime='%4f', ds_datetime='%s')" % (
                   self.instance_id, self.CPUBusyPercent, self.ds_timestamp , self.CPUBusyPercent, self.Frequency_Sys100NS,
                   self.PercentProcessorTime, self.ds_datetime)
