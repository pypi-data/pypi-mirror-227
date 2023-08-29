# coding=utf-8
import decimal
import traceback

from pycore.data.entity import globalvar as gl

from game_base.base.constant import REDIS_ACCOUNT_SESSION, REDIS_SUB_GATEWAY, REDIS_ROOM_LOCK, \
    REDIS_MESSAGE_LIST_COORDINATE_SERVER, REDIS_ROOM_TIMEOUT_LIST
from game_base.base.game.mode import room
from game_base.base.game.mode.game_status import GameStatus
from game_base.base.protocol.base import ENTER_ROOM, ROOM_NOT_EXIST, \
    EXECUTE_ACTION_SCORE_NOT_ENOUGH, UNKNOWN_ERROR, TAKE_SCORE, UPDATE_CURRENCY
from game_base.base.protocol.base import ScoreAction
from game_base.base.send_message import send_to_subscribe, send_to_gateway, send_message_to_server
from game_base.mode.data import base_mode
from game_base.mode.data.currency import Currency
from game_base.mode.data.currency_history import CurrencyHistory


def execute(sid, room_no, session_id, ip, data):
    r"""
    带分
    :param sid: 连接id
    :param room_no: 房间号
    :param session_id: session
    :param ip: ip
    :param data: 收到的数据
    :return:
    """
    account_session = gl.get_v("redis").getobj(REDIS_ACCOUNT_SESSION + session_id)
    score_action = ScoreAction()
    score_action.ParseFromString(data)
    try:
        currency = base_mode.query(Currency, 1, user_id=account_session.account, currency_type=1)
        if None is currency:
            send_to_subscribe(REDIS_SUB_GATEWAY, sid, None, TAKE_SCORE, None, EXECUTE_ACTION_SCORE_NOT_ENOUGH)
            return
        if currency.currency < score_action.score:
            send_to_gateway(TAKE_SCORE, None, account_session.account, EXECUTE_ACTION_SCORE_NOT_ENOUGH)
            return
        if room.exist_room(room_no):
            gl.get_v("redis").lock(REDIS_ROOM_LOCK + room_no)
            try:
                _room = room.get_room(room_no)
                seat = _room.get_seat_by_account(account_session.account)
                if None is seat:
                    return
                base_mode.update(Currency,
                                 {"currency": Currency.currency - decimal.Decimal.from_float(score_action.score)},
                                 user_id=account_session.account, currency_type=1)
                currency_history = CurrencyHistory()
                currency_history.user_id = account_session.account
                currency_history.currency_type = 1
                currency_history.currency = score_action.score
                currency_history.banker_currency = 0
                currency_history.before_currency = float(currency.currency) + score_action.score
                currency_history.before_banker_currency = currency.banker_currency
                currency_history.after_currency = float(currency.currency)
                currency_history.after_banker_currency = currency.banker_currency
                currency_history.type = 1
                currency_history.source = room_no
                base_mode.add(currency_history)
                if _room.game_status == GameStatus.WAITING:
                    seat.score += score_action.score
                else:
                    seat.take_score += score_action.score
                seat.leave_seat = 0
                if None is not seat.leave_seat_timeout:
                    gl.get_v("redis").zrem(REDIS_ROOM_TIMEOUT_LIST + str(_room.game_id), seat.leave_seat_timeout)
                    seat.leave_seat_timeout = None
                    seat.leave_seat = 0
                _room.update_player_info(0)
                send_to_gateway(TAKE_SCORE, None, account_session.account)
                send_message_to_server(REDIS_MESSAGE_LIST_COORDINATE_SERVER, UPDATE_CURRENCY, None, ip, sid)
                _room.check_ready()
                _room.save()
            except:
                gl.get_v("serverlogger").logger.error(traceback.format_exc())
            gl.get_v("redis").unlock(REDIS_ROOM_LOCK + room_no)
        else:
            send_to_subscribe(REDIS_SUB_GATEWAY, sid, None, ENTER_ROOM, None, ROOM_NOT_EXIST)
    except:
        gl.get_v("serverlogger").logger.error(traceback.format_exc())
        send_to_gateway(TAKE_SCORE, None, account_session.account, UNKNOWN_ERROR)
