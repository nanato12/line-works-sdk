from pydantic import Field

from line_works.mqtt.models.payload._base import BasePayload


class ServicePayload(BasePayload):
    detail_message_exist: int = Field(alias="detailMessageExist")
    icon_url: str = Field(alias="iconUrl")
    mqtt_target_device_type_list0: str = Field(
        alias="mqttTargetDeviceTypeList0"
    )
    mqtt_target_device_type_list1: str = Field(
        alias="mqttTargetDeviceTypeList1"
    )
    mqtt_target_device_type_list2: str = Field(
        alias="mqttTargetDeviceTypeList2"
    )
    notification_no: int = Field(alias="notificationNo")
    service_type: int = Field(alias="serviceType")
    show_red_dot: int = Field(alias="showRedDot")

    class Config:
        populate_by_name = True

    @property
    def unique_id(self) -> str:
        return f"{self.loc_key}_{self.notification_no}"
