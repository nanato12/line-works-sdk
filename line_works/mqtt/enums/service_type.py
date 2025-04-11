from enum import IntFlag


class ServiceType(IntFlag):
    UNKNOWN = 0x0000
    VOIP = 0x0001
    MESSAGE = 0x0002
    MAIL = 0x0004
    CALENDAR = 0x0008
    API = 0x0010
    BOARD = 0x0040
    DRIVE = 0x0080
    SCREEN_SHARE = 0x0100
    ASSISTANT = 0x0200
    TASK = 0x0400
    SERVICE = 0x0800
