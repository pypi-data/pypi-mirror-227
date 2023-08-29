import time

from sqlalchemy import Column, Integer, SmallInteger, DECIMAL, String, BigInteger

from game_base.mode.data import Base
from game_base.mode.data import base_mode


class CurrencyHistory(Base):
    # 数据库中存储的表名
    __tablename__ = "currency_history"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID")
    user_id = Column(Integer, nullable=False, comment="user id")
    currency_type = Column(SmallInteger, nullable=False, comment="currency type  1.room card 2.gold")
    currency = Column(DECIMAL(10, 2), nullable=False, default=0, comment="currency")
    create_time = Column(BigInteger, default=int(time.time()), comment="create time")
    banker_currency = Column(DECIMAL(10, 2), nullable=False, default=0, comment="banker currency")
    before_currency = Column(DECIMAL(10, 2), nullable=False, default=0, comment="before currency")
    before_banker_currency = Column(DECIMAL(10, 2), nullable=False, default=0, comment="before banker currency")
    after_currency = Column(DECIMAL(10, 2), nullable=False, default=0, comment="after currency")
    after_banker_currency = Column(DECIMAL(10, 2), nullable=False, default=0, comment="after banker currency")
    type = Column(SmallInteger, nullable=False, comment="type 1.game 2.register 3.invite")
    remark = Column(String(64), default='', comment="remark")
    source = Column(String(64), default='', comment="source")


base_mode.init("currency_history")
