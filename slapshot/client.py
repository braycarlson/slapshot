from __future__ import annotations

import json
import warnings

import httpx
import msgspec

from typing_extensions import Any, Self, TypeVar, TYPE_CHECKING

from slapshot.exceptions import (
    InvalidTimeoutError,
    NHLConnectionError,
    NHLTimeoutError,
    ResponseDecodeError,
    UnexpectedContentTypeError,
    error_from_response,
)
from slapshot.introspect import UnknownFieldWarning, unknown_fields
from slapshot.resources.draft import AsyncDraft, Draft
from slapshot.resources.games import AsyncGames, Games
from slapshot.resources.players import AsyncPlayers, Players
from slapshot.resources.records import AsyncRecords, Records
from slapshot.resources.schedule import AsyncSchedule, Schedule
from slapshot.resources.standings import AsyncStandings, Standings
from slapshot.resources.stats import AsyncStats, Stats
from slapshot.resources.teams import AsyncTeams, Teams
from slapshot.version import __version__

if TYPE_CHECKING:
    from slapshot.request import Request


T = TypeVar('T')

TIMEOUT_SECONDS_DEFAULT = 30.0


def response_raise(response: httpx.Response) -> None:
    if response.status_code >= 400:
        raise error_from_response(response)


def response_process(response: httpx.Response) -> Any:
    response_raise(response)

    content_type = response.headers.get('content-type', '')

    if 'application/json' not in content_type:
        raise UnexpectedContentTypeError(content_type, str(response.request.url))

    try:
        payload = response.json()
    except json.JSONDecodeError as exception:
        raise ResponseDecodeError(str(response.request.url)) from exception

    return payload


def warn_unknown(response: httpx.Response, model: Any) -> None:
    raw = msgspec.json.decode(response.content)
    missing = unknown_fields(raw, model)

    if missing:
        name = getattr(model, '__name__', str(model))
        warnings.warn(
            f'{response.request.url}: response has fields not defined in {name}: {missing}',
            UnknownFieldWarning,
            stacklevel=2,
        )


class NHL:
    """The synchronous client for the NHL API.

    It exposes one attribute per resource: standings, schedule, games, players,
    teams, draft, stats, and records. Every request may raise an NHLError
    subclass on a transport failure or an error response.
    """

    def __init__(
        self,
        *,
        timeout: float = TIMEOUT_SECONDS_DEFAULT,
        client: httpx.Client | None = None,
        warn_unknown_fields: bool = False,
    ) -> None:
        """It initializes the client.

        Args:
            timeout: Request timeout in seconds. Must be greater than zero.
            client: A preconfigured httpx.Client. When omitted, one is created
                and closed automatically; when supplied, its lifecycle is left
                to the caller.
            warn_unknown_fields: When true, emit an UnknownFieldWarning for any
                typed response that carries a field the model does not define.

        Raises:
            InvalidTimeoutError: If timeout is not greater than zero.
        """

        if timeout <= 0:
            raise InvalidTimeoutError(timeout)

        self._warn_unknown_fields = warn_unknown_fields
        self._autoclose = client is None

        if client is None:
            headers = {'User-Agent': f'slapshot/{__version__}'}
            self._client = httpx.Client(follow_redirects=True, timeout=timeout, headers=headers)
        else:
            self._client = client

        self.draft = Draft(self)
        self.games = Games(self)
        self.players = Players(self)
        self.records = Records(self)
        self.schedule = Schedule(self)
        self.standings = Standings(self)
        self.stats = Stats(self)
        self.teams = Teams(self)

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def close(self) -> None:
        """It closes the underlying transport if this client created it."""

        if self._autoclose:
            self._client.close()

    def get(self, request: Request) -> Any:
        """It sends a request and returns the decoded JSON payload.

        Args:
            request: The request to send.

        Returns:
            The decoded JSON response as a dict or list.

        Raises:
            NHLTimeoutError: If the request exceeds its timeout.
            NHLConnectionError: If the request fails to reach the API.
            APIStatusError: If the response status is 400 or greater.
            UnexpectedContentTypeError: If the response is not JSON.
            ResponseDecodeError: If the body cannot be decoded.
        """

        try:
            response = self._client.get(request.url, params=request.params)
        except httpx.TimeoutException as exception:
            raise NHLTimeoutError(str(exception)) from exception
        except httpx.TransportError as exception:
            raise NHLConnectionError(str(exception)) from exception

        return response_process(response)

    def get_model(self, request: Request, model: type[T]) -> T:
        """It sends a request and decodes the JSON body into a model.

        Args:
            request: The request to send.
            model: The msgspec type to decode the response into.

        Returns:
            The decoded model instance.

        Raises:
            NHLTimeoutError: If the request exceeds its timeout.
            NHLConnectionError: If the request fails to reach the API.
            APIStatusError: If the response status is 400 or greater.
            ResponseDecodeError: If the body cannot be decoded into the model.
        """

        try:
            response = self._client.get(request.url, params=request.params)
        except httpx.TimeoutException as exception:
            raise NHLTimeoutError(str(exception)) from exception
        except httpx.TransportError as exception:
            raise NHLConnectionError(str(exception)) from exception

        response_raise(response)

        try:
            model_value = msgspec.json.decode(response.content, type=model)
        except msgspec.MsgspecError as exception:
            raise ResponseDecodeError(str(response.request.url)) from exception

        if self._warn_unknown_fields:
            warn_unknown(response, model)

        return model_value


