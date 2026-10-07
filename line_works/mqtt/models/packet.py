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

# Variable Header の先頭 2 バイトが Packet Identifier のパケット
_PACKET_ID_ONLY_TYPES = frozenset(
    {
        PacketType.PUBACK,
        PacketType.PUBREC,
        PacketType.PUBREL,
        PacketType.PUBCOMP,
        PacketType.SUBACK,
        PacketType.UNSUBACK,
    }
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
    def qos(self) -> int:
        """PUBLISH の QoS レベル (0-2)"""
        return (self.flags & 0x06) >> 1

    @property
    def dup(self) -> bool:
        """PUBLISH の再送フラグ"""
        return bool(self.flags & 0x08)

    @property
    def retain(self) -> bool:
        return bool(self.flags & 0x01)

    @property
    def topic_length(self) -> int:
        self.validate_publish_payload()
        if not self.raw_payload or len(self.raw_payload) < 2:
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
    def packet_id(self) -> Optional[int]:
        """Packet Identifier。持たないパケット (QoS 0 の PUBLISH 等) は None"""
        if self.type == PacketType.PUBLISH:
            if self.qos == 0:
                return None
            pos = 2 + self.topic_length
        elif self.type in _PACKET_ID_ONLY_TYPES:
            pos = 0
        else:
            return None

        if not self.raw_payload or len(self.raw_payload) < pos + 2:
            raise PacketParseException(
                f"Packet too short for packet id: "
                f"expected at least {pos + 2} bytes, "
                f"but got {len(self.raw_payload or b'')} bytes."
            )
        packet_id: int = struct.unpack("!H", self.raw_payload[pos : pos + 2])[
            0
        ]
        return packet_id

    @property
    def publish_payload(self) -> dict[str, Any]:
        self.validate_publish_payload()
        if not self.raw_payload:
            raise PacketParseException("Payload is missing or invalid.")

        pos = 2 + self.topic_length

        if self.qos > 0:
            if len(self.raw_payload) < pos + 2:
                raise PacketParseException(
                    "Packet too short for QoS > 0: "
                    f"expected at least {pos + 2} bytes, "
                    f"but got {len(self.raw_payload)} bytes. "
                    f"raw_payload: {self.raw_payload.hex()}"
                )
            pos += 2

        try:
            payload = self.raw_payload[pos:].decode("utf-8")
        except UnicodeDecodeError as e:
            raise PacketParseException(f"Payload is not UTF-8: {e}") from e

        if not payload:
            return {}

        try:
            j = json.loads(payload)
        except json.JSONDecodeError as e:
            raise PacketParseException(f"Payload is not JSON: {e}") from e
        if not isinstance(j, dict):
            raise PacketParseException(
                f"Payload is not a JSON object: {payload[:80]}"
            )
        return j

    @property
    def payload(self) -> PayloadTypes:
        p = self.publish_payload
        if not (n_type := p.get("nType")):
            raise PacketParseException(f"invalid payload: {p}")

        if not (p_model := NOTIFICATION_TYPE_MODEL_MAPPING.get(n_type)):
            raise PacketParseException(f"invalid notification type: {n_type}")

        return p_model.model_validate(p)  # type: ignore

    @classmethod
    def parse_from_bytes(cls, data: bytes) -> Self:
        """1 つの完全な制御パケットをパースする。

        末尾に余分なデータがあっても無視する。複数パケットが連結された
        ストリームは `MQTTStreamParser` で分割してから渡すこと。
        """
        if (data_length := len(data)) < 2:
            raise PacketParseException(
                f"Data size is too small: {data_length} bytes"
            )

        try:
            packet_type = PacketType((data[0] & 0xF0) >> 4)
        except ValueError as e:
            raise PacketParseException(
                f"Unknown packet type: {(data[0] & 0xF0) >> 4}"
            ) from e
        flags = data[0] & 0x0F

        remaining_length = 0
        multiplier = 1
        pos = 1

        while True:
            if pos >= len(data):
                raise PacketParseException("Truncated remaining length")
            byte = data[pos]
            remaining_length += (byte & 0x7F) * multiplier
            multiplier *= 128
            pos += 1

            if byte & 0x80 == 0:
                break
            if pos > 4:
                raise PacketParseException("Malformed remaining length")

        if len(data) < pos + remaining_length:
            raise PacketParseException(
                f"Truncated packet: expected {pos + remaining_length} bytes, "
                f"but got {len(data)} bytes"
            )

        raw_payload = (
            data[pos : pos + remaining_length]
            if remaining_length > 0
            else None
        )

        return cls(
            type=packet_type,
            flags=flags,
            remaining_length=remaining_length,
            raw_payload=raw_payload,
            raw_packet=data[: pos + remaining_length],
        )
