import json
import struct
from typing import Any, Optional, Self

from pydantic import BaseModel, Field

from line_works.mqtt.enums.packet_type import PacketType
from line_works.mqtt.exceptions import PacketParseException
from line_works.mqtt.models.payload import (
    NOTIFICATION_TYPE_MODEL_MAPPING,
    PayloadTypes,
)


class MQTTPacket(BaseModel):
    type: PacketType
    flags: int
    remaining_length: int
    raw_payload: Optional[bytes]
    raw_packet: bytes = Field(repr=False)

    def validate_publish_payload(self) -> None:
        if self.type != PacketType.PUBLISH:
            raise PacketParseException(
                f"Expected packet type {PacketType.PUBLISH}, "
                f"but got {self.type}."
            )

    @property
    def topic_length(self) -> int:
        self.validate_publish_payload()
        if not self.raw_payload:
            raise PacketParseException("Payload is missing or invalid.")

        topic_length: int = struct.unpack("!H", self.raw_payload[0:2])[0]
        return topic_length

    @property
    def topic_name(self) -> str:
        self.validate_publish_payload()
        if not self.raw_payload:
            raise PacketParseException("Payload is missing or invalid.")

        topic: str = self.raw_payload[2 : 2 + self.topic_length].decode(
            "utf-8"
        )
        return topic

    @property
    def publish_payload(self) -> dict[str, Any]:
        self.validate_publish_payload()
        if not self.raw_payload:
            raise PacketParseException("Payload is missing or invalid.")

        pos = 2 + self.topic_length

        qos = (self.flags & 0x06) >> 1
        if qos > 0:
            if len(self.raw_payload) < pos + 2:
                raise PacketParseException(
                    "Packet too short for QoS > 0: "
                    f"expected at least {pos + 2} bytes, "
                    f"but got {len(self.raw_payload)} bytes. "
                    f"raw_payload: {self.raw_payload.hex()}"
                )
            pos += 2

        payload = self.raw_payload[pos:].decode("utf-8")
        if payload:
            j: dict[str, Any] = json.loads(payload)
            return j

        return {}

    @property
    def payload(self) -> PayloadTypes:
        p = self.publish_payload
        if not (n_type := p.get("nType")):
            raise PacketParseException(f"invalid payload: {p}")

        if not (p_model := NOTIFICATION_TYPE_MODEL_MAPPING.get(n_type)):
            raise PacketParseException(f"invalid notification type: {n_type}")

        return p_model.model_validate(self.publish_payload)  # type: ignore

    @classmethod
    def parse_from_bytes(cls, data: bytes) -> Self:
        if (data_length := len(data)) < 2:
            raise PacketParseException(
                f"Data size is too small: {data_length} bytes"
            )

        packet_type = (data[0] & 0xF0) >> 4
        flags = data[0] & 0x0F

        remaining_length = 0
        multiplier = 1
        pos = 1

        while pos < len(data):
            byte = data[pos]
            remaining_length += (byte & 0x7F) * multiplier
            multiplier *= 128
            pos += 1

            if byte & 0x80 == 0:
                break

        raw_payload = (
            data[pos : pos + remaining_length]
            if remaining_length > 0
            else None
        )

        return cls(
            type=PacketType(packet_type),
            flags=flags,
            remaining_length=remaining_length,
            raw_payload=raw_payload,
            raw_packet=data,
        )
