from models.Model_Base import Base
from sqlalchemy import Column, Integer, String, DATETIME, func
from resouces.globals import *

class Log(Base):
    __tablename__ = 'logs'

    seq_id = Column(Integer, primary_key=True, autoincrement=True)
    log_name = Column(String(50))
    log_type = Column(String(50))
    log_code = Column(String(50))
    log_desc = Column(String(200))
    created_on = Column(DATETIME(timezone=True), server_default=func.now())

    def __repr__(self):
        return "Log(seq_id='%s', log_type='%s', log_name='%s', log_code='%s', log_desc='%s')" % (
        self.seq_id, self.log_type, self.log_name, self.log_code, self.log_desc)