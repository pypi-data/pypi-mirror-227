import time

from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DECIMAL

from game_base.mode.data import Base
from game_base.mode.data import base_mode


class ClubMember(Base):
    # 数据库中存储的表名
    __tablename__ = "club_member"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    club_id = Column(Integer, index=True, comment="亲友圈id")
    create_time = Column(BigInteger, default=int(time.time()), comment="创建时间")
    user_id = Column(Integer, comment="用户ID")
    agent = Column(Boolean, default=False, comment="是否代理")
    agent_id = Column(Integer, default=0, comment="上级代理")
    agent_ids = Column(String(255), default='', comment="代理关系")
    forewarn = Column(DECIMAL(10, 2), default=0, comment="预警值")
    score_ratio = Column(DECIMAL(3, 2), default=0, comment="分数分成")
    guarantees_ratio = Column(DECIMAL(3, 2), default=0, comment="保底分成")


base_mode.init("club_member")
