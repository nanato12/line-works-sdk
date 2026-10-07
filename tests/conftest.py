import json
import struct
from typing import Any

import pytest

from line_works.mqtt.enums.notification_type import NotificationType
from line_works.mqtt.enums.packet_type import PacketType
from line_works.mqtt.packets import encode_remaining_length


def build_publish(
    payload: dict[str, Any] | bytes,
    *,
    qos: int = 1,
    packet_id: int = 1,
    topic: str = "notification",
    dup: bool = False,
) -> bytes:
    """テスト用の PUBLISH パケットを組み立てる"""
    body = (
        payload
        if isinstance(payload, bytes)
        else json.dumps(payload, separators=(",", ":")).encode()
    )
    variable = struct.pack("!H", len(topic)) + topic.encode()
    if qos > 0:
        variable += struct.pack("!H", packet_id)
    flags = (qos << 1) | (0x08 if dup else 0)
    header = bytes([(PacketType.PUBLISH.value << 4) | flags])
    return (
        header
        + encode_remaining_length(len(variable) + len(body))
        + (variable + body)
    )


def message_payload(
    notification_id: str = "n1", text: str = "hello"
) -> dict[str, Any]:
    return {
        "domain_id": 1,
        "sType": 1,
        "ocn": 1,
        "nType": NotificationType.NOTIFICATION_MESSAGE.value,
        "aBadge": 0,
        "badge": 0,
        "cBadge": 0,
        "hBadge": 0,
        "mBadge": 0,
        "token": "t",
        "wpaBadge": 0,
        "userNo": 2,
        "chNo": 3,
        "chType": 10,
        "fromUserNo": 4,
        "loc-key": "k",
        "loc-args1": text,
        "notification-id": notification_id,
    }


CONNACK_OK = bytes([PacketType.CONNACK.value << 4, 0x02, 0x00, 0x00])
CONNACK_REFUSED = bytes([PacketType.CONNACK.value << 4, 0x02, 0x00, 0x05])
PINGRESP = bytes([PacketType.PINGRESP.value << 4, 0x00])


@pytest.fixture
def connack_ok() -> bytes:
    return CONNACK_OK
