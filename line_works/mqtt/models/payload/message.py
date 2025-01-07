from typing import Optional

from pydantic import Field

from line_works.mqtt.models.payload.badge import BadgePayload


class MessagePayload(BadgePayload):
    bot_info: str = Field(alias="botInfo", default="")
    channel_no: Optional[int] = Field(alias="chNo", default=None)
    channel_photo_path: str = Field(alias="chPhotoPath", default="")
    channel_title: str = Field(alias="chTitle", default="")
    channel_type: Optional[int] = Field(alias="chType", default=None)
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
