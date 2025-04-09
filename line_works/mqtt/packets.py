import uuid

from line_works.mqtt.config import KEEP_ALIVE_INTERVAL_SEC
from line_works.mqtt.enums.packet_type import PacketType


class ConnectionPacket(bytearray):
    def __append_utf8_bytes(self, b: bytes) -> None:
        self.extend(len(b).to_bytes(2, byteorder="big"))
        self.extend(b)

    def __append_remaining_length(self, length: int) -> None:
        while True:
            byte = length % 128
            length //= 128
            if length > 0:
                byte |= 0x80  # Set the continuation bit
            self.append(byte)
            if length == 0:
                break

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
        self.__append_remaining_length(remaining_length)

        self.__append_utf8_bytes(protocol_name_bytes)
        self.append(0x04)  # Protocol level: MQTT v3.1.1
        self.append(0xC6)  # Connect flags: 11000110
        self.extend(KEEP_ALIVE_INTERVAL_SEC.to_bytes(2, byteorder="big"))

        self.__append_utf8_bytes(client_id_bytes)
        self.__append_utf8_bytes(username_bytes)
        self.__append_utf8_bytes(password_bytes)

        return bytes(self)
