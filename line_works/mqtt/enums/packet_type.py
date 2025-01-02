from enum import IntEnum


class PacketType(IntEnum):
    CONNECT = 1
    CONNACK = 2
    PUBLISH = 3
    PUBACK = 4
    UNKNWON = 6  # TODO: Rename when you know
    UNKNWON_2 = 7  # TODO: Rename when you know
    SUBSCRIBE = 8
    SUBACK = 9
    PINGREQ = 12
    PINGRESP = 13
    DISCONNECT = 14
