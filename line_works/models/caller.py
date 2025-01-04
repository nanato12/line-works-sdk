from pydantic import BaseModel, Field


class Caller(BaseModel):
    domain_id: int = Field(alias="domainId")
    user_no: int = Field(alias="userNo")

    class Config:
        populate_by_name = True
