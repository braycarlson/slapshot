from __future__ import annotations

import pytest

from slapshot.client import NHL, AsyncNHL
from slapshot.exceptions import InvalidParameterError
from slapshot.validation import (
    date_validate,
    identifier_validate,
    month_validate,
    pagination_validate,
    season_validate,
)


def test_season_accepts_consecutive() -> None:
    assert season_validate(20252026) is None


def test_season_accepts_earliest() -> None:
    assert season_validate(19171918) is None


def test_season_rejects_gap() -> None:
    with pytest.raises(InvalidParameterError):
        season_validate(20252027)


def test_season_rejects_same_year() -> None:
    with pytest.raises(InvalidParameterError):
        season_validate(20252025)


def test_season_rejects_too_early() -> None:
    with pytest.raises(InvalidParameterError):
        season_validate(19161917)


def test_date_accepts_iso() -> None:
    assert date_validate('2025-01-01') is None


def test_date_accepts_leap_day() -> None:
    assert date_validate('2024-02-29') is None


def test_date_rejects_empty() -> None:
    with pytest.raises(InvalidParameterError):
        date_validate('')


def test_date_rejects_bad_month() -> None:
    with pytest.raises(InvalidParameterError):
        date_validate('2025-13-01')


def test_date_rejects_impossible_day() -> None:
    with pytest.raises(InvalidParameterError):
        date_validate('2025-02-30')


def test_date_rejects_unpadded() -> None:
    with pytest.raises(InvalidParameterError):
        date_validate('2025-1-1')


def test_date_rejects_basic_iso_without_dashes() -> None:
    with pytest.raises(InvalidParameterError):
        date_validate('20250101')


def test_date_rejects_iso_week_date() -> None:
    with pytest.raises(InvalidParameterError):
        date_validate('2025-W01-1')


def test_date_rejects_datetime() -> None:
    with pytest.raises(InvalidParameterError):
        date_validate('2025-01-01T00:00')


def test_month_accepts() -> None:
    assert month_validate('2025-01') is None


def test_month_accepts_december() -> None:
    assert month_validate('2025-12') is None


def test_month_rejects_zero_month() -> None:
    with pytest.raises(InvalidParameterError):
        month_validate('2025-00')


def test_month_rejects_bad_month() -> None:
    with pytest.raises(InvalidParameterError):
        month_validate('2025-13')


def test_month_rejects_wrong_shape() -> None:
    with pytest.raises(InvalidParameterError):
        month_validate('2025-1')


def test_month_rejects_missing_separator() -> None:
    with pytest.raises(InvalidParameterError):
        month_validate('2025001')


def test_month_rejects_non_digit_year() -> None:
    with pytest.raises(InvalidParameterError):
        month_validate('abcd-01')


def test_identifier_accepts_positive() -> None:
    assert identifier_validate(1, name='player') is None


def test_identifier_rejects_zero() -> None:
    with pytest.raises(InvalidParameterError):
        identifier_validate(0, name='player')


def test_identifier_rejects_negative() -> None:
    with pytest.raises(InvalidParameterError):
        identifier_validate(-5, name='player')


def test_pagination_accepts() -> None:
    assert pagination_validate(5, 0) is None


def test_pagination_accepts_zero_start() -> None:
    assert pagination_validate(1, 0) is None


def test_pagination_rejects_zero_limit() -> None:
    with pytest.raises(InvalidParameterError):
        pagination_validate(0, 0)


def test_pagination_rejects_negative_limit() -> None:
    with pytest.raises(InvalidParameterError):
        pagination_validate(-1, 0)


def test_pagination_rejects_negative_start() -> None:
    with pytest.raises(InvalidParameterError):
        pagination_validate(5, -1)


def test_timeout_sync_rejects_zero() -> None:
    with pytest.raises(InvalidParameterError):
        NHL(timeout=0)


def test_timeout_sync_rejects_negative() -> None:
    with pytest.raises(InvalidParameterError):
        NHL(timeout=-1)


def test_timeout_async_rejects_zero() -> None:
    with pytest.raises(InvalidParameterError):
        AsyncNHL(timeout=0)
