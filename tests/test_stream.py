import pytest

from line_works.mqtt.exceptions import PacketParseException
from line_works.mqtt.stream import MQTTStreamParser
from tests.conftest import CONNACK_OK, PINGRESP, build_publish


def test_single_packet() -> None:
    parser = MQTTStreamParser()
    assert parser.feed(CONNACK_OK) == [CONNACK_OK]
    assert parser.pending_bytes == 0


def test_multiple_packets_in_one_frame() -> None:
    parser = MQTTStreamParser()
    publish = build_publish({"a": 1})
    assert parser.feed(CONNACK_OK + publish + PINGRESP) == [
        CONNACK_OK,
        publish,
        PINGRESP,
    ]


def test_packet_split_across_frames() -> None:
    parser = MQTTStreamParser()
    publish = build_publish({"text": "x" * 300})  # 2 バイトの remaining length
    assert len(publish) > 128

    # ヘッダの途中で切れる
    assert parser.feed(publish[:1]) == []
    assert parser.feed(publish[1:2]) == []
    # ペイロードの途中で切れる
    assert parser.feed(publish[2:100]) == []
    assert parser.pending_bytes == 100
    # 残りと次のパケットの先頭が一緒に届く
    assert parser.feed(publish[100:] + PINGRESP[:1]) == [publish]
    assert parser.feed(PINGRESP[1:]) == [PINGRESP]
    assert parser.pending_bytes == 0


def test_reserved_packet_type_resets_buffer() -> None:
    parser = MQTTStreamParser()
    with pytest.raises(PacketParseException):
        parser.feed(b"\x00\x00")
    assert parser.pending_bytes == 0


def test_malformed_remaining_length_resets_buffer() -> None:
    parser = MQTTStreamParser()
    with pytest.raises(PacketParseException):
        parser.feed(b"\x30\xff\xff\xff\xff\xff")
    assert parser.pending_bytes == 0


def test_reset() -> None:
    parser = MQTTStreamParser()
    parser.feed(b"\x30\x10abc")
    assert parser.pending_bytes == 5
    parser.reset()
    assert parser.pending_bytes == 0
