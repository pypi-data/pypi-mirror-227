# coding=utf-8
import traceback

from pycore.data.entity import globalvar as gl

from game_base.base.constant import REDIS_ACCOUNT_SESSION, REDIS_SUB_GATEWAY, REDIS_ROOM_LOCK, \
    REDIS_ACCOUNT_GAME
from game_base.base.game.mode import room
from game_base.base.protocol.base import ENTER_ROOM, ROOM_ALREADY, UNKNOWN_ERROR, ROOM_NOT_EXIST
from game_base.base.protocol.base import ReqEnterRoom
from game_base.base.send_message import send_to_subscribe, send_to_gateway
from game_base.mode.data import base_mode
from game_base.mode.data.account import Account


def execute(sid, room_no, session_id, ip, data):
    r"""
    进去房间
    :param sid: 连接id
    :param room_no: 房间号
    :param session_id: session
    :param ip: ip
    :param data: 收到的数据
    :return:
    """
    account_session = gl.get_v("redis").getobj(REDIS_ACCOUNT_SESSION + session_id)
    if gl.get_v("redis").hexists(REDIS_ACCOUNT_GAME, account_session.account):
        send_to_gateway(ENTER_ROOM, None, account_session.account, ROOM_ALREADY)
        return
    enter_room = ReqEnterRoom()
    enter_room.ParseFromString(data)
    room_no = enter_room.roomNo
    account = None
    try:
        account = base_mode.get(Account, account_session.account)
        if None is account:
            send_to_subscribe(REDIS_SUB_GATEWAY, sid, None, ENTER_ROOM, None, UNKNOWN_ERROR)
            return
    except:
        gl.get_v("serverlogger").logger.error(traceback.format_exc())
    if room.exist_room(enter_room.roomNo + ',0,0'):
        gl.get_v("redis").lock(REDIS_ROOM_LOCK + room_no)
        try:
            _room = room.get_room(room_no + ',0,0')
            # if 0 < len(room.seat_nos):
            _room.join_room(account, ip)
            # else:
            #     rec_enter_room.state = 3
            #     send_to_subscribe(REDIS_SUB_GATEWAY, sid, None, ENTER_ROOM, None, ROOM_CARD_NOT_ENOUGH)
        except:
            gl.get_v("serverlogger").logger.error(traceback.format_exc())
        gl.get_v("redis").unlock(REDIS_ROOM_LOCK + room_no)
    else:
        send_to_subscribe(REDIS_SUB_GATEWAY, sid, None, ENTER_ROOM, None, ROOM_NOT_EXIST)
