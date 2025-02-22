from enum import IntEnum


class Presence(IntEnum):
    WEB_ONLINE = 0x00000080
    WEB_AWAY = 0x00000080 | 0x00000002
