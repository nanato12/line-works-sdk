from typing import Type

from line_works.mqtt.enums.notification_type import NotificationType
from line_works.mqtt.models.payload.badge import BadgePayload
from line_works.mqtt.models.payload.message import (
    MessagePayload,
)
from line_works.mqtt.models.payload.service import ServicePayload

PayloadTypes = MessagePayload | ServicePayload | BadgePayload

NOTIFICATION_TYPE_MODEL_MAPPING: dict[int, Type[PayloadTypes]] = {
    NotificationType.NOTIFICATION_MESSAGE.value: MessagePayload,
    NotificationType.NOTIFICATION_STICKER.value: MessagePayload,
    NotificationType.NOTIFICATION_IMAGE.value: MessagePayload,
    NotificationType.NOTIFICATION_LOCATION.value: MessagePayload,
    NotificationType.NOTIFICATION_BADGE.value: BadgePayload,
    NotificationType.NOTIFICATION_SERVICE.value: ServicePayload,
    NotificationType.NOTIFICATION_FILE.value: MessagePayload,
}
