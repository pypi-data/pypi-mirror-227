from sqlalchemy import Column, Integer, BigInteger, String

from game_base.mode.data import Base
from game_base.mode.data import base_mode


class ClubHistory(Base):
    # 数据库中存储的表名
    __tablename__ = "club_history"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="ID")
    user_id = Column(Integer, nullable=False, comment="user id")
    club_id = Column(Integer, nullable=False, comment="club id")
    create_time = Column(BigInteger, default=0, comment="create time")
    ip = Column(String(16), default='', comment="ip")


base_mode.init("club_history")
