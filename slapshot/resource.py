from __future__ import annotations

from typing_extensions import Any, Protocol, TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from slapshot.request import Request


T = TypeVar('T')


class SyncRequester(Protocol):
    """The protocol for a synchronous request sender."""

    def get(self, request: Request) -> Any: ...

    def get_model(self, request: Request, model: type[T]) -> T: ...


class AsyncRequester(Protocol):
    """The protocol for an asynchronous request sender."""

    async def get(self, request: Request) -> Any: ...

    async def get_model(self, request: Request, model: type[T]) -> T: ...


class SyncResource:
    """The base class for synchronous resources."""

    def __init__(self, requester: SyncRequester) -> None:
        self._requester = requester

    def _get(self, request: Request) -> Any:
        return self._requester.get(request)

    def _get_model(self, request: Request, model: type[T]) -> T:
        return self._requester.get_model(request, model)


class AsyncResource:
    """The base class for asynchronous resources."""

    def __init__(self, requester: AsyncRequester) -> None:
        self._requester = requester

    async def _get(self, request: Request) -> Any:
        return await self._requester.get(request)

    async def _get_model(self, request: Request, model: type[T]) -> T:
        return await self._requester.get_model(request, model)