class AsyncNHL:
    """The asynchronous client for the NHL API.

    It mirrors NHL with awaitable methods. Every request may raise an NHLError
    subclass on a transport failure or an error response.
    """

    def __init__(
        self,
        *,
        timeout: float = TIMEOUT_SECONDS_DEFAULT,
        client: httpx.AsyncClient | None = None,
        warn_unknown_fields: bool = False,
    ) -> None:
        """It initializes the client.

        Args:
            timeout: Request timeout in seconds. Must be greater than zero.
            client: A preconfigured httpx.AsyncClient. When omitted, one is
                created and closed automatically; when supplied, its lifecycle
                is left to the caller.
            warn_unknown_fields: When true, emit an UnknownFieldWarning for any
                typed response that carries a field the model does not define.

        Raises:
            InvalidTimeoutError: If timeout is not greater than zero.
        """

        if timeout <= 0:
            raise InvalidTimeoutError(timeout)

        self._warn_unknown_fields = warn_unknown_fields
        self._autoclose = client is None

        if client is None:
            headers = {'User-Agent': f'slapshot/{__version__}'}

            self._client = httpx.AsyncClient(
                follow_redirects=True, timeout=timeout, headers=headers
            )
        else:
            self._client = client

        self.draft = AsyncDraft(self)
        self.games = AsyncGames(self)
        self.players = AsyncPlayers(self)
        self.records = AsyncRecords(self)
        self.schedule = AsyncSchedule(self)
        self.standings = AsyncStandings(self)
        self.stats = AsyncStats(self)
        self.teams = AsyncTeams(self)

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()

    async def close(self) -> None:
        """It closes the underlying transport if this client created it."""

        if self._autoclose:
            await self._client.aclose()

    async def get(self, request: Request) -> Any:
        """It sends a request and returns the decoded JSON payload.

        Args:
            request: The request to send.

        Returns:
            The decoded JSON response as a dict or list.

        Raises:
            NHLTimeoutError: If the request exceeds its timeout.
            NHLConnectionError: If the request fails to reach the API.
            APIStatusError: If the response status is 400 or greater.
            UnexpectedContentTypeError: If the response is not JSON.
            ResponseDecodeError: If the body cannot be decoded.
        """

        try:
            response = await self._client.get(request.url, params=request.params)
        except httpx.TimeoutException as exception:
            raise NHLTimeoutError(str(exception)) from exception
        except httpx.TransportError as exception:
            raise NHLConnectionError(str(exception)) from exception

        return response_process(response)

    async def get_model(self, request: Request, model: type[T]) -> T:
        """It sends a request and decodes the JSON body into a model.

        Args:
            request: The request to send.
            model: The msgspec type to decode the response into.

        Returns:
            The decoded model instance.

        Raises:
            NHLTimeoutError: If the request exceeds its timeout.
            NHLConnectionError: If the request fails to reach the API.
            APIStatusError: If the response status is 400 or greater.
            ResponseDecodeError: If the body cannot be decoded into the model.
        """

        try:
            response = await self._client.get(request.url, params=request.params)
        except httpx.TimeoutException as exception:
            raise NHLTimeoutError(str(exception)) from exception
        except httpx.TransportError as exception:
            raise NHLConnectionError(str(exception)) from exception

        response_raise(response)

        try:
            model_value = msgspec.json.decode(response.content, type=model)
        except msgspec.MsgspecError as exception:
            raise ResponseDecodeError(str(response.request.url)) from exception

        if self._warn_unknown_fields:
            warn_unknown(response, model)

        return model_value
