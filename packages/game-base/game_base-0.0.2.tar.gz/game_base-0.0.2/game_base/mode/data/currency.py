from sqlalchemy import Column, Integer, SmallInteger, DECIMAL

from game_base.mode.data import Base
from game_base.mode.data import base_mode


class Currency(Base):
    # 数据库中存储的表名
    __tablename__ = "currency"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID")
    user_id = Column(Integer, nullable=False, comment="user id")
    currency = Column(DECIMAL(10, 2), nullable=False, default=0, comment="currency")
    banker_currency = Column(DECIMAL(10, 2), nullable=False, default=0, comment="banker currency")
    currency_type = Column(SmallInteger, nullable=False, comment="currency type 1.gold 2.room card 3.vouchers")
    union_id = Column(Integer, nullable=False, default=0, comment="union id")


base_mode.init("currency")
