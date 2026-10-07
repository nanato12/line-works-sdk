from line_works.exceptions import LineWorksException


class LineWorksMQTTException(LineWorksException):
    pass


class PacketParseException(LineWorksMQTTException):
    pass


class MQTTConnectionException(LineWorksMQTTException):
    """接続の確立・維持に失敗した"""


class MQTTConnectionRefused(MQTTConnectionException):
    """サーバが CONNECT を拒否した (CONNACK の return code が 0 以外)"""


class MQTTConnectionLost(MQTTConnectionException):
    """接続が失われた (無通信タイムアウト、サーバからの DISCONNECT など)"""
