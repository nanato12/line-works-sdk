from pydantic import BaseModel, Field

from line_works.enums.yes_no_option import YesNoOption
from line_works.urls.talk import TalkURL


class LoginRequest(BaseModel):
    input_id: str = Field(alias="inputId")
    password: str
    keep_login: YesNoOption = Field(alias="keepLoginYn")
    remember_id: YesNoOption = Field(alias="rememberIdYn")
    access_url: str = Field(alias="accessUrl", default=TalkURL.HOST)

    class Config:
        use_enum_values = True
        populate_by_name = True
