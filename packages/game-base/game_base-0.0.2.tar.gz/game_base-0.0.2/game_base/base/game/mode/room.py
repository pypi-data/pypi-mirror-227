# coding=utf-8
import time

import pycore.data.entity.globalvar as gl
from game_base.utils import int_utils

from game_base.base.constant import REDIS_ROOM_MAP, REDIS_ACCOUNT_GAME, REDIS_UNION_ROOM_MAP
from game_base.base.game.mode.game_status import GameStatus
from game_base.base.protocol.base import ENTER_ROOM, UPDATE_GAME_INFO, UPDATE_GAME_PLAYER_INFO, SELF_INFO, \
    REENTER_GAME_INFO, START_GAME, EXECUTE_ACTION, UNKNOWN_ERROR, STAND_UP
from game_base.base.protocol.base import RecGpsInfo, RecUpdateGameInfo, RecUpdateGameUsers, \
    RecReEnterGameInfo, RecExecuteAction
from game_base.base.send_message import send_to_gateway


def seat2_user_info(seat, user_info):
    u"""
    座位转用户信息
    :param seat: 座位
    :param user_info: 用户信息
    :return: 用户信息
    """
    user_info.playerId = seat.user_id
    user_info.account = seat.account
    user_info.nick = seat.nickname
    user_info.headUrl = seat.head
    user_info.sex = seat.sex
    user_info.ip = seat.ip
    user_info.address = seat.address
    if None is not seat.gps_info:
        user_info.gpsInfo = seat.gps_info
    user_info.ready = seat.ready
    user_info.score = seat.score - seat.play_score
    # user_info.playScore = seat.play_score
    # user_info.banker = self.banker == seat.seat_no
    user_info.seatNo = seat.seat_no
    user_info.createTime = seat.create_time
    user_info.online = seat.online
    if 0 != seat.leave_seat:
        leave_time = seat.leave_seat - int(time.time())
        if leave_time > 0:
            user_info.leaveSeat = leave_time
    return user_info


def get_room(room_no):
    u"""
    通过房间号获取房间
    :param room_no:
    :return:
    """
    room_no_info = room_no.split(',')
    if room_no_info[1] == '0':
        return gl.get_v("redis").hgetobj(REDIS_ROOM_MAP, room_no_info[0])
    else:
        return gl.get_v("redis").hgetobj(REDIS_UNION_ROOM_MAP + room_no_info[2] + room_no_info[1], room_no_info[0])


def exist_room(room_no):
    u"""
    房间是否存在
    :param room_no:
    :return:
    """
    room_no_info = room_no.split(',')
    if room_no_info[1] == '0':
        return gl.get_v("redis").hexists(REDIS_ROOM_MAP, room_no_info[0])
    else:
        return gl.get_v("redis").hexists(REDIS_UNION_ROOM_MAP + room_no_info[2] + room_no_info[1], room_no_info[0])


