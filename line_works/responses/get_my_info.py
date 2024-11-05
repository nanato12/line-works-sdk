from pydantic import BaseModel, Field


class Name(BaseModel):
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")
    phonetic_first_name: str = Field(alias="phoneticFirstName")
    phonetic_last_name: str = Field(alias="phoneticLastName")
    phonetic_name: str = Field(alias="phoneticName")
    display_name: str = Field(alias="displayName")

    class Config:
        populate_by_name = True


class Organization(BaseModel):
    domain_id: int = Field(alias="domainId")
    organization: str
    groups: list[str]

    class Config:
        populate_by_name = True


class Email(BaseModel):
    content: str
    type_code: str = Field(alias="typeCode")
    represent: bool

    class Config:
        populate_by_name = True


class UserService(BaseModel):
    service_type: str = Field(alias="serviceType")
    works_at_user_no: int = Field(alias="worksAtUserNo")
    name: str
    id: str
    invite_url: str = Field(alias="inviteUrl")

    class Config:
        populate_by_name = True


class WorksAt(BaseModel):
    id: str
    invite_url: str = Field(alias="inviteUrl")
    users: list[UserService]
    works_at_count: int = Field(alias="worksAtCount")
    id_search_block: bool = Field(alias="idSearchBlock")

    class Config:
        populate_by_name = True


class GetMyInfoResponse(BaseModel):
    tenant_id: int = Field(alias="tenantId")
    domain_id: int = Field(alias="domainId")
    contact_no: int = Field(alias="contactNo")
    read_only: bool = Field(alias="readOnly")
    temp_id: bool = Field(alias="tempId")
    name: Name
    i18n_name: str = Field(alias="i18nName")
    i18n_names: list[str] = Field(alias="i18nNames")
    photos: list[str]
    organizations: list[Organization]
    emails: list[Email]
    telephones: list[str]
    messengers: list[str]
    position: str
    department: str
    location: str
    important: bool
    executive: bool
    photo_hash: str = Field(alias="photoHash")
    works_at: WorksAt = Field(alias="worksAt")
    access_limit: bool = Field(alias="accessLimit")
    user_photo_modify: bool = Field(alias="userPhotoModify")
    user_absence_modify: bool = Field(alias="userAbsenceModify")
    organization: str
    groups: list[str]
    works_services: list[str] = Field(alias="worksServices")
    custom_fields: list[str] = Field(alias="customFields")
    profile_statuses: list[str] = Field(alias="profileStatuses")
    profile_statuses_v2: list[str] = Field(alias="profileStatusesV2")
    instance: int

    class Config:
        populate_by_name = True
