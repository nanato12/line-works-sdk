from line_works.models.sent_message import SentMessage
from line_works.responses._base import BaseResponse


class SendMessageResponse(BaseResponse):
    result: SentMessage
