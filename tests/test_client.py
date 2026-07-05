from __future__ import annotations

import httpx
import pytest

from tests.support import VALID_STANDINGS, Recorder, async_nhl, sync_nhl

from slapshot.client import NHL, AsyncNHL
from slapshot.exceptions import (
    BadRequestError,
    NHLConnectionError,
    NHLTimeoutError,
    NotFoundError,
    ResponseDecodeError,
    ServerError,
    UnexpectedContentTypeError,
)
from slapshot.models import StandingsResponse
from slapshot.request import request_build
from slapshot.version import __version__


URL = 'https://api-web.nhle.com/v1/standings/now'


def test_get_returns_decoded_json() -> None:
    nhl = sync_nhl(Recorder(b'{"a":1}'))
    assert nhl.get(request_build(URL)) == {'a': 1}


async def test_async_get_returns_decoded_json() -> None:
    nhl = async_nhl(Recorder(b'{"a":1}'))
    assert await nhl.get(request_build(URL)) == {'a': 1}


def test_get_forwards_params() -> None:
    recorder = Recorder(b'{}')
    sync_nhl(recorder).get(request_build(URL, {'a': 1, 'b': 'x'}))
    assert recorder.params == {'a': '1', 'b': 'x'}


async def test_async_get_forwards_params() -> None:
    recorder = Recorder(b'{}')
    await async_nhl(recorder).get(request_build(URL, {'a': 1, 'b': 'x'}))
    assert recorder.params == {'a': '1', 'b': 'x'}


def test_get_model_decodes_struct() -> None:
    nhl = sync_nhl(Recorder(VALID_STANDINGS))
    value = nhl.get_model(request_build(URL), StandingsResponse)
    assert isinstance(value, StandingsResponse)
    assert value.standings == []


async def test_async_get_model_decodes_struct() -> None:
    nhl = async_nhl(Recorder(VALID_STANDINGS))
    value = await nhl.get_model(request_build(URL), StandingsResponse)
    assert isinstance(value, StandingsResponse)


def test_get_raises_not_found() -> None:
    nhl = sync_nhl(Recorder(b'{}', status_code=404))
    with pytest.raises(NotFoundError):
        nhl.get(request_build(URL))


def test_get_raises_bad_request() -> None:
    nhl = sync_nhl(Recorder(b'{}', status_code=400))
    with pytest.raises(BadRequestError):
        nhl.get(request_build(URL))


def test_get_raises_server_error() -> None:
    nhl = sync_nhl(Recorder(b'{}', status_code=503))
    with pytest.raises(ServerError):
        nhl.get(request_build(URL))


async def test_async_get_raises_not_found() -> None:
    nhl = async_nhl(Recorder(b'{}', status_code=404))
    with pytest.raises(NotFoundError):
        await nhl.get(request_build(URL))


def test_get_model_raises_before_decode_on_error_status() -> None:
    nhl = sync_nhl(Recorder(b'not json', status_code=404))
    with pytest.raises(NotFoundError):
        nhl.get_model(request_build(URL), StandingsResponse)


def test_get_rejects_non_json() -> None:
    nhl = sync_nhl(Recorder(b'<html>', content_type='text/html'))
    with pytest.raises(UnexpectedContentTypeError):
        nhl.get(request_build(URL))


def test_get_rejects_missing_content_type() -> None:
    nhl = sync_nhl(Recorder(b'{}', content_type=None))
    with pytest.raises(UnexpectedContentTypeError):
        nhl.get(request_build(URL))


def test_get_wraps_bad_json() -> None:
    nhl = sync_nhl(Recorder(b'not json'))
    with pytest.raises(ResponseDecodeError):
        nhl.get(request_build(URL))


def test_get_model_wraps_bad_json() -> None:
    nhl = sync_nhl(Recorder(b'not json'))
    with pytest.raises(ResponseDecodeError):
        nhl.get_model(request_build(URL), StandingsResponse)


async def test_async_get_model_wraps_bad_json() -> None:
    nhl = async_nhl(Recorder(b'not json'))
    with pytest.raises(ResponseDecodeError):
        await nhl.get_model(request_build(URL), StandingsResponse)


def test_get_wraps_timeout() -> None:
    nhl = sync_nhl(Recorder(exception=httpx.TimeoutException('slow')))
    with pytest.raises(NHLTimeoutError):
        nhl.get(request_build(URL))


def test_get_model_wraps_timeout() -> None:
    nhl = sync_nhl(Recorder(exception=httpx.TimeoutException('slow')))
    with pytest.raises(NHLTimeoutError):
        nhl.get_model(request_build(URL), StandingsResponse)


def test_get_wraps_transport_error() -> None:
    nhl = sync_nhl(Recorder(exception=httpx.ConnectError('down')))
    with pytest.raises(NHLConnectionError):
        nhl.get(request_build(URL))


def test_get_model_wraps_transport_error() -> None:
    nhl = sync_nhl(Recorder(exception=httpx.ConnectError('down')))
    with pytest.raises(NHLConnectionError):
        nhl.get_model(request_build(URL), StandingsResponse)


async def test_async_get_model_wraps_timeout() -> None:
    nhl = async_nhl(Recorder(exception=httpx.TimeoutException('slow')))
    with pytest.raises(NHLTimeoutError):
        await nhl.get_model(request_build(URL), StandingsResponse)


async def test_async_get_model_wraps_transport_error() -> None:
    nhl = async_nhl(Recorder(exception=httpx.ConnectError('down')))
    with pytest.raises(NHLConnectionError):
        await nhl.get_model(request_build(URL), StandingsResponse)


async def test_async_get_wraps_timeout() -> None:
    nhl = async_nhl(Recorder(exception=httpx.TimeoutException('slow')))
    with pytest.raises(NHLTimeoutError):
        await nhl.get(request_build(URL))


async def test_async_get_wraps_transport_error() -> None:
    nhl = async_nhl(Recorder(exception=httpx.ConnectError('down')))
    with pytest.raises(NHLConnectionError):
        await nhl.get(request_build(URL))


def test_default_client_sets_user_agent() -> None:
    nhl = NHL()
    assert nhl._client.headers['user-agent'] == f'slapshot/{__version__}'
    nhl.close()


def test_close_closes_owned_client() -> None:
    nhl = NHL()
    nhl.close()
    assert nhl._client.is_closed


def test_close_leaves_injected_client_open() -> None:
    client = httpx.Client()
    nhl = NHL(client=client)
    nhl.close()
    assert not client.is_closed
    client.close()


def test_context_manager_closes() -> None:
    with NHL() as nhl:
        client = nhl._client
    assert client.is_closed


async def test_async_context_manager_closes() -> None:
    async with AsyncNHL() as nhl:
        client = nhl._client
    assert client.is_closed


async def test_async_close_leaves_injected_client_open() -> None:
    client = httpx.AsyncClient()
    nhl = AsyncNHL(client=client)
    await nhl.close()
    assert not client.is_closed
    await client.aclose()
