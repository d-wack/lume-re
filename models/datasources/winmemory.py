from models.Model_Base import Base
from sqlalchemy import Column, Integer, BIGINT, Float, String, DATETIME, TIMESTAMP, func


class WinMemory(Base):
    __tablename__ = 'ds_winmemory'

    seq_id = Column(Integer, primary_key=True, autoincrement=True)
    instance_id = Column(Integer)
    ds_timestamp = Column(BIGINT)
    ds_datetime = Column(DATETIME)
    FreePhysicalMemory = Column(Float)
    FreeSpaceInPagingFiles = Column(Float)
    NumberOfProcesses = Column(Float)
    SizeStoredInPagingFiles = Column(Float)
    TotalVisibleMemorySize = Column(Float)
    MemoryUtilizationPercent = Column(Float)
    PercentVirtualMemoryInUse = Column(Float)
    FreeVirtualMemory = Column(Float)
    TotalVirtualMemorySize = Column(Float)

    def __repr__(self):
        return "WinVolumeUsage(instance_id='%s', ds_datetime='%s', ds_timestamp='%s', " \
               "FreePhysicalMemory,='%4f',' FreeSpaceInPagingFiles,='%4f',' NumberOfProcesses,='%4f'," \
               "' SizeStoredInPagingFiles,='%4f','TotalVisibleMemorySize,='%4f',' MemoryUtilizationPercent,='%4f'," \
               "' PercentVirtualMemoryInUse,='%4f',' FreeVirtualMemory,='%4f','TotalVirtualMemorySize,='%4f')" % (
            self.instance_id, self.ds_datetime, self.ds_timestamp, self.FreePhysicalMemory, self.FreeSpaceInPagingFiles,
        self.NumberOfProcesses, self.SizeStoredInPagingFiles, self.TotalVisibleMemorySize, self.MemoryUtilizationPercent,
        self.PercentVirtualMemoryInUse, self.FreeVirtualMemory, self.TotalVirtualMemorySize)
