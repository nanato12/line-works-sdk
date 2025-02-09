import json
from typing import Optional

from pydantic import Field

from line_works.exceptions import LogicException
from line_works.mqtt.enums.notification_type import NotificationType
from line_works.mqtt.models.payload.badge import BadgePayload
from line_works.openapi.talk.models.sticker import Sticker


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
    domain_id: Optional[int] = Field(default=None)
    loc_args0: str = Field(default="")
    loc_args1: str = Field(default="")
    loc_key: str = Field(default="")
    s_type: Optional[int] = Field(default=None)
    ocn: Optional[int] = Field(default=None)
    a_badge: Optional[int] = Field(default=None)
    c_badge: Optional[int] = Field(default=None)
    h_badge: Optional[int] = Field(default=None)
    m_badge: Optional[int] = Field(default=None)
    token: Optional[int] = Field(default=None)
    wpa_badge: Optional[int] = Field(default=None)
    user_no: Optional[int] = Field(default=None)
    badge: Optional[int] = Field(default=None)

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

    @property
    def video(self) -> dict:
        if self.notification_type == NotificationType.NOTIFICATION_VIDEO:
            return self.extras_dict
        raise LogicException(
            f"Invalid notification type: {self.notification_type}. "
            f"Expected {NotificationType.NOTIFICATION_VIDEO}."
        )

    @property
    def file(self) -> dict:
        if self.notification_type == NotificationType.NOTIFICATION_FILE:
            return self.extras_dict
        raise LogicException(
            f"Invalid notification type: {self.notification_type}. "
            f"Expected {NotificationType.NOTIFICATION_FILE}."
        )

    @property
    def location(self) -> dict:
        if self.notification_type == NotificationType.NOTIFICATION_LOCATION:
            return self.extras_dict
        raise LogicException(
            f"Invalid notification type: {self.notification_type}. "
            f"Expected {NotificationType.NOTIFICATION_LOCATION}."
        )

    @property
    def image(self) -> dict:
        if self.notification_type == NotificationType.NOTIFICATION_IMAGE:
            return {
                "channel_no": self.channel_no,
                "from_user_no": self.from_user_no,
                "from_photo_hash": self.from_photo_hash,
                "message_no": self.message_no,
                "notification_id": self.notification_id,
                **self.extras_dict
            }
        raise LogicException(
            f"Invalid notification type: {self.notification_type}. "
            f"Expected {NotificationType.NOTIFICATION_IMAGE}."
        )

    @property
    def emoji(self) -> dict:
        if self.notification_type == NotificationType.NOTIFICATION_EMOJI:
            return self.extras_dict
        raise LogicException(
            f"Invalid notification type: {self.notification_type}. "
            f"Expected {NotificationType.NOTIFICATION_EMOJI}."
        )

    @property
    def badge_info(self) -> dict:
        if self.notification_type == NotificationType.NOTIFICATION_BADGE:
            return self.extras_dict
        raise LogicException(
            f"Invalid notification type: {self.notification_type}. "
            f"Expected {NotificationType.NOTIFICATION_BADGE}."
        )

    @property
    def service(self) -> dict:
        if self.notification_type == NotificationType.NOTIFICATION_SERVICE:
            return self.extras_dict
        raise LogicException(
            f"Invalid notification type: {self.notification_type}. "
            f"Expected {NotificationType.NOTIFICATION_SERVICE}."
        )

    @property
    def message(self) -> dict:
        if self.notification_type == NotificationType.NOTIFICATION_MESSAGE:
            return self.extras_dict
        raise LogicException(
            f"Invalid notification type: {self.notification_type}. "
            f"Expected {NotificationType.NOTIFICATION_MESSAGE}."
        )

    @property
    def file_details(self) -> Optional[dict]:
        if self.notification_type == NotificationType.NOTIFICATION_FILE:
            return {
                "channel_no": self.channel_no,
                "channel_title": self.channel_title,
                "channel_type": self.channel_type,
                "channel_photo_path": self.channel_photo_path,
                "from_user_no": self.from_user_no,
                "from_photo_hash": self.from_photo_hash,
                "message_no": self.message_no,
                "create_time": self.create_time,
                "extras": self.extras_dict
            }
        return None

    @property
    def sender_info(self) -> Optional[dict]:
        if self.from_user_no:
            return {
                "user_no": self.from_user_no,
                "photo_hash": self.from_photo_hash,
                "bot_info": self.bot_info
            }
        return None

    @property
    def channel_info(self) -> Optional[dict]:
        if self.channel_no:
            return {
                "channel_no": self.channel_no,
                "channel_title": self.channel_title,
                "channel_type": self.channel_type,
                "channel_photo_path": self.channel_photo_path
            }
        return None

