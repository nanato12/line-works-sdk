import json
from os import makedirs
from os.path import exists
from os.path import join as path_join
from typing import Any

from pydantic import BaseModel, Field, PrivateAttr
from requests import HTTPError, Session

from line_works import config
from line_works.decorator import save_cookie
from line_works.enums.yes_no_option import YesNoOption
from line_works.exceptions import LoginException
from line_works.logger import get_file_path_logger
from line_works.openapi.talk.api.default_api import DefaultApi as TalkApi
from line_works.openapi.talk.api_client import ApiClient as TalkApiClient
from line_works.openapi.talk.models.caller import Caller
from line_works.openapi.talk.models.flex_content import FlexContent
from line_works.openapi.talk.models.send_message_response import (
    SendMessageResponse,
)
from line_works.openapi.talk.models.sticker import Sticker
from line_works.requests.login import LoginRequest
from line_works.requests.send_message import SendMessageRequest
from line_works.urls.auth import AuthURL

logger = get_file_path_logger(__name__)


class LineWorks(BaseModel, TalkApi):
    works_id: str
    password: str = Field(repr=False)
    keep_login: YesNoOption = Field(repr=False, default=YesNoOption.YES)
    remember_id: YesNoOption = Field(repr=False, default=YesNoOption.YES)
    tenant_id: int = Field(init=False, default=0)
    domain_id: int = Field(init=False, default=0)
    contact_no: int = Field(init=False, default=0)
    session: Session = Field(init=False, repr=False, default_factory=Session)
    api_client: TalkApiClient = Field(
        init=False, repr=False, default_factory=TalkApiClient
    )
    _caller: Caller = PrivateAttr()

    class Config:
        arbitrary_types_allowed = True

    @property
    def session_dir(self) -> str:
        return path_join(config.SESSION_DIR, self.works_id)

    @property
    def cookie_path(self) -> str:
        return path_join(self.session_dir, "cookie.json")

    @property
    def cookie_str(self) -> str:
        return "; ".join(f"{k}={v}" for k, v in self.session.cookies.items())

    def model_post_init(self, __context: Any) -> None:
        makedirs(self.session_dir, exist_ok=True)
        self.session.headers.update(config.HEADERS)

        if exists(self.cookie_path):
            # login with cookie
            with open(self.cookie_path) as j:
                c = json.load(j)
            self.session.cookies.update(c)

        try:
            my_info = self.get_my_info()
        except Exception:
            self.login_with_id()

        TalkApi.__init__(self)
        for k, v in config.HEADERS.items():
            self.api_client.set_default_header(k, v)
        self.api_client.set_default_header("Cookie", self.cookie_str)

        my_info = self.get_my_info()
        self.tenant_id = my_info.tenant_id
        self.domain_id = my_info.domain_id
        self.contact_no = my_info.contact_no
        self._caller = Caller(
            domain_id=self.domain_id, user_no=self.contact_no
        )

        logger.info(f"login success: {self!r}")

    @save_cookie
    def login_with_id(self, with_default_cookie: bool = False) -> None:
        self.session.cookies.clear()
        if with_default_cookie:
            self.session.cookies.update(config.COOKIE)
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

        j: dict = r.json()
        if j.get("accessUrl"):
            return

        if with_default_cookie:
            raise LoginException("invalid login.")

        self.login_with_id(with_default_cookie=True)

    def send_text_message(self, to: int, text: str) -> SendMessageResponse:
        return self.send_message(
            send_message_request=SendMessageRequest.text_message(
                self._caller, to, text
            )
        )

    def send_sticker_message(
        self, to: int, sticker: Sticker
    ) -> SendMessageResponse:
        return self.send_message(
            send_message_request=SendMessageRequest.sticker_message(
                self._caller, to, sticker
            )
        )

    def send_flex_message(
        self, to: int, flex_content: FlexContent
    ) -> SendMessageResponse:
        return self.send_message(
            send_message_request=SendMessageRequest.flex_message(
                self._caller, to, flex_content
            )
        )