class Room(object):

    def __init__(self) -> None:
        self.room_no = None
        self.game_id = 0
        self.game_type = 0
        self.pay_type = 0
        self.score = 0
        self.in_score = 0
        self.leave_score = 0
        self.game_times = 0
        self.times_type = 0
        self.people_count = 0
        self.people_start = 0
        self.leave_type = 0
        self.game_rules = 0
        self.gps_limit = 0
        self.match_level = 0
        self.watch_seats = []
        self.seats = []
        self.seat_nos = []
        self.start_time = int(time.time())
        self.game_status = GameStatus.WAITING
        self.history_actions = []
        self.room_owner = 0
        self.current_game_times = 0
        self.operation_time = 0
        self.last_operation_time = 0
        self.desk_score = 0
        self.banker = 0
        self.min_score = 0
        self.operation_seat = 0
        self.record_ids = []
        self.total_win_lose = {}
        self.union_id = 0
        self.room_type = 0
        self.room_config_id = 0

    def save(self):
        u"""
        保存房间信息
        """
        if 0 == self.union_id:
            if self.game_status != GameStatus.DESTORY:
                gl.get_v("redis").hsetobj(REDIS_ROOM_MAP, self.room_no, self)
            else:
                gl.get_v("redis").hdelobj(REDIS_ROOM_MAP, self.room_no)
                del self
        else:
            if self.game_status != GameStatus.DESTORY:
                gl.get_v("redis").hsetobj(REDIS_UNION_ROOM_MAP + str(self.room_type) + str(self.union_id), self.room_no,
                                          self)
            else:
                gl.get_v("redis").hdelobj(REDIS_UNION_ROOM_MAP + str(self.room_type) + str(self.union_id), self.room_no)
                del self

    def clear(self):
        self.game_status = GameStatus.WAITING
        self.desk_score = 0
        self.min_score = 0
        self.operation_seat = 0
        self.history_actions.clear()
        for s in self.seats:
            s.clear()
        for s in self.watch_seats:
            s.clear()

    def get_game_rule(self, index):
        int_utils.has_bit(self.game_rules, index)

    def get_seat_by_seat_no(self, seat_no):
        for s in self.seats:
            if s.seat_no == seat_no:
                return s
        return None

    def get_seat_by_account(self, user_id):
        for s in self.seats:
            if s.user_id == user_id:
                return s
        return None

    def get_watch_seat_by_account(self, user_id):
        for s in self.watch_seats:
            if s.user_id == user_id:
                return s
        return None

    def get_playing_count(self):
        count = 0
        for s in self.seats:
            if s.gaming and not s.end:
                count += 1
        return count

    def get_gpa_info(self):
        rec_gps_info = RecGpsInfo()
        for seat in self.seats:
            gps_player_info = rec_gps_info.playerInfos.add()
            gps_player_info.gpsInfo = seat.gps_info
            gps_player_info.playerId = seat.user_id
        return rec_gps_info

    def join_room(self, account, ip):
        send_to_gateway(ENTER_ROOM, None, account.id)
        send_to_gateway(UPDATE_GAME_INFO, self.update_game_info().SerializeToString(), account.id)
        seat = self.get_seat_by_account(account.id)
        if seat is None:
            seat = self.get_watch_seat_by_account(account.id)
        user_info = seat2_user_info(seat, RecUpdateGameUsers.UserInfo())
        send_to_gateway(SELF_INFO, user_info.SerializeToString(), account.id)
        self.update_player_info(account.id)
        if self.game_status != GameStatus.WAITING:
            self.reenter_game_info(account.id)
        gl.get_v("redis").hset(REDIS_ACCOUNT_GAME, account.id,
                               '%s,%s,%d' % (self.room_no, self.union_id, self.game_type))
        self.save()

    def stand_up(self, user_id):
        seat = self.get_seat_by_account(user_id)
        if None is not seat:
            self.seat_nos.append(seat.seat_no)
            seat.seat_no = 0
            self.watch_seats.append(seat)
            self.seats.remove(seat)
            send_to_gateway(STAND_UP, None, user_id)
            self.update_player_info(0)
            return
        send_to_gateway(STAND_UP, None, user_id, UNKNOWN_ERROR)
        self.check_ready()

    def reconnect(self, user_id, ip):
        seat = self.get_seat_by_account(user_id)
        if None is seat:
            seat = self.get_watch_seat_by_account(user_id)
        if seat is not None:
            seat.ip = ip
            seat.online = True
            send_to_gateway(ENTER_ROOM, None, user_id)
            send_to_gateway(UPDATE_GAME_INFO, self.update_game_info().SerializeToString(), user_id)
            user_info = seat2_user_info(seat, RecUpdateGameUsers.UserInfo())
            send_to_gateway(SELF_INFO, user_info.SerializeToString(), user_id)
            self.update_player_info(0)
            if self.game_status != GameStatus.WAITING:
                self.reenter_game_info(user_id)

    def update_game_info(self):
        update_game_info = RecUpdateGameInfo()
        update_game_info.roomNo = self.room_no
        update_game_info.gameState = self.game_status
        update_game_info.curPlayCount = self.current_game_times
        update_game_info.createRoom.gameId = self.game_id
        update_game_info.createRoom.gameType = self.game_type
        update_game_info.createRoom.payType = self.pay_type
        update_game_info.createRoom.baseScore = self.score
        update_game_info.createRoom.inScore = self.in_score
        update_game_info.createRoom.leaveScore = self.leave_score
        update_game_info.createRoom.gameTimes = self.game_times
        update_game_info.createRoom.timesType = self.times_type
        update_game_info.createRoom.peopleCount = self.people_count
        update_game_info.createRoom.peopleStart = self.people_start
        update_game_info.createRoom.leaveType = self.leave_type
        update_game_info.createRoom.gameRules = self.game_rules
        update_game_info.createRoom.gpsLimit = self.gps_limit
        update_game_info.createRoom.operationTime = self.operation_time
        return update_game_info

    def update_player_info(self, user_id):
        game_users = self.player_info()
        if 0 == user_id:
            self.broadcast_all_to_gateway(UPDATE_GAME_PLAYER_INFO, game_users.SerializeToString())
        else:
            send_to_gateway(UPDATE_GAME_PLAYER_INFO, game_users.SerializeToString(), user_id)

    def player_info(self):
        game_users = RecUpdateGameUsers()
        for seat in self.seats:
            seat2_user_info(seat, game_users.users.add())
        return game_users

    def reenter_game_info(self, user_id):
        game_info = RecReEnterGameInfo()
        for a in self.history_actions:
            execute_action = game_info.actionInfos.add()
            execute_action.ParseFromString(a)
        send_to_gateway(REENTER_GAME_INFO, game_info.SerializeToString(), user_id)

    def check_ready(self):
        if self.game_status == GameStatus.WAITING:
            all_ready = True
            for seat in self.seats:
                if (not seat.ready or seat.score < self.in_score) and 0 == seat.leave_seat:
                    all_ready = False
                    break
            if all_ready:
                self.start()

    def start(self):
        if self.game_status == GameStatus.WAITING:
            if len(self.seats) - self.leave_seat_people() < self.get_start_people():
                gl.get_v("serverlogger").logger.exception("user count < start_people, cant start")
                return
            for seat in self.seats:
                if 0 == seat.leave_seat:
                    seat.score += seat.take_score
                    seat.take_score = 0
                    seat.ready = False
                    seat.gaming = True
            self.broadcast_seat_to_gateway(START_GAME, None)

    def change_operation(self):
        thisop = self.operation_seat
        next_seat_no = self.get_next_seat(self.operation_seat)
        next_operation = self.get_seat_by_seat_no(next_seat_no)
        count = 0
        while None is next_operation or next_operation.end or not next_operation.gaming or 0 == next_operation.score - next_operation.play_score - next_operation.play_mangguo:
            next_seat_no = self.get_next_seat(next_seat_no)
            next_operation = self.get_seat_by_seat_no(next_seat_no)
            count += 1
            if thisop == next_seat_no or count == self.people_count:
                return 0
        self.operation_seat = next_seat_no
        return self.operation_seat

    def get_next_seat(self, next_seat):
        next_seat += 1
        if next_seat > self.people_count:
            return 1
        return next_seat

    def execute_action(self, user_id, action_type, data):
        execute_action = RecExecuteAction()
        execute_action.actionType = action_type
        execute_action.playerId = user_id
        if data is not None:
            execute_action.data = data
        self.broadcast_all_to_gateway(EXECUTE_ACTION, execute_action.SerializeToString())
        self.history_actions.append(execute_action.SerializeToString())

    def leave_seat_people(self):
        leave_count = 0
        for seat in self.seats:
            if 0 != seat.leave_seat:
                leave_count += 1
        return leave_count

    def get_start_people(self):
        if self.current_game_times == 0:
            return self.people_start
        return 2

    def broadcast_seat_to_gateway(self, opcode, data, skip=None):
        if skip is None:
            skip = []
        for seat in self.seats:
            if seat.user_id not in skip:
                send_to_gateway(opcode, data, seat.user_id)

    def broadcast_watch_to_gateway(self, opcode, data, skip=None):
        if skip is None:
            skip = []
        for seat in self.watch_seats:
            if seat.user_id not in skip:
                send_to_gateway(opcode, data, seat.user_id)

    def broadcast_all_to_gateway(self, opcode, data, skip=None):
        self.broadcast_seat_to_gateway(opcode, data, skip)
        self.broadcast_watch_to_gateway(opcode, data, skip)
