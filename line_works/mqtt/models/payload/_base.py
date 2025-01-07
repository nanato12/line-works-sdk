from abc import ABC, abstractmethod

from pydantic import BaseModel, Field

from line_works.mqtt.enums.notification_type import NotificationType


class BasePayload(BaseModel, ABC):
    domain_id: int = Field(alias="domain_id")
    loc_args0: str = Field(alias="loc-args0", default="")
    loc_args1: str = Field(alias="loc-args1", default="")
    loc_key: str = Field(alias="loc-key", default="")
    s_type: int = Field(alias="sType")
    ocn: int
    notification_type: NotificationType = Field(alias="nType")

    class Config:
        populate_by_name = True

    @property
    @abstractmethod
    def unique_id(self) -> str:
        pass
