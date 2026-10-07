from line_works.mqtt.exceptions import PacketParseException

# MQTT 3.1.1 §2.2.3: Remaining Length は最大 4 バイト
MAX_REMAINING_LENGTH_BYTES = 4


class MQTTStreamParser:
    """バイトストリームから MQTT 制御パケットを 1 つずつ切り出す。

    MQTT over WebSocket では、1 つの WebSocket フレームに複数の制御パケットが
    含まれることも、1 つの制御パケットが複数のフレームに分割されることもある
    (MQTT 3.1.1 §6.1)。このクラスは受信したバイト列を蓄積し、完全な
    パケットだけを返す。
    """

    def __init__(self) -> None:
        self._buffer = bytearray()

    @property
    def pending_bytes(self) -> int:
        """まだパケットとして確定していないバイト数"""
        return len(self._buffer)

    def reset(self) -> None:
        self._buffer.clear()

    def feed(self, data: bytes) -> list[bytes]:
        """受信データを追加し、完成したパケットをすべて返す。

        Raises:
            PacketParseException: ストリームが壊れていて同期を回復できない。
                バッファは破棄されるため、呼び出し側は再接続すべき。
        """
        self._buffer.extend(data)
        packets: list[bytes] = []
        while (packet := self._pop_packet()) is not None:
            packets.append(packet)
        return packets

    def _pop_packet(self) -> bytes | None:
        buffer = self._buffer
        if len(buffer) < 2:
            return None

        packet_type = (buffer[0] & 0xF0) >> 4
        if packet_type in (0, 15):
            self.reset()
            raise PacketParseException(
                f"Reserved packet type {packet_type}; stream is out of sync"
            )

        remaining_length = 0
        multiplier = 1
        pos = 1
        while True:
            if pos >= len(buffer):
                return None
            byte = buffer[pos]
            remaining_length += (byte & 0x7F) * multiplier
            multiplier *= 128
            pos += 1
            if byte & 0x80 == 0:
                break
            if pos > MAX_REMAINING_LENGTH_BYTES:
                self.reset()
                raise PacketParseException(
                    "Malformed remaining length; stream is out of sync"
                )

        total_length = pos + remaining_length
        if len(buffer) < total_length:
            return None

        packet = bytes(buffer[:total_length])
        del buffer[:total_length]
        return packet
