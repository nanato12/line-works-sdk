import asyncio
from typing import Any, Union

import pytest
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK
from websockets.frames import Close

from line_works.mqtt import client as client_module
from line_works.mqtt.client import MQTTClient
from line_works.mqtt.enums.packet_type import PacketType
from line_works.mqtt.exceptions import (
    MQTTConnectionLost,
    MQTTConnectionRefused,
)
from line_works.mqtt.models.packet import MQTTPacket
from line_works.tracer import LineWorksTracer
from tests.conftest import (
    CONNACK_OK,
    CONNACK_REFUSED,
    PINGRESP,
    build_publish,
    message_payload,
)


class FakeWorks:
    cookie_str = "a=b"

    def ensure_login(self) -> bool:
        return False


class _NoSocketTransport:
    def get_extra_info(self, name: str) -> None:
        return None


class FakeWebSocket:
    """サーバからの受信をキューで模倣する WebSocket"""

    def __init__(self) -> None:
        self.incoming: asyncio.Queue[Union[bytes, str, BaseException]] = (
            asyncio.Queue()
        )
        self.sent: list[Union[bytes, str]] = []
        self.closed = False
        self.transport = _NoSocketTransport()

    def push(self, *messages: Union[bytes, str, BaseException]) -> None:
        for m in messages:
            self.incoming.put_nowait(m)

    async def recv(self) -> Union[bytes, str]:
        if self.closed:
            raise ConnectionClosedOK(Close(1000, ""), None)
        item = await self.incoming.get()
        if isinstance(item, BaseException):
            raise item
        return item

    async def send(self, message: Union[bytes, str]) -> None:
        self.sent.append(message)

    async def close(self) -> None:
        self.closed = True
        self.incoming.put_nowait(ConnectionClosedOK(Close(1000, ""), None))

    def sent_binary(self) -> list[bytes]:
        return [m for m in self.sent if isinstance(m, bytes)]


@pytest.fixture
def ws(monkeypatch: pytest.MonkeyPatch) -> FakeWebSocket:
    fake = FakeWebSocket()

    async def fake_connect(*args: Any, **kwargs: Any) -> FakeWebSocket:
        return fake

    monkeypatch.setattr(client_module.websockets, "connect", fake_connect)
    return fake


def make_client(**overrides: Any) -> MQTTClient:
    fields: dict[str, Any] = {
        "works": FakeWorks(),
        "keepalive_interval": 1000.0,
        "idle_timeout": 5.0,
        "dedupe_cache_size": 1000,
    }
    fields.update(overrides)
    client: MQTTClient = MQTTClient.model_construct(**fields)
    return client


async def run_until(client: MQTTClient, ws: FakeWebSocket) -> None:
    """connect() を起動し、disconnect() で終了させる"""
    task = asyncio.create_task(client.connect())
    await asyncio.sleep(0.05)
    await client.disconnect()
    await task


@pytest.mark.asyncio
async def test_connect_sends_connect_and_keepalive(ws: FakeWebSocket) -> None:
    client = make_client()
    ws.push(CONNACK_OK)
    await run_until(client, ws)
    binary = ws.sent_binary()
    assert (binary[0][0] & 0xF0) >> 4 == PacketType.CONNECT.value
    assert b"\xc0\x00" in binary  # PINGREQ
    assert "keepalive" in ws.sent
    assert client.is_connected is False  # 切断後


@pytest.mark.asyncio
async def test_connack_sets_connected(ws: FakeWebSocket) -> None:
    client = make_client()
    ws.push(CONNACK_OK)
    task = asyncio.create_task(client.connect())
    await asyncio.sleep(0.05)
    assert client.is_connected is True
    assert client.last_received_at is not None
    await client.disconnect()
    await task


@pytest.mark.asyncio
async def test_connack_refused(ws: FakeWebSocket) -> None:
    client = make_client()
    ws.push(CONNACK_REFUSED)
    with pytest.raises(MQTTConnectionRefused):
        await client.connect()


