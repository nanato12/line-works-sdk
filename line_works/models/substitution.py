from typing import Dict, Optional

from pydantic import BaseModel

from line_works.models.emoji import Emoji
from line_works.models.mention import Mention


class Substitution(BaseModel):
    """メッセージ内のプレースホルダーをメンション・絵文字に置き換える

    使用例:
        >>> substitution = Substitution(
        ...     mentions={
        ...         "user": MentionUser(user_no=123456)
        ...     },
        ...     emojis={
        ...         "smile": Emoji(
        ...             product_id="3",
        ...             package_id="1.1",
        ...             emoji_id="1001D5"
        ...         )
        ...     }
        ... )
        >>> content = substitution.apply("Hello {user}! {smile}")
        >>> # => "Hello <m userNo=\"123456\">@User</m>! "
        ... #    "<e class=\"/3/1.1/1001D5\">(1001D5)</e>"
    """

    mentions: Dict[str, Mention] = {}
    emojis: Dict[str, Emoji] = {}

    def apply(
        self, text: str, user_name_map: Optional[Dict[int, str]] = None
    ) -> str:
        """テキスト内のプレースホルダーをLINE WORKS形式のHTMLに置き換える"""
        content = text
        for placeholder, mention in self.mentions.items():
            pattern = f"{{{placeholder}}}"
            display_name = self._get_mention_display_name(
                mention, placeholder, user_name_map
            )
            replacement = mention.to_html(display_name)
            content = content.replace(pattern, replacement)
        for placeholder, emoji in self.emojis.items():
            pattern = f"{{{placeholder}}}"
            replacement = emoji.to_html()
            content = content.replace(pattern, replacement)
        return content

    def _get_mention_display_name(
        self,
        mention: Mention,
        placeholder: str,
        user_name_map: Optional[Dict[int, str]],
    ) -> Optional[str]:
        """メンションの表示名を取得"""
        if mention.type == "user":
            if user_name_map and mention.user_no in user_name_map:
                return user_name_map[mention.user_no]
            return placeholder
        return "None"

    def has_content(self) -> bool:
        """メンションまたは絵文字が含まれているかチェック"""
        return bool(self.mentions or self.emojis)

    def to_content(
        self, text: str, user_name_map: Optional[Dict[int, str]] = None
    ) -> str:
        """後方互換性のためのエイリアス"""
        return self.apply(text, user_name_map)
