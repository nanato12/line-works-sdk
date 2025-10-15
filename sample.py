import json

from line_works.client import LineWorks
from line_works.models import Emoji, MentionAll, MentionUser, Substitution
from line_works.mqtt.enums.notification_type import NotificationType
from line_works.mqtt.enums.packet_type import PacketType
from line_works.mqtt.models.packet import MQTTPacket
from line_works.mqtt.models.payload.message import MessagePayload
from line_works.openapi.talk.models.flex_content import FlexContent
from line_works.tracer import LineWorksTracer


def receive_publish_packet(w: LineWorks, p: MQTTPacket) -> None:
    payload = p.payload

    if not isinstance(payload, MessagePayload):
        return

    if not payload.channel_no:
        return

    print(f"{payload!r}")

    if payload.loc_args1 == "test":
        w.send_text_message(payload.channel_no, "ok")

    elif payload.loc_args1 == "/msg":
        w.send_text_message(payload.channel_no, f"{payload!r}")

    elif payload.loc_args1 == "/flex":
        with open("src/sample_flex.json") as f:
            j: dict = json.load(f)
        w.send_flex_message(
            payload.channel_no,
            flex_content=FlexContent(alt_text="test", contents=j),
        )

    elif payload.loc_args1 == "/mention":
        substitution = Substitution(
            mentions={"user": MentionUser(user_no=payload.from_user_no)}
        )
        w.send_text_message(
            payload.channel_no,
            "Hello, {user} !!",
            substitution=substitution,
        )

    elif payload.loc_args1 == "/emoji":
        substitution = Substitution(
            emojis={
                "emoji1": Emoji(
                    product_id="3", package_id="1.1", emoji_id="1001D5"
                )
            }
        )
        w.send_text_message(
            payload.channel_no,
            "{emoji1}",
            substitution=substitution,
        )

    elif payload.loc_args1 == "/all":
        substitution = Substitution(mentions={"everyone": MentionAll()})
        w.send_text_message(
            payload.channel_no, "{everyone}", substitution=substitution
        )

    if payload.notification_type == NotificationType.NOTIFICATION_STICKER:
        w.send_text_message(payload.channel_no, "スタンプ")
        w.send_text_message(payload.channel_no, f"{payload.sticker=}")

        w.send_sticker_message(payload.channel_no, payload.sticker)


WORKS_ID = "YOUR WORKS ID"
PASSWORD = "YOUR WORKS PASSWORD"

works = LineWorks(works_id=WORKS_ID, password=PASSWORD)

my_info = works.get_my_info()
print(f"{my_info=}")

tracer = LineWorksTracer(works=works)
tracer.add_trace_func(PacketType.PUBLISH, receive_publish_packet)
tracer.trace()