@pytest.mark.asyncio
async def test_publish_is_acked_and_dispatched(ws: FakeWebSocket) -> None:
    client = make_client()
    received: list[MQTTPacket] = []

    def on_publish(w: Any, p: MQTTPacket) -> None:
        received.append(p)

    client.add_trace_func(PacketType.PUBLISH, on_publish)
    ws.push(CONNACK_OK, build_publish(message_payload(), packet_id=9))
    await run_until(client, ws)
    assert b"\x40\x02\x00\x09" in ws.sent_binary()
    assert len(received) == 1
    assert received[0].publish_payload["loc-args1"] == "hello"


@pytest.mark.asyncio
async def test_async_trace_func(ws: FakeWebSocket) -> None:
    client = make_client()
    received: list[str] = []

    async def on_publish(w: Any, p: MQTTPacket) -> None:
        await asyncio.sleep(0)
        received.append(p.publish_payload["loc-args1"])

    client.add_trace_func(PacketType.PUBLISH, on_publish)
    ws.push(CONNACK_OK, build_publish(message_payload(text="async")))
    await run_until(client, ws)
    assert received == ["async"]


@pytest.mark.asyncio
async def test_trace_func_error_does_not_kill_connection(
    ws: FakeWebSocket,
) -> None:
    client = make_client()
    calls = 0

    def on_publish(w: Any, p: MQTTPacket) -> None:
        nonlocal calls
        calls += 1
        raise RuntimeError("boom")

    client.add_trace_func(PacketType.PUBLISH, on_publish)
    ws.push(
        CONNACK_OK,
        build_publish(message_payload("a"), packet_id=1),
        build_publish(message_payload("b"), packet_id=2),
    )
    await run_until(client, ws)
    assert calls == 2


@pytest.mark.asyncio
async def test_duplicate_publish_is_dropped(ws: FakeWebSocket) -> None:
    client = make_client()
    received: list[MQTTPacket] = []
    client.add_trace_func(PacketType.PUBLISH, lambda w, p: received.append(p))
    packet = build_publish(message_payload("same"), packet_id=5)
    ws.push(CONNACK_OK, packet, packet, build_publish(message_payload("x")))
    await run_until(client, ws)
    assert len(received) == 2
    # 再送にも PUBACK は返す
    assert ws.sent_binary().count(b"\x40\x02\x00\x05") == 2


@pytest.mark.asyncio
async def test_dedupe_cache_is_bounded(ws: FakeWebSocket) -> None:
    client = make_client(dedupe_cache_size=2)
    received: list[MQTTPacket] = []
    client.add_trace_func(PacketType.PUBLISH, lambda w, p: received.append(p))
    ws.push(
        CONNACK_OK,
        build_publish(message_payload("1")),
        build_publish(message_payload("2")),
        build_publish(message_payload("3")),
        build_publish(message_payload("1")),  # 追い出されているので再通知
    )
    await run_until(client, ws)
    assert len(received) == 4


@pytest.mark.asyncio
async def test_publish_split_across_frames(ws: FakeWebSocket) -> None:
    client = make_client()
    received: list[MQTTPacket] = []
    client.add_trace_func(PacketType.PUBLISH, lambda w, p: received.append(p))
    packet = build_publish(message_payload(text="x" * 500))
    ws.push(CONNACK_OK, packet[:100], packet[100:300], packet[300:] + PINGRESP)
    await run_until(client, ws)
    assert len(received) == 1
    assert received[0].publish_payload["loc-args1"] == "x" * 500


@pytest.mark.asyncio
async def test_qos2_flow(ws: FakeWebSocket) -> None:
    client = make_client()
    ws.push(
        CONNACK_OK,
        build_publish(message_payload(), qos=2, packet_id=3),
        b"\x62\x02\x00\x03",  # PUBREL
    )
    await run_until(client, ws)
    binary = ws.sent_binary()
    assert b"\x50\x02\x00\x03" in binary  # PUBREC
    assert b"\x70\x02\x00\x03" in binary  # PUBCOMP


