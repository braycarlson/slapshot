from __future__ import annotations

import json

from typing_extensions import Any, NamedTuple, Sequence

from slapshot.exceptions import InvalidCayenneValueError


class Request(NamedTuple):
    """A prepared request: a URL and its query parameters."""

    url: str
    params: dict[str, Any]


def request_build(url: str, params: dict[str, Any] | None = None) -> Request:
    """It builds a request, dropping any parameter whose value is None.

    Args:
        url: The fully formed request URL.
        params: Query parameters. Entries with a value of None are removed.

    Returns:
        A request holding the URL and the filtered parameters.
    """

    if params is None:
        return Request(url, {})

    filtered = {key: value for key, value in params.items() if value is not None}

    return Request(url, filtered)


def cayenne_build_value(value: Any) -> str:
    """It formats a single value for a cayenne expression.

    A boolean renders as true or false, and a string is quoted.

    Args:
        value: The value to format.

    Returns:
        The formatted value.

    Raises:
        InvalidCayenneValueError: If a string value contains a double quote.
    """

    if isinstance(value, bool):
        return 'true' if value else 'false'

    if isinstance(value, str):
        if '"' in value:
            raise InvalidCayenneValueError(value)

        return f'"{value}"'

    return str(value)


def cayenne_build(conditions: dict[str, Any]) -> str | None:
    """It joins conditions into a cayenne expression, skipping None values.

    Args:
        conditions: A mapping of field names to filter values.

    Returns:
        The joined expression, or None when no conditions remain.
    """

    clauses = [
        f'{key}={cayenne_build_value(value)}'
        for key, value in conditions.items()
        if value is not None
    ]

    if not clauses:
        return None

    return ' and '.join(clauses)


def sort_build(sort: str | Sequence[dict[str, str]] | None) -> str | None:
    """It serializes a sort specification to the string the API expects.

    Args:
        sort: A property name, a sequence of property and direction mappings,
            or None.

    Returns:
        The sort string, or None when no sort is given.
    """

    if sort is None:
        return None

    if isinstance(sort, str):
        return sort

    return json.dumps(list(sort))
