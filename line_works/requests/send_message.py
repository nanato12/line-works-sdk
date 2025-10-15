from typing import Optional, Self

from line_works.enums.message_type import MessageType
from line_works.models.substitution import Substitution
from line_works.openapi.talk.models.caller import Caller
from line_works.openapi.talk.models.flex_content import FlexContent
from line_works.openapi.talk.models.send_message_request import (
    SendMessageRequest as BaseSendMessageRequest,
)
from line_works.openapi.talk.models.sticker import Sticker


class SendMessageRequest(BaseSendMessageRequest):
    """メッセージ送信リクエスト

    LINE WORKS APIに送信するメッセージリクエストを構築します。
    """

    class Config:
        use_enum_values = True

    @classmethod
    def text_message(
        cls,
        caller: Caller,
        channel_no: int,
        text: str,
        substitution: Optional[Substitution] = None,
        user_name_map: Optional[dict[int, str]] = None,
    ) -> Self:
        """テキストメッセージを作成

        Args:
            caller: 送信者情報
            channel_no: チャンネル番号
            text: メッセージテキスト（プレースホルダー含む可能性あり）
            substitution: メンション・絵文字の置換情報
            user_name_map: userNoから名前へのマッピング

        Returns:
            SendMessageRequest: メッセージ送信リクエスト
        """
        # substitutionがある場合はプレースホルダーを置換
        if substitution and substitution.has_content():
            content = substitution.apply(text, user_name_map)
            # メンション・絵文字を含む場合はNEW_RICHタイプを使用
            message_type = MessageType.NEW_RICH
        else:
            content = text
            message_type = MessageType.TEXT

        return cls(
            channel_no=channel_no,
            content=content,
            caller=caller,
            type=message_type,
            extras="",
        )

    @classmethod
    def sticker_message(
        cls, caller: Caller, channel_no: int, sticker: Sticker
    ) -> Self:
        """スタンプメッセージを作成

        Args:
            caller: 送信者情報
            channel_no: チャンネル番号
            sticker: スタンプ情報

        Returns:
            SendMessageRequest: スタンプ送信リクエスト
        """
        return cls(
            channel_no=channel_no,
            caller=caller,
            extras=sticker.model_dump_json(by_alias=True),
            type=MessageType.STICKER,
        )

    @classmethod
    def flex_message(
        cls, caller: Caller, channel_no: int, flex_content: FlexContent
    ) -> Self:
        """Flexメッセージを作成

        Args:
            caller: 送信者情報
            channel_no: チャンネル番号
            flex_content: Flexコンテンツ

        Returns:
            SendMessageRequest: Flex送信リクエスト
        """
        return cls(
            channel_no=channel_no,
            caller=caller,
            extras=flex_content.model_dump_json(by_alias=True),
            type=MessageType.BOT_FLEX,
        )
