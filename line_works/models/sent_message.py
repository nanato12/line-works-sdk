from pydantic import BaseModel, Field


class SentMessage(BaseModel):
    message_id: int = Field(alias="messageId")
    channel_no: int = Field(alias="channelNo")
    writer_id: str = Field(alias="writerId")
    user_no: int = Field(alias="userNo")
    bot_no: int = Field(alias="botNo")
    message_no: int = Field(alias="messageNo")
    content: str
    member_count: int = Field(alias="memberCount")
    message_type_code: int = Field(alias="messageTypeCode")
    message_status_type: str = Field(alias="messageStatusType")
    message_status_type_code: int = Field(alias="messageStatusTypeCode")
    extras: str = Field(default="")
    tid: int
    create_time: int = Field(alias="createTime")
    update_time: int = Field(alias="updateTime")

    class Config:
        populate_by_name = True
