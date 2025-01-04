import json
from os import makedirs
from os.path import exists
from os.path import join as path_join
from typing import Any, Type

from pydantic import BaseModel, Field, PrivateAttr
from requests import HTTPError, JSONDecodeError, Session

from line_works import config
from line_works.constants import RequestType
from line_works.decorator import save_cookie
from line_works.enums.yes_no_option import YesNoOption
from line_works.exceptions import (
    GetMyInfoException,
    LoginException,
    SendMessageException,
)
from line_works.logger import get_file_path_logger
from line_works.models.caller import Caller
from line_works.requests.login import LoginRequest
from line_works.requests.send_message import SendMessageRequest
from line_works.responses.get_my_info import GetMyInfoResponse
from line_works.responses.send_message import SendMessageResponse
from line_works.urls.auth import AuthURL
from line_works.urls.talk import TalkURL

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
    _caller: Caller = PrivateAttr()

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

        if exists(self.cookie_path):
            # login with cookie
            with open(self.cookie_path) as j:
                c = json.load(j)
            self.session.cookies.update(c)

        try:
            my_info = self.get_my_info()
        except Exception:
            self.session.cookies.clear()
            self.login_with_id()

        my_info = self.get_my_info()
        self.tenant_id = my_info.tenant_id
        self.domain_id = my_info.domain_id
        self.contact_no = my_info.contact_no
        self._caller = Caller(
            domain_id=self.domain_id, user_no=self.contact_no
        )

        logger.info(f"login success: {self!r}")

    def _request_with_error_handling(
        self,
        method: str,
        url: str,
        ex: Type[Exception],
        **kwargs: Any,
    ) -> dict[str, Any]:
        try:
            r = self.session.request(method, url, **kwargs)
            r.raise_for_status()
            return r.json()  # type: ignore
        except HTTPError as e:
            raise ex(f"HTTP error: {e}") from e
        except JSONDecodeError as e:
            raise ex(f"Invalid response: [{r.status_code}] {r.url}") from e
        except Exception as e:
            raise ex(f"Unexpected error: {e}") from e

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
        d = self._request_with_error_handling(
            RequestType.GET,
            TalkURL.MY_INFO,
            GetMyInfoException,
        )
        return GetMyInfoResponse.model_validate(d)  # type: ignore

    def send_message(self, to: int, text: str) -> SendMessageResponse:
        d = self._request_with_error_handling(
            RequestType.POST,
            TalkURL.SEND_MESSAGE,
            SendMessageException,
            json=SendMessageRequest.text_message(
                to, text, self._caller
            ).model_dump(by_alias=True),
        )
        return SendMessageResponse.model_validate(d)  # type: ignore
