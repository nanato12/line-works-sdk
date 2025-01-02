from line_works.exceptions import LineWorksException


class LineWorksMQTTException(LineWorksException):
    pass


class PacketParseException(LineWorksMQTTException):
    pass
