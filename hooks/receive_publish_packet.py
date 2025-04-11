import json
from datetime import datetime

from line_works.client import LineWorks
from line_works.logger import get_file_path_logger
from line_works.mqtt.enums.notification_type import NotificationType
from line_works.mqtt.models.packet import MQTTPacket
from line_works.mqtt.models.payload.message import MessagePayload
from line_works.openapi.talk.models.flex_content import FlexContent
from line_works.openapi.talk.models.get_channel_members_request import (
    GetChannelMembersRequest,
)
from line_works.openapi.talk.models.leave_channel_request import (
    LeaveChannelRequest,
)

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

    elif payload.loc_args1 == "/leave":
        w.send_text_message(payload.channel_no, "bye")
        w.leave_channel(
            leave_channel_request=LeaveChannelRequest(
                channel_no_list=[payload.channel_no]
            )
        )

    elif payload.loc_args1 == "/id":
        w.send_text_message(payload.channel_no, str(payload.from_user_no))

    elif payload.loc_args1 == "/join_time":
        r = w.get_channel_members(
            get_channel_members_request=GetChannelMembersRequest(
                channel_no=payload.channel_no
            )
        )
        m = next(
            filter(lambda m: m.user_no == payload.from_user_no, r.members),
            None,
        )
        if m:
            j_time = datetime.fromtimestamp(int(m.join_time / 1000))
            w.send_text_message(payload.channel_no, f"{j_time!r}")
        else:
            w.send_text_message(payload.channel_no, "not found")

    elif payload.loc_args1 == "/members":
        r = w.get_channel_members_with_http_info(
            get_channel_members_request=GetChannelMembersRequest(
                channel_no=payload.channel_no
            )
        )
        w.send_text_message(payload.channel_no, f"{r.data.members[0]!r}")

    elif payload.loc_args1 == "/flex":
        with open("src/sample_flex.json") as f:
            j: dict = json.load(f)
        w.send_flex_message(
            payload.channel_no,
            flex_content=FlexContent(alt_text="test", contents=j),
        )

    if payload.notification_type == NotificationType.NOTIFICATION_STICKER:
        w.send_text_message(payload.channel_no, f"{payload.sticker=}")
        w.send_sticker_message(payload.channel_no, payload.sticker)
