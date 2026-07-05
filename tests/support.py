from __future__ import annotations

import httpx

from typing_extensions import Any, TYPE_CHECKING

from slapshot.client import NHL, AsyncNHL

if TYPE_CHECKING:
    from slapshot.request import Request


JSON = 'application/json'

VALID_EMPTY = b'{}'
VALID_LIST = b'[]'
VALID_RESULT_SET = b'{"data":[],"total":0}'
VALID_ROSTER = b'{"forwards":[],"defensemen":[],"goalies":[]}'
VALID_STANDINGS = b'{"standings":[]}'
VALID_PLAYER_LANDING = (
    b'{"playerId":1,"isActive":true,"firstName":{"default":"A"},"lastName":{"default":"B"}}'
)


class Recorder:
    def __init__(
        self,
        payload: bytes = VALID_EMPTY,
        *,
        status_code: int = 200,
        content_type: str | None = JSON,
        exception: BaseException | None = None,
    ) -> None:
        self.requests: list[httpx.Request] = []
        self.payload = payload
        self.status_code = status_code
        self.content_type = content_type
        self.exception = exception

    def handle(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)

        if self.exception is not None:
            raise self.exception

        headers = {} if self.content_type is None else {'content-type': self.content_type}

        return httpx.Response(
            self.status_code,
            headers=headers,
            content=self.payload,
            request=request,
        )

    def transport(self) -> httpx.MockTransport:
        return httpx.MockTransport(self.handle)

    @property
    def request(self) -> httpx.Request:
        assert len(self.requests) == 1, f'expected one request, captured {len(self.requests)}'
        return self.requests[0]

    @property
    def url(self) -> str:
        return str(self.request.url)

    @property
    def path(self) -> str:
        return self.request.url.path

    @property
    def params(self) -> dict[str, str]:
        return dict(self.request.url.params)


class FakeSyncRequester:
    def __init__(self, result: Any = None) -> None:
        self.result = result
        self.calls: list[tuple[str, Request, type | None]] = []

    def get(self, request: Request) -> Any:
        self.calls.append(('get', request, None))
        return self.result

    def get_model(self, request: Request, model: type) -> Any:
        self.calls.append(('get_model', request, model))
        return self.result

    @property
    def call(self) -> tuple[str, Request, type | None]:
        assert len(self.calls) == 1, f'expected one call, captured {len(self.calls)}'
        return self.calls[0]

    @property
    def method(self) -> str:
        return self.call[0]

    @property
    def request(self) -> Request:
        return self.call[1]

    @property
    def model(self) -> type | None:
        return self.call[2]


class FakeAsyncRequester:
    def __init__(self, result: Any = None) -> None:
        self.result = result
        self.calls: list[tuple[str, Request, type | None]] = []

    async def get(self, request: Request) -> Any:
        self.calls.append(('get', request, None))
        return self.result

    async def get_model(self, request: Request, model: type) -> Any:
        self.calls.append(('get_model', request, model))
        return self.result

    @property
    def call(self) -> tuple[str, Request, type | None]:
        assert len(self.calls) == 1, f'expected one call, captured {len(self.calls)}'
        return self.calls[0]

    @property
    def method(self) -> str:
        return self.call[0]

    @property
    def request(self) -> Request:
        return self.call[1]

    @property
    def model(self) -> type | None:
        return self.call[2]


def sync_nhl(recorder: Recorder) -> NHL:
    return NHL(client=httpx.Client(transport=recorder.transport()))


def async_nhl(recorder: Recorder) -> AsyncNHL:
    return AsyncNHL(client=httpx.AsyncClient(transport=recorder.transport()))
