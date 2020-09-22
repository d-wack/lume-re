from models.Model_Base import Base
from sqlalchemy import Column, Integer, BIGINT, Float, String, DATETIME, TIMESTAMP, func


class WinPhysicalDrive(Base):
    __tablename__ = 'ds_winphysycaldrive'
    # ['AvgDiskSecPerRead', 'AvgDiskSecPerWrite', 'CurrentDiskQueueLength', 'DiskReadBytesPerSec',
    # 'DiskReadsPerSec', 'DiskWriteBytesPerSec', 'DiskWritesPerSec', 'Frequency_PerfTime', 'PercentDiskReadTime',
    # 'PercentDiskWriteTime', 'PercentIdleTime', 'SplitIOPercent', 'SplitIOPerSec']
    seq_id = Column(Integer, primary_key=True, autoincrement=True)
    instance_id = Column(Integer)
    ds_timestamp = Column(BIGINT)
    ds_datetime = Column(DATETIME)
    AvgDiskSecPerRead = Column(Float)
    AvgDiskSecPerWrite = Column(Float)
    CurrentDiskQueueLength = Column(Float)
    DiskReadBytesPerSec = Column(Float)
    DiskReadsPerSec = Column(Float)
    Frequency_PerfTime = Column(Float)
    DiskWriteBytesPerSec = Column(Float)
    DiskWritesPerSec = Column(Float)
    PercentDiskReadTime = Column(Float)
    PercentDiskWriteTime = Column(Float)
    PercentIdleTime = Column(Float)
    SplitIOPercent = Column(Float)
    SplitIOPerSec = Column(Float)

    def __repr__(self):
        return "WinPhysicalDrive(instance_id='%s', ds_datetime='%s', ds_timestamp='%s', AvgDiskSecPerRead='%4f'," \
               "  AvgDiskSecPerWrite='%4f', CurrentDiskQueueLength='%4f', DiskReadBytesPerSec='%4f', " \
               "DiskReadsPerSec='%4f', DiskWriteBytesPerSec='%4f', DiskWritesPerSec='%4f', PercentDiskReadTime='%4f'," \
               "PercentDiskWriteTime='%4f')" % (
                   self.instance_id, self.ds_datetime, self.ds_timestamp, self.AvgDiskSecPerRead,
                   self.AvgDiskSecPerWrite,
                   self.CurrentDiskQueueLength, self.DiskReadBytesPerSec, self.DiskReadsPerSec,
                   self.DiskWriteBytesPerSec,
                   self.DiskWritesPerSec, self.PercentDiskReadTime, self.PercentDiskWriteTime)
