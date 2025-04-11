from typing import Self

from line_works.enums.message_type import MessageType
from line_works.openapi.talk.models.caller import Caller
from line_works.openapi.talk.models.flex_content import FlexContent
from line_works.openapi.talk.models.send_message_request import (
    SendMessageRequest as BaseSendMessageRequest,
)
from line_works.openapi.talk.models.sticker import Sticker


class SendMessageRequest(BaseSendMessageRequest):
    class Config:
        use_enum_values = True

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

    @classmethod
    def flex_message(
        cls, caller: Caller, channel_no: int, flex_content: FlexContent
    ) -> Self:
        return cls(
            channel_no=channel_no,
            caller=caller,
            extras=flex_content.model_dump_json(by_alias=True),
            type=MessageType.BOT_FLEX,
        )
