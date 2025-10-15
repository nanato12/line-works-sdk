from typing import Literal

from pydantic import BaseModel


class Emoji(BaseModel):
    """絵文字"""

    type: Literal["emoji"] = "emoji"
    product_id: str  # 例: "3"
    package_id: str  # 例: "1.1"
    emoji_id: str  # 例: "1001D5"

    def to_html(self) -> str:
        """LINE WORKS形式のHTMLに変換

        Returns:
            <e class="/3/1.1/1001D5">(emoji_name)</e> 形式の文字列
        """
        class_path = f"/{self.product_id}/{self.package_id}/{self.emoji_id}"
        return f'<e class="{class_path}">({self.emoji_id})</e>'
