from typing import Optional

from pydantic import BaseModel, Field

from line_works.mqtt.enums.notification_type import NotificationType


class NotificationMessage(BaseModel):
    a_badge: int = Field(alias="aBadge")
    badge: int
    bot_info: str = Field(alias="botInfo", default="")
    c_badge: int = Field(alias="cBadge")
    channel_no: Optional[int] = Field(alias="chNo", default=None)
    channel_photo_path: str = Field(alias="chPhotoPath", default="")
    channel_title: str = Field(alias="chTitle", default="")
    channel_type: Optional[int] = Field(alias="chType", default=None)
    create_time: Optional[int] = Field(alias="createTime", default="")
    domain_id: int = Field(alias="domain_id")
    extras: str = Field(default="")
    from_photo_hash: str = Field(alias="fromPhotoHash", default="")
    from_user_no: Optional[int] = Field(alias="fromUserNo", default=None)
    h_badge: int = Field(alias="hBadge")
    loc_args0: str = Field(alias="loc-args0", default="")
    loc_args1: str = Field(alias="loc-args1", default="")
    loc_key: str = Field(alias="loc-key", default="")
    m_badge: int = Field(alias="mBadge")
    message_no: Optional[int] = Field(alias="messageNo", default=None)
    notification_type: NotificationType = Field(alias="nType")
    notification_id: str = Field(alias="notification-id", default="")
    ocn: int
    s_type: int = Field(alias="sType")
    token: str
    user_no: int = Field(alias="userNo")
    wpa_badge: int = Field(alias="wpaBadge")

    class Config:
        populate_by_name = True
