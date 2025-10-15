import io
import json
from os import makedirs
from os.path import exists
from os.path import join as path_join
from pathlib import Path
from time import time
from typing import Any, Optional
from urllib.parse import urljoin

from PIL import Image
from pydantic import BaseModel, Field, PrivateAttr
from requests import HTTPError, Session

from line_works import config
from line_works.decorator import save_cookie
from line_works.enums.message_type import MessageType
from line_works.enums.yes_no_option import YesNoOption
from line_works.exceptions import LoginException
from line_works.logger import get_file_path_logger
from line_works.models.substitution import Substitution
from line_works.mqtt.enums.channel_type import ChannelType
from line_works.openapi.storage.api.default_api import DefaultApi as StorageApi
from line_works.openapi.storage.models.resource_extras import ResourceExtras
from line_works.openapi.storage.models.upload_resouce_response import (
    UploadResouceResponse,
)
from line_works.openapi.talk.api.default_api import DefaultApi as TalkApi
from line_works.openapi.talk.api_client import ApiClient as TalkApiClient
from line_works.openapi.talk.models.caller import Caller
from line_works.openapi.talk.models.flex_content import FlexContent
from line_works.openapi.talk.models.get_channel_members_request import (
    GetChannelMembersRequest,
)
from line_works.openapi.talk.models.issue_resource_path_request import (
    IssueResourcePathRequest,
)
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
    storage_api: StorageApi = Field(
        init=False, repr=False, default_factory=StorageApi
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
            self.storage_api.api_client.set_default_header(k, v)
        self.api_client.set_default_header("Cookie", self.cookie_str)
        self.storage_api.api_client.set_default_header(
            "Cookie", self.cookie_str
        )

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

    def _send_message_urlencoded(
        self, send_message_request: SendMessageRequest
    ) -> SendMessageResponse:
        """メンションや絵文字を含むメッセージを
        application/x-www-form-urlencodedで送信
        """
        payload_dict = send_message_request.model_dump(
            by_alias=True,
            exclude_none=True,
        )
        payload_json = json.dumps(
            payload_dict, ensure_ascii=False, separators=(",", ":")
        )
        logger.debug(f"Sending message with payload: {payload_json}")

        response = self.session.post(
            "https://talk.worksmobile.com/p/oneapp/client/chat/sendMessage",
            data={"payload": payload_json},
            headers={
                "Content-Type": (
                    "application/x-www-form-urlencoded;charset=UTF-8"
                ),
            },
        )
        response.raise_for_status()
        return SendMessageResponse.model_validate(response.json())

    def get_user_name_map(self, channel_no: int) -> dict[int, str]:
        """チャンネルメンバーのuserNoから名前へのマッピングを取得"""
        response = self.get_channel_members(
            get_channel_members_request=GetChannelMembersRequest(
                channel_no=channel_no
            )
        )
        return {member.user_no: member.name for member in response.members}

    def send_text_message(
        self,
        to: int,
        text: str,
        substitution: "Optional[Substitution]" = None,
    ) -> SendMessageResponse:
        """テキストメッセージを送信"""
        user_name_map = None
        if substitution and getattr(substitution, "mentions", None):
            user_name_map = self.get_user_name_map(to)

        request = SendMessageRequest.text_message(
            self._caller, to, text, substitution, user_name_map
        )

        if (
            substitution
            and getattr(substitution, "has_content", lambda: False)()
        ):
            return self._send_message_urlencoded(request)

        return self.send_message(send_message_request=request)

    def __upload_resource(
        self,
        to: int,
        channel_type: ChannelType,
        msg_type: MessageType,
        resource_bytes: bytes,
        file_name: str,
        extras: ResourceExtras,
    ) -> UploadResouceResponse:
        res = self.issue_resource_path(
            issue_resource_path_request=IssueResourcePathRequest(
                channel_no=to,
                channel_type=channel_type,
                filename=file_name,
                filesize=len(resource_bytes),
                msg_type=msg_type,
            )
        )
        extras.resourcepath = res.var_resource_path

        # TODO: openapiで定義したものを使う
        # res = self.storage_api.upload_resource(
        #     x_type=str(msg_type),
        #     x_channelno=str(to),
        #     x_extras=extras,
        #     upload_resource_path=res.var_resource_path,
        # )
        # print(res)

        self.session.headers.update(
            {
                "Device-Language": "ja_JP",
                "x-resourcepath": res.var_resource_path,
                "x-serviceid": "works",
                "x-type": str(msg_type),
                "x-callerno": str(self.contact_no),
                "x-channelno": str(to),
                "x-extras": extras.model_dump_json(),
                "x-ocn": "1",
                "x-tid": str(int(time() * 1000)),
            }
        )

        response = self.session.post(
            urljoin("https://storage.worksmobile.com", res.var_resource_path),
            params={
                "Servicekey": "oneapp",
                "writeMode": "overwrite",
                "isMakethumbnail": "true",
            },
            files={"file": resource_bytes},
        )
        return UploadResouceResponse.model_validate(response.json())

    def send_image_message(
        self, to: int, channel_type: ChannelType, image_file_path: str
    ) -> UploadResouceResponse:
        path = Path(image_file_path)
        with open(path, "rb") as f:
            image_bytes = f.read()

        return self.send_image_message_with_file(
            to=to,
            channel_type=channel_type,
            image_bytes=image_bytes,
            file_name=path.name,
        )

    def send_image_message_with_file(
        self,
        to: int,
        channel_type: ChannelType,
        image_bytes: bytes,
        file_name: str,
    ) -> UploadResouceResponse:
        image = Image.open(io.BytesIO(image_bytes), mode="r")

        extras = ResourceExtras(
            filename=file_name,
            filesize=len(image_bytes),
            width=image.width,
            height=image.height,
        )

        return self.__upload_resource(
            to, channel_type, MessageType.IMAGE, image_bytes, file_name, extras
        )

    def send_file_message(
        self, to: int, channel_type: ChannelType, file_path: str
    ) -> UploadResouceResponse:
        path = Path(file_path)
        with open(path, "rb") as f:
            file_bytes = f.read()

        extras = ResourceExtras(
            filename=path.name,
            filesize=len(file_bytes),
        )

        return self.__upload_resource(
            to, channel_type, MessageType.FILE, file_bytes, path.name, extras
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
