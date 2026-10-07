import uuid

from line_works.mqtt.config import KEEP_ALIVE_INTERVAL_SEC
from line_works.mqtt.enums.packet_type import PacketType


def encode_remaining_length(length: int) -> bytes:
    """MQTT 3.1.1 §2.2.3 の可変長エンコード"""
    if length < 0 or length > 268_435_455:
        raise ValueError(f"Remaining length out of range: {length}")
    encoded = bytearray()
    while True:
        byte = length % 128
        length //= 128
        if length > 0:
            byte |= 0x80  # continuation bit
        encoded.append(byte)
        if length == 0:
            return bytes(encoded)


class ConnectionPacket(bytearray):
    def __append_utf8_bytes(self, b: bytes) -> None:
        self.extend(len(b).to_bytes(2, byteorder="big"))
        self.extend(b)

    def generate(self) -> bytes:
        client_id = str(uuid.uuid4()).replace("-", "")[:22]
        client_id_bytes = client_id.encode("utf-8")
        username_bytes = "dummy".encode("utf-8")
        password_bytes = client_id_bytes
        protocol_name_bytes = "MQTT".encode("utf-8")

        remaining_length = (
            2  # Protocol name
            + len(protocol_name_bytes)
            + 1  # Protocol level
            + 1  # Connect flags
            + 2  # Keep alive
            + 2  # Client ID
            + len(client_id_bytes)
            + 2  # User name
            + len(username_bytes)
            + 2  # Password
            + len(password_bytes)
        )

        packet_type = PacketType.CONNECT.value << 4
        self.append(packet_type)
        self.extend(encode_remaining_length(remaining_length))

        self.__append_utf8_bytes(protocol_name_bytes)
        self.append(0x04)  # Protocol level: MQTT v3.1.1
        self.append(0xC6)  # Connect flags: 11000110
        self.extend(KEEP_ALIVE_INTERVAL_SEC.to_bytes(2, byteorder="big"))

        self.__append_utf8_bytes(client_id_bytes)
        self.__append_utf8_bytes(username_bytes)
        self.__append_utf8_bytes(password_bytes)

        return bytes(self)


class PacketIdPacket:
    """Packet Identifier だけを持つ制御パケット (PUBACK など)"""

    packet_type: PacketType
    flags: int = 0

    def __init__(self, packet_id: int) -> None:
        if not 0 < packet_id <= 0xFFFF:
            raise ValueError(f"Invalid packet id: {packet_id}")
        self.packet_id = packet_id

    def generate(self) -> bytes:
        header = (self.packet_type.value << 4) | self.flags
        return (
            bytes([header])
            + encode_remaining_length(2)
            + self.packet_id.to_bytes(2, byteorder="big")
        )


class PubAckPacket(PacketIdPacket):
    """QoS 1 の PUBLISH に対する応答"""

    packet_type = PacketType.PUBACK


class PubRecPacket(PacketIdPacket):
    """QoS 2 の PUBLISH に対する応答 (Part 1)"""

    packet_type = PacketType.PUBREC


class PubRelPacket(PacketIdPacket):
    """QoS 2 の PUBREC に対する応答 (Part 2)。flags は 0b0010 固定"""

    packet_type = PacketType.PUBREL
    flags = 0x02


class PubCompPacket(PacketIdPacket):
    """QoS 2 の PUBREL に対する応答 (Part 3)"""

    packet_type = PacketType.PUBCOMP


class EmptyPacket:
    """ペイロードを持たない制御パケット (PINGREQ, DISCONNECT)"""

    packet_type: PacketType

    def generate(self) -> bytes:
        return bytes([self.packet_type.value << 4, 0x00])


class PingReqPacket(EmptyPacket):
    packet_type = PacketType.PINGREQ


class DisconnectPacket(EmptyPacket):
    packet_type = PacketType.DISCONNECT
