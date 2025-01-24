import json
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
        cls,
        caller: Caller,
        channel_no: int,
        package_id: str,
        sticker_id: str,
        sticker_option: str = "",
        sticker_version: str = "",
        sticker_type: str = "line",
    ) -> Self:
        return cls(
            channel_no=channel_no,
            caller=caller,
            extras=json.dumps(
                {
                    "pkgVer": sticker_version,
                    "pkgId": package_id,
                    "stkId": sticker_id,
                    "stkType": sticker_type,
                    "stkOpt": sticker_option,
                }
            ),
            type=MessageType.STICKER,
        )
