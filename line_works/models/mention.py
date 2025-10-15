from typing import Literal, Optional

from pydantic import BaseModel


class MentionUser(BaseModel):
    """特定ユーザーへのメンション"""

    type: Literal["user"] = "user"
    user_no: int

    def to_html(self, display_name: Optional[str] = None) -> str:
        """LINE WORKS形式のHTMLに変換

        Args:
            display_name: 表示名（省略時はユーザー番号を使用）

        Returns:
            <m userNo="123456">@名前</m> 形式の文字列
        """
        name = display_name or str(self.user_no)
        return f'<m userNo="{self.user_no}">@{name}</m>'


class MentionAll(BaseModel):
    """全員へのメンション"""

    type: Literal["all"] = "all"

    def to_html(self, display_name: Optional[str] = None) -> str:
        """LINE WORKS形式のHTMLに変換

        Returns:
            <m userNo="all">@All</m> 形式の文字列
        """
        return '<m userNo="all">@All</m>'


Mention = MentionUser | MentionAll
