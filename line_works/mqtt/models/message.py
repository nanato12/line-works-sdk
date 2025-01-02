from pydantic import BaseModel, Field


class NotificationMessage(BaseModel):
    a_badge: int = Field(..., alias="aBadge")
    badge: int
    bot_info: str = Field(..., alias="botInfo")
    c_badge: int = Field(..., alias="cBadge")
    ch_no: int = Field(..., alias="chNo")
    ch_photo_path: str = Field(..., alias="chPhotoPath")
    ch_title: str = Field(..., alias="chTitle")
    ch_type: int = Field(..., alias="chType")
    create_time: int = Field(..., alias="createTime")
    domain_id: int = Field(..., alias="domain_id")
    extras: str
    from_photo_hash: str = Field(..., alias="fromPhotoHash")
    from_user_no: int = Field(..., alias="fromUserNo")
    h_badge: int = Field(..., alias="hBadge")
    loc_args0: str = Field(..., alias="loc-args0")
    loc_args1: str = Field(..., alias="loc-args1")
    loc_key: str = Field(..., alias="loc-key")
    m_badge: int = Field(..., alias="mBadge")
    message_no: int = Field(..., alias="messageNo")
    n_type: int = Field(..., alias="nType")
    notification_id: str = Field(..., alias="notification-id")
    ocn: int
    s_type: int = Field(..., alias="sType")
    token: str
    user_no: int = Field(..., alias="userNo")
    wpa_badge: int = Field(..., alias="wpaBadge")

    class Config:
        populate_by_name = True
