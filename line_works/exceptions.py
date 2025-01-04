class LineWorksException(Exception):
    pass


class LoginException(LineWorksException):
    pass


class GetMyInfoException(LineWorksException):
    pass


class SendMessageException(LineWorksException):
    pass
