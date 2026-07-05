from __future__ import annotations

import datetime

from slapshot.exceptions import (
    SEASON_YEAR_START_MIN,
    InvalidDateError,
    InvalidIdentifierError,
    InvalidLimitError,
    InvalidMonthError,
    InvalidSeasonError,
    InvalidStartError,
)


def season_validate(season: int) -> None:
    year_start = season // 10000
    year_end = season % 10000

    if year_end != year_start + 1 or year_start < SEASON_YEAR_START_MIN:
        raise InvalidSeasonError(season)


def date_validate(date: str) -> None:
    if len(date) != 10 or date[4] != '-' or date[7] != '-':
        raise InvalidDateError(date)

    try:
        datetime.date.fromisoformat(date)
    except ValueError as exception:
        raise InvalidDateError(date) from exception


def month_validate(month: str) -> None:
    year_part = month[:4]
    month_part = month[5:]

    if (
        len(month) != 7
        or month[4] != '-'
        or not year_part.isdigit()
        or not month_part.isdigit()
        or not 1 <= int(month_part) <= 12
    ):
        raise InvalidMonthError(month)


def identifier_validate(value: int, *, name: str) -> None:
    if value <= 0:
        raise InvalidIdentifierError(value, name)


def pagination_validate(limit: int, start: int) -> None:
    if limit <= 0:
        raise InvalidLimitError(limit)

    if start < 0:
        raise InvalidStartError(start)
