from __future__ import annotations

from typing_extensions import TYPE_CHECKING

if TYPE_CHECKING:
    import httpx


BODY_PREVIEW_LENGTH_MAX = 200
SEASON_YEAR_START_MIN = 1917


class NHLError(Exception):
    """The base class for all slapshot errors."""


class NHLConnectionError(NHLError):
    """The request failed to reach the API."""


class NHLTimeoutError(NHLConnectionError):
    """The request exceeded its timeout."""


class InvalidParameterError(NHLError, ValueError):
    """The base class for invalid parameter errors."""


class InvalidSeasonError(InvalidParameterError):
    """A season that is not two consecutive years."""

    def __init__(self, season: int) -> None:
        self.season = season
        super().__init__(
            f'season must be two consecutive years YYYYYYYY '
            f'starting at {SEASON_YEAR_START_MIN}: {season}'
        )


class InvalidDateError(InvalidParameterError):
    """A date that is not ISO format YYYY-MM-DD."""

    def __init__(self, date: str) -> None:
        self.date = date
        super().__init__(f'date must be ISO format YYYY-MM-DD: {date!r}')


class InvalidMonthError(InvalidParameterError):
    """A month that is not YYYY-MM."""

    def __init__(self, month: str) -> None:
        self.month = month
        super().__init__(f'month must be YYYY-MM with a month of 01 through 12: {month!r}')


class InvalidIdentifierError(InvalidParameterError):
    """An identifier that is not a positive integer."""

    def __init__(self, value: int, name: str) -> None:
        self.value = value
        self.name = name
        super().__init__(f'{name} must be a positive integer: {value}')


class InvalidLimitError(InvalidParameterError):
    """A limit that is not a positive integer."""

    def __init__(self, limit: int) -> None:
        self.limit = limit
        super().__init__(f'limit must be a positive integer: {limit}')


class InvalidStartError(InvalidParameterError):
    """A start offset that is negative."""

    def __init__(self, start: int) -> None:
        self.start = start
        super().__init__(f'start must be zero or greater: {start}')


class InvalidTimeoutError(InvalidParameterError):
    """A timeout that is not a positive number of seconds."""

    def __init__(self, timeout: float) -> None:
        self.timeout = timeout
        super().__init__(f'timeout must be a positive number of seconds: {timeout}')


class InvalidCayenneValueError(InvalidParameterError):
    """A cayenne string value that contains a double quote."""

    def __init__(self, value: str) -> None:
        self.value = value
        super().__init__(f'cayenne string value must not contain a double quote: {value!r}')


class InvalidQueryError(InvalidParameterError):
    """A search query that is empty."""

    def __init__(self) -> None:
        super().__init__('query must not be empty')


class InvalidDraftRoundError(InvalidParameterError):
    """A draft round that is less than one."""

    def __init__(self, draft_round: int) -> None:
        self.draft_round = draft_round
        super().__init__(f'draft_round must be at least 1: {draft_round}')


class ResponseDecodeError(NHLError):
    """The response body cannot be decoded."""

    def __init__(self, url: str) -> None:
        self.url = url
        super().__init__(f'could not decode the response body from {url}')


class UnexpectedContentTypeError(NHLError):
    """The response is not JSON."""

    def __init__(self, content_type: str, url: str) -> None:
        self.content_type = content_type
        self.url = url
        super().__init__(f'expected a JSON response but received {content_type!r} from {url}')


class APIStatusError(NHLError):
    """The base class for HTTP status errors."""

    def __init__(self, response: httpx.Response) -> None:
        self.response = response
        self.status_code = response.status_code
        body = response.text[:BODY_PREVIEW_LENGTH_MAX]
        super().__init__(f'{response.status_code} for {response.request.url}: {body}')


class BadRequestError(APIStatusError):
    """An HTTP 400 response."""


class ForbiddenError(APIStatusError):
    """An HTTP 403 response."""


class NotFoundError(APIStatusError):
    """An HTTP 404 response."""


class RateLimitError(APIStatusError):
    """An HTTP 429 response."""


class ServerError(APIStatusError):
    """An HTTP 5xx response."""


class UnauthorizedError(APIStatusError):
    """An HTTP 401 response."""


_STATUS_ERRORS = {
    400: BadRequestError,
    401: UnauthorizedError,
    403: ForbiddenError,
    404: NotFoundError,
    429: RateLimitError,
}


def error_from_response(response: httpx.Response) -> APIStatusError:
    error_type = _STATUS_ERRORS.get(response.status_code)

    if error_type is not None:
        return error_type(response)

    if response.status_code >= 500:
        return ServerError(response)

    return APIStatusError(response)
