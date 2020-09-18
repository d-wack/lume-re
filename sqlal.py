import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('mysql+pymysql://dotwack:redtango1@localhost/re')
Session = sessionmaker(bind=engine)


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=50))

    def __repr__(self):
        return "<User(name='%s')>" % (self.name)


Base.metadata.create_all(engine)


session = Session()
ed_user = Users(name='ed')
session.add(ed_user)
our_user = session.query(Users).filter_by(name='ed').first()
print(ed_user is our_user)

print(session.query(Users).all())

session.add_all([
    Users(name='Brandon'),
    Users(name="Israa"),
    Users(name="Ian")])


print(session.query(Users).all())
session.commit()
