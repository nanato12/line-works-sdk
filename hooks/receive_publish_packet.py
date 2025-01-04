from line_works.client import LineWorks
from line_works.mqtt.models.packet import MQTTPacket


def receive_publish_packet(w: LineWorks, p: MQTTPacket) -> None:
    m = p.message

    if not m.channel_no:
        return

    if m.loc_args1 == "test":
        r = w.send_message(m.channel_no, "ok")
        print(f"{r=}")
