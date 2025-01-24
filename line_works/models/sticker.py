from pydantic import BaseModel, Field


class Sticker(BaseModel):
    sticker_type: str = Field(alias="stkType")
    package_version: str = Field(alias="pkgVer")
    package_id: str = Field(alias="pkgId")
    sticker_id: str = Field(alias="stkId")
    sticker_option: str = Field(alias="stkOpt")

    class Config:
        populate_by_name = True
