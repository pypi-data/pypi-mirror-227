from sqlalchemy import Column, Integer, String, SmallInteger, BigInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class LoginLog(Base):
    __tablename__ = "LoginLog"
    LogSerial = Column(BigInteger, primary_key=True)
    HeroSerial = Column(BigInteger, nullable=False)
    HeroIdx = Column(Integer, nullable=False)
    HeroOrder = Column(SmallInteger, nullable=False)
    HeroName = Column(String, nullable=False)
    IP = Column(String, nullable=False)
    LoginTime = Column(Integer, nullable=False)
    LogoutTime = Column(Integer, nullable=False)
