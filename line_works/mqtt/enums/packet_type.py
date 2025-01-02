from enum import IntEnum


class PacketType(IntEnum):
    CONNECT = 1
    CONNACK = 2
    PUBLISH = 3
    PUBACK = 4
    SUBSCRIBE = 8
    SUBACK = 9
    PINGREQ = 12
    PINGRESP = 13
    DISCONNECT = 14
