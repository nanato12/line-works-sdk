import pytest

from line_works.mqtt.enums.packet_type import PacketType
from line_works.mqtt.exceptions import PacketParseException
from line_works.mqtt.models.packet import MQTTPacket
from line_works.mqtt.models.payload.message import MessagePayload
from line_works.mqtt.packets import (
    DisconnectPacket,
    PingReqPacket,
    PubAckPacket,
    PubCompPacket,
    PubRecPacket,
    PubRelPacket,
    encode_remaining_length,
)
from tests.conftest import CONNACK_OK, build_publish, message_payload


def test_encode_remaining_length() -> None:
    assert encode_remaining_length(0) == b"\x00"
    assert encode_remaining_length(127) == b"\x7f"
    assert encode_remaining_length(128) == b"\x80\x01"
    assert encode_remaining_length(16_383) == b"\xff\x7f"
    assert encode_remaining_length(268_435_455) == b"\xff\xff\xff\x7f"
    with pytest.raises(ValueError):
        encode_remaining_length(268_435_456)


def test_ack_packets() -> None:
    assert PubAckPacket(0x1234).generate() == b"\x40\x02\x12\x34"
    assert PubRecPacket(1).generate() == b"\x50\x02\x00\x01"
    assert PubRelPacket(1).generate() == b"\x62\x02\x00\x01"
    assert PubCompPacket(1).generate() == b"\x70\x02\x00\x01"
    assert PingReqPacket().generate() == b"\xc0\x00"
    assert DisconnectPacket().generate() == b"\xe0\x00"
    with pytest.raises(ValueError):
        PubAckPacket(0)


def test_parse_publish_qos1() -> None:
    raw = build_publish(message_payload(), qos=1, packet_id=42)
    packet = MQTTPacket.parse_from_bytes(raw)
    assert packet.type == PacketType.PUBLISH
    assert packet.qos == 1
    assert packet.dup is False
    assert packet.packet_id == 42
    assert packet.topic_name == "notification"
    assert packet.publish_payload["loc-args1"] == "hello"
    payload = packet.payload
    assert isinstance(payload, MessagePayload)
    assert payload.channel_no == 3
    assert payload.unique_id == "k_n1"


def test_parse_publish_qos0_has_no_packet_id() -> None:
    packet = MQTTPacket.parse_from_bytes(build_publish({"nType": 1}, qos=0))
    assert packet.packet_id is None
    assert packet.publish_payload == {"nType": 1}


def test_parse_publish_dup_flag() -> None:
    packet = MQTTPacket.parse_from_bytes(build_publish({}, dup=True))
    assert packet.dup is True


def test_parse_ack_packet_id() -> None:
    packet = MQTTPacket.parse_from_bytes(b"\x62\x02\x00\x07")
    assert packet.type == PacketType.PUBREL
    assert packet.packet_id == 7
    assert MQTTPacket.parse_from_bytes(CONNACK_OK).packet_id is None


def test_parse_large_payload() -> None:
    raw = build_publish({"text": "x" * 20_000})
    packet = MQTTPacket.parse_from_bytes(raw)
    assert packet.remaining_length > 16_383
    assert len(packet.publish_payload["text"]) == 20_000


def test_trailing_bytes_are_ignored() -> None:
    packet = MQTTPacket.parse_from_bytes(CONNACK_OK + b"junk")
    assert packet.raw_packet == CONNACK_OK


def test_truncated_packet_raises() -> None:
    raw = build_publish(message_payload())
    with pytest.raises(PacketParseException):
        MQTTPacket.parse_from_bytes(raw[:-1])
    with pytest.raises(PacketParseException):
        MQTTPacket.parse_from_bytes(b"\x30")
    with pytest.raises(PacketParseException):
        MQTTPacket.parse_from_bytes(b"\x00\x00")


def test_invalid_payload_raises_parse_exception() -> None:
    packet = MQTTPacket.parse_from_bytes(build_publish(b"not json"))
    with pytest.raises(PacketParseException):
        packet.publish_payload
    packet = MQTTPacket.parse_from_bytes(build_publish(b"\xff\xfe"))
    with pytest.raises(PacketParseException):
        packet.publish_payload
    packet = MQTTPacket.parse_from_bytes(build_publish({"nType": 27}))
    with pytest.raises(PacketParseException):
        packet.payload
