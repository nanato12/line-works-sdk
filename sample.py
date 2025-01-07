from line_works.client import LineWorks
from line_works.mqtt.enums.packet_type import PacketType
from line_works.mqtt.models.packet import MQTTPacket
from line_works.mqtt.models.payload.message import MessagePayload
from line_works.tracer import LineWorksTracer


def receive_publish_packet(w: LineWorks, p: MQTTPacket) -> None:
    payload = p.payload

    if not isinstance(payload, MessagePayload):
        return

    if not payload.channel_no:
        return

    print(f"{payload!r}")

    if payload.loc_args1 == "test":
        w.send_message(payload.channel_no, "ok")

    elif payload.loc_args1 == "/msg":
        w.send_message(payload.channel_no, f"{payload!r}")


WORKS_ID = "YOUR WORKS ID"
PASSWORD = "YOUR WORKS PASSWORD"

works = LineWorks(works_id=WORKS_ID, password=PASSWORD)

my_info = works.get_my_info()
print(f"{my_info=}")

tracer = LineWorksTracer(works=works)
tracer.add_trace_func(PacketType.PUBLISH, receive_publish_packet)
tracer.trace()
