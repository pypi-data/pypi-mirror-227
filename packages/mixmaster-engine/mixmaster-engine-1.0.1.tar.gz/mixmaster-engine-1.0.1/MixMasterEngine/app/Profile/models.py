from sqlalchemy import Column, Integer, String, Enum, DateTime, SmallInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from termcolor import colored

Base = declarative_base()


class Players(Base):
    __tablename__ = 'Player'
    id_idx = Column(Integer, primary_key=True)
    PlayerID = Column(String)
    Passwd = Column(String)
    Passwd_Q = Column(String, nullable=False)
    Passwd_A = Column(String, nullable=False)
    Name = Column(String)
    JuminNo = Column(String, default="")
    nYear = Column(String, default="")
    nMonth = Column(String, default="")
    nDay = Column(String, nullable=False)
    Sex = Column(Enum('1', '2'), default="1")
    TelePhone1 = Column(String, nullable=False)
    TelePhone2 = Column(String, default="")
    TelePhone3 = Column(String, default="")
    CPhone1 = Column(String, nullable=False)
    CPhone2 = Column(String, default="")
    CPhone3 = Column(String, default="")
    ZipCode = Column(String, default="")
    AddressDo = Column(String, nullable=False)
    AddressSi = Column(String, nullable=False)
    AddressDong = Column(String, nullable=False)
    AddressEtc = Column(String, nullable=False)
    Address = Column(String, nullable=False)
    Email = Column(String)
    JobType = Column(String, nullable=False)
    SchoolName = Column(String, nullable=False)
    Access = Column(SmallInteger, default=21)
    Block = Column(Enum('ALLOW', 'GAME', 'WEB', 'SUM',
                   'SUCEDER', 'WAIT'), default="ALLOW")
    LoginIP = Column(String, nullable=False)
    NewsLetter = Column(Enum('1', '2'), default="1")
    ParentName = Column(String, nullable=False)
    ParentJuminNo = Column(String, nullable=False)
    ParentPhone1 = Column(String, nullable=False)
    ParentPhone2 = Column(String, default="")
    ParentPhone3 = Column(String, default="")
    LastLoginDate = Column(DateTime, nullable=False)
    SecederDate = Column(DateTime, nullable=False)
    PayPlayDate = Column(DateTime, nullable=False)
    PayPlayHours = Column(Integer, default=0)
    RegDate = Column(DateTime, default='0000-00-00 00:00:00')
    OldBlock = Column(Enum('ALLOW', 'GAME', 'WEB', 'SUM',
                      'SUCEDER', 'WAIT'), default="ALLOW")
    ssoChk = Column(String, nullable=False)
    AuthCheck = Column(Enum('AUTH_OK', 'AUTH_WAIT',
                       'AUTH_CHECK'), default="AUTH_OK")
    AuthTimeLimit = Column(DateTime, default='0000-00-00 00:00:00')
    LoginState = Column(SmallInteger, default=0)
    personal_auth = Column(String, nullable=False)
    Accesschecktype = Column(Integer, nullable=False)
    PlayerNickName = Column(String, nullable=False)
    PlayerGameServer = Column(String, nullable=False)
    IsAdmin = Column(Integer, nullable=False)
    CashPoint = Column(Integer, nullable=False)

    @property
    def formatted_LastLoginDate(self, LastLoginDate):
        return self.LastLoginDate.strftime("%Y-%m-%d %H:%M:%S")

    @property
    def formatted_SecederDate(self, SecederDate):
        return self.SecederDate.strftime("%Y-%m-%d %H:%M:%S")

    @property
    def formatted_PayPlayDate(self, PayPlayDate):
        return self.PayPlayDate.strftime("%Y-%m-%d %H:%M:%S")

    @property
    def formatted_RegDate(self, RegDate):
        return self.RegDate.strftime("%Y-%m-%d %H:%M:%S")
