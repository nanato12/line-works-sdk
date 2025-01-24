from line_works.client import LineWorks
from line_works.logger import get_file_path_logger
from line_works.mqtt.enums.notification_type import NotificationType
from line_works.mqtt.models.packet import MQTTPacket
from line_works.mqtt.models.payload.message import MessagePayload

logger = get_file_path_logger(__name__)


def receive_publish_packet(w: LineWorks, p: MQTTPacket) -> None:
    payload = p.payload

    if not isinstance(payload, MessagePayload):
        return

    if not payload.channel_no:
        return

    logger.info(f"{payload!r}")

    if payload.loc_args1 == "test":
        w.send_text_message(payload.channel_no, "ok")

    elif payload.loc_args1 == "/msg":
        w.send_text_message(payload.channel_no, f"{payload!r}")

    if payload.notification_type == NotificationType.NOTIFICATION_STICKER:
        w.send_text_message(payload.channel_no, "スタンプ")
        w.send_text_message(payload.channel_no, f"{payload.sticker=}")

        w.send_sticker_message(payload.channel_no, payload.sticker)
