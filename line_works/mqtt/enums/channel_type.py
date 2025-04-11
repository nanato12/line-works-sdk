from enum import IntEnum


class ChannelType(IntEnum):
    UNKNOWN = 0
    PRIVATE = 1
    ROOM = 2
    TEAM = 3
    GROUP = 4
    BOT = 5
    EXTERNAL_PRIVATE = 6
    EXTERNAL_ROOM = 7
    EXTERNAL_GROUP = 9
    EXTERNAL_LINE_GROUP = 10
    PTT = 12
