import time
import traceback

import sqlalchemy
from pycore.data.entity import globalvar as gl
from sqlalchemy import Column, Integer, String, SmallInteger, Boolean, BigInteger, and_, func
from sqlalchemy.orm import sessionmaker, load_only

from game_base import mode
from game_base.mode.data import Base
from game_base.mode.data import base_mode
from game_base.mode.data.account import Account
from game_base.mode.data.club_member import ClubMember
from game_base.mode.data.currency import Currency


class Club(Base):
    # 数据库中存储的表名
    __tablename__ = "club"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    club_id = Column(Integer, index=True, comment="亲友圈id")
    name = Column(String(32), nullable=False, comment="亲友圈名称")
    create_time = Column(BigInteger, default=int(time.time()), comment="创建时间")
    last_update_time = Column(BigInteger, onupdate=int(time.time()), comment="最后更新时间")
    status = Column(SmallInteger(), default=1, comment="状态 0.暂停 1.正常")
    owner_id = Column(Integer, comment="拥有者")
    join_audit = Column(Boolean, default=False, comment="加入需要审核")
    quit_audit = Column(Boolean, default=False, comment="退出需要审核")
    area_id = Column(Integer, comment="区域id")
    notice = Column(String(255), default='', comment="公告")


def club_list(user_id, limit):
    session = None
    try:
        Session = sessionmaker(mode.data.engine)
        session = Session()
        _select = sqlalchemy.select(Club).options(
            load_only(Club.club_id, Club.name, Club.area_id)) \
            .join(ClubMember, Club.id == ClubMember.club_id).filter(ClubMember.user_id == user_id).offset(
            limit[0] - 1).limit(limit[1])
        return session.execute(_select).scalars().all()
    except:
        gl.get_v("serverlogger").logger.error(traceback.format_exc())
    finally:
        if None is not session:
            session.close()


def my_member(club_id, limit, agent_id, union_id):
    session = None
    try:
        Session = sessionmaker(mode.data.engine)
        session = Session()
        _select = sqlalchemy.select(Account, ClubMember, Currency).options(
            load_only(Account.account_name, Account.nickname),
            load_only(ClubMember.forewarn, ClubMember.score_ratio, ClubMember.guarantees_ratio),
            load_only(Currency.currency, Currency.banker_currency)) \
            .join(ClubMember, ClubMember.user_id == Account.id) \
            .join(Currency,
                  and_(Currency.user_id == Account.id, Currency.currency_type == 1, Currency.union_id == union_id)) \
            .filter(ClubMember.club_id == club_id, ClubMember.agent_id == agent_id) \
            .offset(limit[0] - 1).limit(limit[1])
        return session.execute(_select).all()
    except:
        gl.get_v("serverlogger").logger.error(traceback.format_exc())
    finally:
        if None is not session:
            session.close()


def my_agent(club_id, limit, agent_id, union_id):
    session = None
    try:
        Session = sessionmaker(mode.data.engine)
        session = Session()
        _select = sqlalchemy.select(Account, ClubMember, Currency, func.count(ClubMember.id)).options(
            load_only(Account.account_name, Account.nickname),
            load_only(ClubMember.forewarn, ClubMember.score_ratio, ClubMember.guarantees_ratio),
            load_only(Currency.currency, Currency.banker_currency)) \
            .join(ClubMember, ClubMember.user_id == Account.id) \
            .join(Currency,
                  and_(Currency.user_id == Account.id, Currency.currency_type == 1, Currency.union_id == union_id)) \
            .filter(ClubMember.club_id == club_id, ClubMember.agent_id == agent_id, ClubMember.agent is True) \
            .offset(limit[0] - 1).limit(limit[1])
        return session.execute(_select).all()
    except:
        gl.get_v("serverlogger").logger.error(traceback.format_exc())
    finally:
        if None is not session:
            session.close()


def all_member(club_id, limit, union_id):
    session = None
    try:
        Session = sessionmaker(mode.data.engine)
        session = Session()
        _select = sqlalchemy.select(Account, ClubMember, Currency).options(
            load_only(Account.account_name, Account.nickname),
            load_only(ClubMember.forewarn, ClubMember.score_ratio, ClubMember.guarantees_ratio),
            load_only(Currency.currency, Currency.banker_currency)) \
            .join(ClubMember, ClubMember.user_id == Account.id) \
            .join(Currency,
                  and_(Currency.user_id == Account.id, Currency.currency_type == 1, Currency.union_id == union_id)) \
            .filter(ClubMember.club_id == club_id) \
            .offset(limit[0] - 1).limit(limit[1])
        return session.execute(_select).all()
    except:
        gl.get_v("serverlogger").logger.error(traceback.format_exc())
    finally:
        if None is not session:
            session.close()


base_mode.init("club")
