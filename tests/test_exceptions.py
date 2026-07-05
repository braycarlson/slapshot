from __future__ import annotations

import httpx
import pytest

from slapshot.client import NHL, response_process
from slapshot.exceptions import (
    BODY_PREVIEW_LENGTH_MAX,
    APIStatusError,
    BadRequestError,
    ForbiddenError,
    InvalidIdentifierError,
    InvalidParameterError,
    InvalidSeasonError,
    NHLConnectionError,
    NHLError,
    NHLTimeoutError,
    NotFoundError,
    RateLimitError,
    ResponseDecodeError,
    ServerError,
    UnauthorizedError,
    UnexpectedContentTypeError,
    error_from_response,
)


def response_with(status_code: int, content: bytes = b'') -> httpx.Response:
    return httpx.Response(
        status_code,
        content=content,
        request=httpx.Request('GET', 'https://example.com'),
    )


def response_body(content_type: str, content: bytes) -> httpx.Response:
    return httpx.Response(
        200,
        headers={'content-type': content_type},
        content=content,
        request=httpx.Request('GET', 'https://example.com'),
    )


def test_maps_bad_request() -> None:
    assert isinstance(error_from_response(response_with(400)), BadRequestError)


def test_maps_unauthorized() -> None:
    assert isinstance(error_from_response(response_with(401)), UnauthorizedError)


def test_maps_forbidden() -> None:
    assert isinstance(error_from_response(response_with(403)), ForbiddenError)


def test_maps_not_found() -> None:
    assert isinstance(error_from_response(response_with(404)), NotFoundError)


def test_maps_rate_limit() -> None:
    assert isinstance(error_from_response(response_with(429)), RateLimitError)


def test_maps_server_500() -> None:
    assert isinstance(error_from_response(response_with(500)), ServerError)


def test_maps_server_502() -> None:
    assert isinstance(error_from_response(response_with(502)), ServerError)


def test_maps_unmapped_4xx_to_base_type() -> None:
    assert type(error_from_response(response_with(418))) is APIStatusError


def test_status_error_exposes_status_code() -> None:
    assert error_from_response(response_with(404)).status_code == 404


def test_status_error_message_includes_code_and_url() -> None:
    message = str(error_from_response(response_with(404)))
    assert '404' in message
    assert 'https://example.com' in message


def test_status_error_truncates_long_body_preview() -> None:
    error = error_from_response(response_with(400, content=b'x' * 500))
    message = str(error)
    assert 'x' * BODY_PREVIEW_LENGTH_MAX in message
    assert 'x' * (BODY_PREVIEW_LENGTH_MAX + 1) not in message


def test_timeout_is_caught_as_connection_error() -> None:
    assert issubclass(NHLTimeoutError, NHLConnectionError)


def test_parameter_errors_are_caught_as_value_error() -> None:
    assert issubclass(InvalidParameterError, ValueError)


def test_every_error_is_caught_as_nhl_error() -> None:
    leaves = [
        NHLConnectionError,
        APIStatusError,
        InvalidParameterError,
        ResponseDecodeError,
        UnexpectedContentTypeError,
    ]
    assert all(issubclass(error, NHLError) for error in leaves)


def test_season_error_message_reports_value_and_minimum() -> None:
    message = str(InvalidSeasonError(20252027))
    assert '20252027' in message
    assert '1917' in message


def test_identifier_error_message_names_the_parameter() -> None:
    message = str(InvalidIdentifierError(0, 'player'))
    assert 'player' in message
    assert '0' in message


def test_response_process_wraps_bad_json() -> None:
    with pytest.raises(ResponseDecodeError):
        response_process(response_body('application/json', b'not json'))


def test_response_process_rejects_non_json() -> None:
    with pytest.raises(UnexpectedContentTypeError):
        response_process(response_body('text/html', b'<html></html>'))


def test_get_model_wraps_bad_json() -> None:
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            headers={'content-type': 'application/json'},
            content=b'not json',
        )

    client = NHL(client=httpx.Client(transport=httpx.MockTransport(handler)))

    with pytest.raises(ResponseDecodeError):
        client.standings.now()
