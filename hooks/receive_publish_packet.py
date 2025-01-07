from line_works.client import LineWorks
from line_works.mqtt.models.packet import MQTTPacket
from line_works.mqtt.models.payload.message import MessagePayload


def receive_publish_packet(w: LineWorks, p: MQTTPacket) -> None:
    payload = p.payload

    if not isinstance(payload, MessagePayload):
        return

    if not payload.channel_no:
        return

    if payload.loc_args1 == "test":
        r = w.send_message(payload.channel_no, "ok")
        print(f"{r=}")
