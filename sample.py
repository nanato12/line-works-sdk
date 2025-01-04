from line_works.client import LineWorks
from line_works.mqtt.enums.packet_type import PacketType
from line_works.mqtt.models.packet import MQTTPacket
from line_works.tracer import LineWorksTracer


def receive_publish_packet(w: LineWorks, p: MQTTPacket) -> None:
    m = p.message

    if not m.channel_no:
        return

    if m.loc_args1 == "test":
        r = w.send_message(m.channel_no, "ok")
        print(f"{r=}")


WORKS_ID = "YOUR WORKS ID"
PASSWORD = "YOUR WORKS PASSWORD"

works = LineWorks(works_id=WORKS_ID, password=PASSWORD)

my_info = works.get_my_info()
print(f"{my_info=}")

tracer = LineWorksTracer(works=works)
tracer.add_trace_func(PacketType.PUBLISH, receive_publish_packet)
tracer.trace()
