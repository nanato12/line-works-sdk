from pydantic import Field

from line_works.mqtt.models.payload._base import BasePayload


class BadgePayload(BasePayload):
    a_badge: int = Field(alias="aBadge")
    badge: int
    c_badge: int = Field(alias="cBadge")
    h_badge: int = Field(alias="hBadge")
    m_badge: int = Field(alias="mBadge")
    token: str
    user_no: int = Field(alias="userNo")
    wpa_badge: int = Field(alias="wpaBadge")

    class Config:
        populate_by_name = True

    @property
    def unique_id(self) -> str:
        return f"{self.loc_key}_{self.token}"
