import socket
from typing import Any, Mapping, Optional, Union

from requests import PreparedRequest, Response, Session
from requests.adapters import HTTPAdapter
from urllib3.connection import HTTPConnection

from line_works.openapi.talk.api_client import ApiClient as TalkApiClient
from line_works.openapi.talk.configuration import (
    Configuration as TalkConfiguration,
)
from line_works.openapi.talk.rest import RESTResponse

# (connect, read) のタイムアウト秒。無制限にすると NAT などで静かに
# 捨てられたコネクションで数十分ブロックする
DEFAULT_TIMEOUT: tuple[float, float] = (10.0, 30.0)

# アイドル中に切れたコネクションをカーネルに検出させ、プールから
# 取り出す前に閉じておくための TCP keepalive
KEEPALIVE_SOCKET_OPTIONS: list[tuple[int, int, int]] = [
    *HTTPConnection.default_socket_options,
    (socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1),
]
if hasattr(socket, "TCP_KEEPIDLE"):
    KEEPALIVE_SOCKET_OPTIONS.append(
        (socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 60)
    )
if hasattr(socket, "TCP_KEEPINTVL"):
    KEEPALIVE_SOCKET_OPTIONS.append(
        (socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 10)
    )
if hasattr(socket, "TCP_KEEPCNT"):
    KEEPALIVE_SOCKET_OPTIONS.append(
        (socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 3)
    )


class TimeoutHTTPAdapter(HTTPAdapter):
    """timeout 未指定のリクエストに既定値を適用する HTTPAdapter"""

    def __init__(self, timeout: tuple[float, float], **kwargs: Any) -> None:
        self.timeout = timeout
        super().__init__(**kwargs)

    def init_poolmanager(self, *args: Any, **kwargs: Any) -> None:
        kwargs.setdefault("socket_options", KEEPALIVE_SOCKET_OPTIONS)
        super().init_poolmanager(*args, **kwargs)

    def send(
        self,
        request: PreparedRequest,
        stream: bool = False,
        timeout: Union[
            None, float, tuple[float, float], tuple[float, None]
        ] = None,
        verify: Union[bool, str] = True,
        cert: Union[
            None, bytes, str, tuple[Union[bytes, str], Union[bytes, str]]
        ] = None,
        proxies: Optional[Mapping[str, str]] = None,
    ) -> Response:
        if timeout is None:
            timeout = self.timeout
        return super().send(
            request,
            stream=stream,
            timeout=timeout,
            verify=verify,
            cert=cert,
            proxies=proxies,
        )


def create_session(
    timeout: tuple[float, float] = DEFAULT_TIMEOUT,
) -> Session:
    session = Session()
    adapter = TimeoutHTTPAdapter(timeout)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


class TimeoutTalkApiClient(TalkApiClient):
    """`_request_timeout` 未指定の呼び出しに既定値を適用する ApiClient"""

    def __init__(
        self,
        timeout: tuple[float, float] = DEFAULT_TIMEOUT,
        configuration: Optional[TalkConfiguration] = None,
    ) -> None:
        if configuration is None:
            configuration = TalkConfiguration()
            configuration.socket_options = KEEPALIVE_SOCKET_OPTIONS
        super().__init__(configuration=configuration)
        self.timeout = timeout

    def call_api(
        self,
        method: str,
        url: str,
        header_params: Optional[dict[str, Any]] = None,
        body: Any = None,
        post_params: Any = None,
        _request_timeout: Any = None,
    ) -> RESTResponse:
        if _request_timeout is None:
            _request_timeout = self.timeout
        return super().call_api(
            method,
            url,
            header_params=header_params,
            body=body,
            post_params=post_params,
            _request_timeout=_request_timeout,
        )
