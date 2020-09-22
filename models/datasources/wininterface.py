from models.Model_Base import Base
from sqlalchemy import Column, Integer, BIGINT, Float, String, DATETIME, TIMESTAMP, func


class WinInterface(Base):
    __tablename__ = 'ds_wininterface'
    # ['HandleCount', 'ProcessesCount', 'ThreadCount', 'WorkingSet']
    seq_id = Column(Integer, primary_key=True, autoincrement=True)
    instance_id = Column(Integer)
    ds_timestamp = Column(BIGINT)
    ds_datetime = Column(DATETIME)
    BytesSentPerSec = Column(Float)
    PacketsOutboundDiscarded = Column(Float)
    PacketsReceivedDiscarded = Column(Float)
    PacketsReceivedNonUnicastPerSec = Column(Float)
    PacketsReceivedUnicastPerSec = Column(Float)
    PacketsSentNonUnicastPerSec = Column(Float)
    PacketsSentUnicastPerSec = Column(Float)
    ReceivedBitsPerSec = Column(Float)
    OutboundBitsPerSec = Column(Float)
    BytesReceivedPerSec = Column(Float)

    def __repr__(self):
        return "WinInterface(instance_id='%s', ds_datetime='%s', ds_timestamp='%s', BytesSentPerSec,='%4f',' " \
               "PacketsOutboundDiscarded,='%4f',' PacketsReceivedDiscarded,='%4f',' " \
               "PacketsReceivedNonUnicastPerSec,='%4f','PacketsSentUnicastPerSec,='%4f',' ReceivedBitsPerSec,='%4f'," \
               "' OutboundBitsPerSec,='%4f',' BytesReceivedPerSec,='%4f')" % (self.instance_id, self.ds_datetime,
                                                                              self.ds_timestamp, self.BytesSentPerSec,
                                                                              self.PacketsOutboundDiscarded,
                                                                              self.PacketsReceivedDiscarded,
                                                                              self.PacketsReceivedNonUnicastPerSec,
                                                                              self.PacketsReceivedUnicastPerSec,
                                                                              self.ReceivedBitsPerSec,
                                                                              self.OutboundBitsPerSec,
                                                                              self.BytesReceivedPerSec)
