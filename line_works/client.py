import json
from os import makedirs
from os.path import exists
from os.path import join as path_join
from typing import Any, Optional

from pydantic import BaseModel, Field
from requests import HTTPError, JSONDecodeError, Response, Session

from line_works import config
from line_works.decorator import save_cookie
from line_works.enums.yes_no_option import YesNoOption
from line_works.exceptions import GetMyInfoException, LoginException
from line_works.requests.login import LoginRequest
from line_works.responses.get_my_info import GetMyInfoResponse
from line_works.urls.auth import AuthURL
from line_works.urls.talk import TalkURL
from line_works.utils import get_msec
from logger import get_file_path_logger

logger = get_file_path_logger(__name__)


class LineWorks(BaseModel):
    works_id: str
    password: str = Field(repr=False)
    keep_login: YesNoOption = Field(repr=False, default=YesNoOption.YES)
    remember_id: YesNoOption = Field(repr=False, default=YesNoOption.YES)
    tenant_id: int = Field(init=False, default=0)
    domain_id: int = Field(init=False, default=0)
    contact_no: int = Field(init=False, default=0)
    session: Session = Field(init=False, repr=False, default_factory=Session)

    class Config:
        arbitrary_types_allowed = True

    @property
    def session_dir(self) -> str:
        return path_join(config.SESSION_DIR, self.works_id)

    @property
    def cookie_path(self) -> str:
        return path_join(self.session_dir, "cookie.json")

    def model_post_init(self, __context: Any) -> None:
        makedirs(self.session_dir, exist_ok=True)
        self.session.headers.update(config.HEADERS)

        r: Optional[Response] = None

        if exists(self.cookie_path):
            # login with cookie
            with open(self.cookie_path) as j:
                c = json.load(j)
            self.session.cookies.update(c)
            r = self.session.get(TalkURL.HOST, allow_redirects=False)

        if not r or r.status_code != 200:
            self.login_with_id()

        my_info = self.get_my_info()
        self.tenant_id = my_info.tenant_id
        self.domain_id = my_info.domain_id
        self.contact_no = my_info.contact_no

        logger.info(f"login success: {self!r}")

    @save_cookie
    def login_with_id(self) -> None:
        self.session.get(AuthURL.LOGIN)

        try:
            r = self.session.post(
                AuthURL.LOGIN_PROCESS_V2,
                data=LoginRequest(
                    input_id=self.works_id,
                    password=self.password,
                    keep_login=self.keep_login,
                    remember_id=self.remember_id,
                ).model_dump(by_alias=True),
            )
            r.raise_for_status()
        except HTTPError as e:
            raise LoginException(e)

    def get_my_info(self) -> GetMyInfoResponse:
        try:
            res: GetMyInfoResponse = GetMyInfoResponse.model_validate(
                (
                    r := self.session.get(f"{TalkURL.MY_INFO}?{get_msec()}")
                ).json()
            )
            r.raise_for_status()
        except JSONDecodeError:
            raise GetMyInfoException(
                f"Invalid response: [{r.status_code}] " f"{r.url}"
            )
        except HTTPError:
            raise GetMyInfoException(f"{res=}")

        return res
