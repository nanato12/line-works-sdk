from typing import Self

from pydantic import BaseModel, Field

from line_works.enums.message_type import MessageType
from line_works.models.caller import Caller


class SendMessageRequest(BaseModel):
    service_id: str = Field(alias="serviceId", default="works")
    channel_no: int = Field(alias="channelNo")
    temp_message_id: int = Field(alias="tempMessageId", default=733428260)
    caller: Caller
    extras: str = Field(default="")
    content: str
    type: MessageType

    class Config:
        populate_by_name = True

    @classmethod
    def text_message(cls, channel_no: int, text: str, caller: Caller) -> Self:
        return cls(
            channel_no=channel_no,
            content=text,
            caller=caller,
            type=MessageType.TEXT,
        )
