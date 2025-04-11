import json
from typing import Optional

from pydantic import Field

from line_works.exceptions import LogicException
from line_works.mqtt.enums.channel_type import ChannelType
from line_works.mqtt.enums.notification_type import NotificationType
from line_works.mqtt.models.payload.badge import BadgePayload
from line_works.openapi.talk.models.sticker import Sticker


class MessagePayload(BadgePayload):
    bot_info: str = Field(alias="botInfo", default="")
    channel_no: Optional[int] = Field(alias="chNo", default=None)
    channel_photo_path: str = Field(alias="chPhotoPath", default="")
    channel_title: str = Field(alias="chTitle", default="")
    channel_type: Optional[ChannelType] = Field(alias="chType", default=None)
    create_time: Optional[int] = Field(alias="createTime", default="")
    extras: str = Field(default="")
    from_photo_hash: str = Field(alias="fromPhotoHash", default="")
    from_user_no: Optional[int] = Field(alias="fromUserNo", default=None)
    message_no: Optional[int] = Field(alias="messageNo", default=None)
    notification_id: str = Field(alias="notification-id", default="")

    class Config:
        populate_by_name = True

    @property
    def unique_id(self) -> str:
        return f"{self.loc_key}_{self.notification_id}"

    @property
    def extras_dict(self) -> dict:
        return json.loads(self.extras) if self.extras else {}

    @property
    def sticker(self) -> Sticker:
        if self.notification_type == NotificationType.NOTIFICATION_STICKER:
            return Sticker(**self.extras_dict)
        raise LogicException(
            f"Invalid notification type: {self.notification_type}. "
            f"Expected {NotificationType.NOTIFICATION_STICKER}."
        )
