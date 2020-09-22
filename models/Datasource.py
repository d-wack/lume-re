from models.Model_Base import Base
from sqlalchemy import Column, Integer, String, DATETIME, func
from resouces.globals import *

class Datasource(Base):
    __tablename__ = 'datasources'

    datasource_id = Column(String(25), primary_key=True)
    datasource_name = Column(String(100))
    created_on = Column(DATETIME(timezone=True), server_default=func.now())
    updated_on = Column(DATETIME(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return "Datasource(id='%s', name='%s')" % (self.datasource_id, self.datasource_name)

