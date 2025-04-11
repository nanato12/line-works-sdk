from enum import IntEnum


class ConnectionStatus(IntEnum):
    PENDING = 0
    CONNECTED = 1
    DISCONNECTED = 2
