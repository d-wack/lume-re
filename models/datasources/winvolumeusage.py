from models.Model_Base import Base
from sqlalchemy import Column, Integer, BIGINT, Float, String, DATETIME, TIMESTAMP, func


class WinVolumeUsage(Base):
    __tablename__ = 'ds_winvolumeusage'
    seq_id = Column(Integer, primary_key=True, autoincrement=True)
    instance_id = Column(Integer)
    ds_timestamp = Column(BIGINT)
    ds_datetime = Column(DATETIME)
    Capacity = Column(Float)
    FreeSpace = Column(Float)
    PercentUsed = Column(Float)

    def __repr__(self):
        return "WinVolumeUsage(instance_id='%s', ds_datetime='%s', ds_timestamp='%s'," \
               "Capacity='%4f', FreeSpace='%4f', PercentUsed='%4f')" % (
                   self.instance_id, self.ds_datetime, self.ds_timestamp, self.Capacity, self.FreeSpace,
                   self.PercentUsed)
