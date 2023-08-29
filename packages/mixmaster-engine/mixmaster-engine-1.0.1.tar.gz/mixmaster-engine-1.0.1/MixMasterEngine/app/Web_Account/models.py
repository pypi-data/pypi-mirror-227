from sqlalchemy import Column, Integer, String, Enum, DateTime, SmallInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class GameTail(Base):
    __tablename__ = "GameTail"
    SubType = Column(Enum('TNULL', 'HENCH', 'ITEM'), default='ITEM')
    GiftPlayerID = Column(String, default="")
    GiftIdIdx = Column(Integer, default=0)
    IdIdx = Column(Integer, default=0)
    nKey = Column(Integer, primary_key=True)
    ItemIdx = Column(SmallInteger, default=0)
    Opt = Column(SmallInteger, default=0)
    OptLevel = Column(SmallInteger, default=0)
    Qty = Column(SmallInteger, default=0)
    ServerID = Column(SmallInteger, default=21)
    Flag = Column(Enum('NEW', 'LOCK', 'SPEND', 'BACK'), default='NEW')
    RegDate = Column(DateTime, default='0000-00-00 00:00:00')
    ReceiptDate = Column(DateTime, default='0000-00-00 00:00:00')
    CartID = Column(String, default="")
    uKey = Column(SmallInteger, default=0)


class GameTail_Event(Base):
    __tablename__ = "GameTail_Event"
    num = Column(Integer, default=0)
    SubType = Column(Enum('TNULL', 'HENCH', 'ITEM'), default='ITEM')
    PlayerID = Column(String, default="")
    IdIdx = Column(Integer, default=0)
    nKey = Column(Integer, primary_key=True)
    ObjectIdx = Column(SmallInteger, default=0)
    Qty = Column(SmallInteger, default=0)
    ServerFlag = Column(Enum('define', 'undefine'), default='define')
    ServerID = Column(SmallInteger, default=21)
    Flag = Column(Enum('NEW', 'LOCK', 'SPEND', 'TIME_OVER'), default='NEW')
    RegDate = Column(DateTime, default='0000-00-00 00:00:00')
    ReceiptDate = Column(DateTime, default='0000-00-00 00:00:00')
    Info = Column(String, default="")
    GroupTxt = Column(String, default="")
    StartDate = Column(DateTime, default='0000-00-00 00:00:00')
    EndDate = Column(DateTime, default='0000-00-00 00:00:00')
