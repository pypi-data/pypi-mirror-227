import time

from sqlalchemy import Column, Integer, BigInteger

from game_base.mode.data import Base
from game_base.mode.data import base_mode


class UnionMember(Base):
    # 数据库中存储的表名
    __tablename__ = "union_member"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    union_id = Column(Integer, index=True, comment="联盟id")
    create_time = Column(BigInteger, default=int(time.time()), comment="创建时间")
    club_id = Column(Integer, comment="亲友圈ID")


base_mode.init("union_member")
