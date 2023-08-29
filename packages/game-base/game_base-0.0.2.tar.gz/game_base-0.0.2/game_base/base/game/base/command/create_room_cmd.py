# coding=utf-8
import json
import traceback

from pycore.data.entity import globalvar as gl

from game_base.base.constant import REDIS_ACCOUNT_SESSION, REDIS_SUB_GATEWAY, REDIS_ACCOUNT_GAME
from game_base.base.protocol.base import CREATE_ROOM, ENTER_ROOM, ROOM_ALREADY
from game_base.base.protocol.base import ReqCreateRoom, ReqEnterRoom
from game_base.base.send_message import send_to_subscribe, send_to_gateway


def execute(sid, room_no, session_id, ip, data):
    r"""
    创建房间
    :param sid: 连接id
    :param room_no: 房间号
    :param session_id: session
    :param ip: ip
    :param data: 收到的数据
    :return:
    """
    account_session = gl.get_v("redis").getobj(REDIS_ACCOUNT_SESSION + session_id)
    create_room = ReqCreateRoom()
    create_room.ParseFromString(data)
    if gl.get_v("redis").hexists(REDIS_ACCOUNT_GAME, account_session.account):
        send_to_gateway(CREATE_ROOM, None, account_session.account, ROOM_ALREADY)
        return
    if create_room.gameType == 0:
        with open("./conf/roomcard/roomcard1.json", "r") as data:
            room_card_conf = json.load(data)
            confs = [conf for conf in room_card_conf if (conf["gameTimes"] == 5 and conf["peopleCount"] == 8)]
        if len(confs) != 0:
            room_card = confs[0]["roomCard"]
            try:
                # TODO 检测房卡
                # if None is card or card.currency < room_card:
                #     send_to_subscribe(REDIS_SUB_GATEWAY, sid, None, CREATE_ROOM, None, ROOM_CARD_NOT_ENOUGH)
                # else:
                room_no = gl.get_v("game_command")["create_room"].execute(account_session.account, create_room)
                gl.get_v("serverlogger").logger.info("房间号" + str(room_no))
                send_to_subscribe(REDIS_SUB_GATEWAY, sid, None, CREATE_ROOM, None)
                enter_room = ReqEnterRoom()
                enter_room.roomNo = room_no
                gl.get_v("command")[str(ENTER_ROOM)].execute(sid, room_no, session_id, ip,
                                                             enter_room.SerializeToString())
            except:
                gl.get_v("serverlogger").logger.error(traceback.format_exc())

