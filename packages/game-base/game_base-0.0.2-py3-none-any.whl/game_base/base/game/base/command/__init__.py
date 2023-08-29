from game_base.base.server import Server
from game_base.base.game.base.command import enter_room_cmd, record_cmd, take_score_cmd, gps_cmd
from game_base.base.game.base.command import stand_up_cmd, exit_room_cmd, voice_cmd, action_cmd, chat_cmd, ready_cmd, \
    reconnect_cmd, room_review_cmd, seat_down_cmd, room_record_cmd, create_room_cmd
from game_base.base.game.base.command import online_cmd
from game_base.base.protocol.base import CREATE_ROOM, ENTER_ROOM, RECONNECT, READY, SEAT_DOWN, EXECUTE_ACTION, \
    TAKE_SCORE, \
    EXIT_ROOM, PLAYER_CHAT, PLAYER_VOICE, PLAYER_ONLINE, PLAYER_GPS, STAND_UP, ROOM_REVIEW


def init_command():
    command = dict()
    command[str(CREATE_ROOM)] = create_room_cmd
    command[str(ENTER_ROOM)] = enter_room_cmd
    command[str(RECONNECT)] = reconnect_cmd
    command[str(READY)] = ready_cmd
    command[str(SEAT_DOWN)] = seat_down_cmd
    command[str(STAND_UP)] = stand_up_cmd
    command[str(EXECUTE_ACTION)] = action_cmd
    command[str(TAKE_SCORE)] = take_score_cmd
    command[str(EXIT_ROOM)] = exit_room_cmd
    command[str(ROOM_REVIEW)] = room_review_cmd
    command[str(PLAYER_CHAT)] = chat_cmd
    command[str(PLAYER_VOICE)] = voice_cmd
    command[str(PLAYER_ONLINE)] = online_cmd
    command[str(PLAYER_GPS)] = gps_cmd
    command["record"] = record_cmd
    command["room_record"] = room_record_cmd
    Server.init_command(command)
