from typing import Optional

from pydantic import BaseModel, Field


class NotificationMessage(BaseModel):
    a_badge: int = Field(alias="aBadge")
    badge: int
    bot_info: str = Field(alias="botInfo")
    c_badge: int = Field(alias="cBadge")
    channel_no: int = Field(alias="chNo")
    channel_photo_path: str = Field(alias="chPhotoPath")
    channel_title: str = Field(alias="chTitle")
    channel_type: int = Field(alias="chType")
    create_time: int = Field(alias="createTime")
    domain_id: int = Field(alias="domain_id")
    extras: str
    from_photo_hash: str = Field(alias="fromPhotoHash")
    from_user_no: int = Field(alias="fromUserNo")
    h_badge: int = Field(alias="hBadge")
    loc_args0: str = Field(alias="loc-args0")
    loc_args1: Optional[str] = Field(alias="loc-args1", default=None)
    loc_key: str = Field(alias="loc-key")
    m_badge: int = Field(alias="mBadge")
    message_no: int = Field(alias="messageNo")
    notification_type: int = Field(alias="nType")
    notification_id: str = Field(alias="notification-id")
    ocn: int
    s_type: int = Field(alias="sType")
    token: str
    user_no: int = Field(alias="userNo")
    wpa_badge: int = Field(alias="wpaBadge")

    class Config:
        populate_by_name = True
