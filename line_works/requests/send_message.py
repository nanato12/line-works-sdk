from typing import Self

from pydantic import BaseModel, Field

from line_works.enums.message_type import MessageType
from line_works.models.caller import Caller
from line_works.models.sticker import Sticker


class SendMessageRequest(BaseModel):
    service_id: str = Field(alias="serviceId", default="works")
    channel_no: int = Field(alias="channelNo")
    temp_message_id: int = Field(alias="tempMessageId", default=733428260)
    caller: Caller
    extras: str = Field(default="")
    content: str = Field(default="")
    type: MessageType

    class Config:
        populate_by_name = True

    @classmethod
    def text_message(cls, caller: Caller, channel_no: int, text: str) -> Self:
        return cls(
            channel_no=channel_no,
            content=text,
            caller=caller,
            type=MessageType.TEXT,
        )

    @classmethod
    def sticker_message(
        cls, caller: Caller, channel_no: int, sticker: Sticker
    ) -> Self:
        return cls(
            channel_no=channel_no,
            caller=caller,
            extras=sticker.model_dump_json(by_alias=True),
            type=MessageType.STICKER,
        )
