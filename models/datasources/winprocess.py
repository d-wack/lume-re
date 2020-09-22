from models.Model_Base import Base
from sqlalchemy import Column, Integer, BIGINT, Float, String, DATETIME, TIMESTAMP, func


class WinProcess(Base):
    __tablename__ = 'ds_winprocess'
    # ['HandleCount', 'ProcessesCount', 'ThreadCount', 'WorkingSet']
    seq_id = Column(Integer, primary_key=True, autoincrement=True)
    instance_id = Column(Integer)
    ds_timestamp = Column(BIGINT)
    ds_datetime = Column(DATETIME)
    HandleCount = Column(Float)
    ProcessesCount = Column(Float)
    ThreadCount = Column(Float)
    WorkingSet = Column(Float)

    def __repr__(self):
        return "WinVolumeUsage(instance_id='%s', ds_datetime='%s', ds_timestamp='%s', HandleCount='%4f'," \
               "ThreadCount='%4f', ProcessesCount='%4f', WorkingSet='%4f',)" % (
                   self.instance_id, self.ds_datetime, self.ds_timestamp, self.HandleCount, self.ThreadCount,
                   self.ProcessesCount, self.WorkingSet)
