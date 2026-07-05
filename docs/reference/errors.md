# Errors

## Overview

Every error raised by slapshot inherits from `NHLError`, so a single `except NHLError` catches transport failures, HTTP status errors, decode failures, and invalid arguments. The more specific classes let you handle one failure without catching the others.

```python
from slapshot import NHLError
```

## Hierarchy

```
NHLError
├── NHLConnectionError
│   └── NHLTimeoutError
├── InvalidParameterError            (also a ValueError)
│   ├── InvalidSeasonError
│   ├── InvalidDateError
│   ├── InvalidMonthError
│   ├── InvalidIdentifierError
│   ├── InvalidLimitError
│   ├── InvalidStartError
│   ├── InvalidTimeoutError
│   ├── InvalidCayenneValueError
│   ├── InvalidQueryError
│   └── InvalidDraftRoundError
├── ResponseDecodeError
├── UnexpectedContentTypeError
└── APIStatusError
    ├── BadRequestError              (400)
    ├── UnauthorizedError            (401)
    ├── ForbiddenError               (403)
    ├── NotFoundError                (404)
    ├── RateLimitError               (429)
    └── ServerError                  (5xx)
```

`NHLError`, its transport and decode subclasses, `InvalidParameterError`, and every `APIStatusError` subclass are importable from the package root. The granular parameter subclasses (`InvalidSeasonError` and the others) live in `slapshot.exceptions`.

## Transport Errors

Raised when the request never produces an HTTP response.

| Error | Raised when |
|-------|-------------|
| `NHLConnectionError` | The request fails to reach the API. |
| `NHLTimeoutError` | The request exceeds its timeout. Subclass of `NHLConnectionError`. |

## HTTP Status Errors

Raised when the API returns a status of 400 or greater. Each carries the originating `httpx.Response` on `response` and the code on `status_code`.

| Error | Status |
|-------|--------|
| `BadRequestError` | 400 |
| `UnauthorizedError` | 401 |
| `ForbiddenError` | 403 |
| `NotFoundError` | 404 |
| `RateLimitError` | 429 |
| `ServerError` | 500 and above |
| `APIStatusError` | Any other status of 400 or greater. Base class of the above. |

## Response Errors

Raised when a response arrives but its body is unusable.

| Error | Raised when |
|-------|-------------|
| `UnexpectedContentTypeError` | The response is not JSON. Carries `content_type` and `url`. |
| `ResponseDecodeError` | The body cannot be decoded, or does not match the expected model. Carries `url`. |

## Parameter Errors

Raised before a request is sent, when an argument fails validation. `InvalidParameterError` also subclasses `ValueError`, so existing `except ValueError` handlers keep working.

| Error | Raised when |
|-------|-------------|
| `InvalidSeasonError` | `season` is not two consecutive years, `YYYYYYYY`, starting at 1917. |
| `InvalidDateError` | `date` is not ISO format `YYYY-MM-DD`. |
| `InvalidMonthError` | `month` is not `YYYY-MM` with a month of 01 through 12. |
| `InvalidIdentifierError` | An identifier such as `player`, `game`, `team`, `franchise`, or `year` is not a positive integer. |
| `InvalidLimitError` | `limit` is not a positive integer. |
| `InvalidStartError` | `start` is negative. |
| `InvalidTimeoutError` | `timeout` is not a positive number of seconds. |
| `InvalidCayenneValueError` | A cayenne string value contains a double quote. |
| `InvalidQueryError` | A search `query` is empty. |
| `InvalidDraftRoundError` | `draft_round` is less than 1. |

## Handling Errors

Catch a specific failure, then fall back to the base class:

```python
from slapshot import NHL, NHLError, NotFoundError, RateLimitError

with NHL() as client:
    try:
        player = client.players.landing(8478402)
    except NotFoundError:
        print('No such player')
    except RateLimitError:
        print('Rate limited; back off and retry')
    except NHLError as error:
        print('Request failed:', error)
```

Because parameter errors are also `ValueError`, you can validate input with either name:

```python
from slapshot import NHL, InvalidParameterError

with NHL() as client:
    try:
        client.standings.by_date('2025/01/15')
    except InvalidParameterError as error:
        print('Bad argument:', error)
```
