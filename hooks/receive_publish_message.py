from line_works.client import LineWorks
from line_works.mqtt.models.message import NotificationMessage


def receive_publish_message(
    w: LineWorks, message: NotificationMessage
) -> None:
    print(f"{message=}")
