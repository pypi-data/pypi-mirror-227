import time

from sqlalchemy import Column, Integer, String, BigInteger, SmallInteger

from game_base.mode.data import Base
from game_base.mode.data import base_mode


class Account(Base):
    # 数据库中存储的表名
    __tablename__ = "account"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID")
    account_name = Column(String(32), index=True, nullable=False, comment="account")
    nickname = Column(String(8), nullable=False, default='', comment="nickname")
    sex = Column(SmallInteger, nullable=False, default=0, comment="sex(0.unknown 1.man 2.woman)")
    head_url = Column(String(32), nullable=False, default='', comment="head url")
    pwd = Column(String(32), comment="pwd")
    salt = Column(String(32), comment="salt")
    create_time = Column(BigInteger, default=int(time.time()), comment="create time")
    status = Column(SmallInteger, nullable=False, default=0, comment="status")
    bank_pwd = Column(String(32), comment="bank pwd")
    # 权限
    authority = Column(SmallInteger, nullable=False, default=0, comment="authority")
    phone = Column(String(16), default='', comment="phone number")
    wechat = Column(String(64), default='', comment="register wechat")
    device = Column(String(64), default='', comment="register device")
    ip = Column(String(16), default='', comment="register ip")
    code = Column(String(4), default='', comment="code")


base_mode.init("account")