@pytest.mark.asyncio
async def test_unknown_notification_type_is_still_dispatched(
    ws: FakeWebSocket,
) -> None:
    client = make_client()
    received: list[MQTTPacket] = []
    client.add_trace_func(PacketType.PUBLISH, lambda w, p: received.append(p))
    ws.push(CONNACK_OK, build_publish({"nType": 27}))
    await run_until(client, ws)
    assert len(received) == 1


@pytest.mark.asyncio
async def test_idle_timeout_disabled_by_default(ws: FakeWebSocket) -> None:
    client = make_client(idle_timeout=None)
    ws.push(CONNACK_OK)
    task = asyncio.create_task(client.connect())
    await asyncio.sleep(0.3)
    assert not task.done()
    await client.disconnect()
    await task


@pytest.mark.asyncio
async def test_idle_timeout_raises(ws: FakeWebSocket) -> None:
    client = make_client(idle_timeout=0.1)
    ws.push(CONNACK_OK)
    with pytest.raises(MQTTConnectionLost):
        await client.connect()
    assert ws.closed is True
    assert client.is_connected is False


@pytest.mark.asyncio
async def test_server_disconnect_packet_raises(ws: FakeWebSocket) -> None:
    client = make_client()
    ws.push(CONNACK_OK, b"\xe0\x00")
    with pytest.raises(MQTTConnectionLost):
        await client.connect()


@pytest.mark.asyncio
async def test_server_close_raises(ws: FakeWebSocket) -> None:
    client = make_client()
    ws.push(CONNACK_OK, ConnectionClosedError(None, None))
    with pytest.raises(ConnectionClosedError):
        await client.connect()


@pytest.mark.asyncio
async def test_out_of_sync_stream_raises(ws: FakeWebSocket) -> None:
    client = make_client()
    ws.push(CONNACK_OK, b"\x00\x00")
    with pytest.raises(MQTTConnectionLost):
        await client.connect()


@pytest.mark.asyncio
async def test_connect_can_be_cancelled(ws: FakeWebSocket) -> None:
    client = make_client()
    ws.push(CONNACK_OK)
    task = asyncio.create_task(client.connect())
    await asyncio.sleep(0.05)
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
    assert ws.closed is True


@pytest.mark.asyncio
async def test_tracer_reconnects(monkeypatch: pytest.MonkeyPatch) -> None:
    # 1 回目: 無通信タイムアウト、2 回目: サーバ切断、3 回目: 自分で切断
    sockets = [FakeWebSocket(), FakeWebSocket(), FakeWebSocket()]
    sockets[0].push(CONNACK_OK)
    sockets[1].push(CONNACK_OK, ConnectionClosedError(None, None))
    sockets[2].push(CONNACK_OK)
    remaining = list(sockets)

    async def fake_connect(*args: Any, **kwargs: Any) -> FakeWebSocket:
        return remaining.pop(0)

    monkeypatch.setattr(client_module.websockets, "connect", fake_connect)
    monkeypatch.setattr(client_module.config, "STABLE_CONNECTION_SEC", 0.0)

    tracer = LineWorksTracer.model_construct(
        works=FakeWorks(),
        keepalive_interval=1000.0,
        idle_timeout=0.1,
        dedupe_cache_size=10,
        reconnect_backoff_max=0.01,
    )
    connects = 0

    def on_connack(w: Any, p: MQTTPacket) -> None:
        nonlocal connects
        connects += 1
        if connects == 3:
            asyncio.get_running_loop().create_task(tracer.disconnect())

    tracer.add_trace_func(PacketType.CONNACK, on_connack)
    await asyncio.wait_for(tracer.run(), timeout=5)
    assert connects == 3
    assert remaining == []
    assert all(s.closed for s in sockets)


@pytest.mark.asyncio
async def test_tracer_without_reconnect(ws: FakeWebSocket) -> None:
    tracer = LineWorksTracer.model_construct(
        works=FakeWorks(),
        keepalive_interval=1000.0,
        idle_timeout=0.1,
        dedupe_cache_size=10,
        reconnect_backoff_max=1.0,
    )
    ws.push(CONNACK_OK)
    await asyncio.wait_for(tracer.run(reconnect=False), timeout=2)
