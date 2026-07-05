from __future__ import annotations

import pytest

from tests.support import FakeSyncRequester

from slapshot.enums import Team
from slapshot.exceptions import InvalidDateError, InvalidMonthError, InvalidSeasonError
from slapshot.resources.schedule import (
    Schedule,
    schedule_by_date,
    schedule_club_month,
    schedule_club_season,
    schedule_club_week,
    schedule_now,
)


BASE = 'https://api-web.nhle.com/v1'


def test_by_date_url() -> None:
    assert schedule_by_date('2025-01-01').url == f'{BASE}/schedule/2025-01-01'


def test_by_date_rejects_bad_date() -> None:
    with pytest.raises(InvalidDateError):
        schedule_by_date('2025-13-01')


def test_club_month_now_when_month_none() -> None:
    assert schedule_club_month('TOR', None).url == f'{BASE}/club-schedule/TOR/month/now'


def test_club_month_with_month() -> None:
    assert schedule_club_month('TOR', '2025-01').url == f'{BASE}/club-schedule/TOR/month/2025-01'


def test_club_month_rejects_bad_month() -> None:
    with pytest.raises(InvalidMonthError):
        schedule_club_month('TOR', '2025-13')


def test_club_season_url() -> None:
    assert schedule_club_season('TOR', 20242025).url == f'{BASE}/club-schedule-season/TOR/20242025'


def test_club_season_rejects_bad_season() -> None:
    with pytest.raises(InvalidSeasonError):
        schedule_club_season('TOR', 20242030)


def test_club_week_now_when_date_none() -> None:
    assert schedule_club_week('TOR', None).url == f'{BASE}/club-schedule/TOR/week/now'


def test_club_week_with_date() -> None:
    assert (
        schedule_club_week('TOR', '2025-01-01').url == f'{BASE}/club-schedule/TOR/week/2025-01-01'
    )


def test_club_week_rejects_bad_date() -> None:
    with pytest.raises(InvalidDateError):
        schedule_club_week('TOR', '2025-13-01')


def test_now_url() -> None:
    assert schedule_now().url == f'{BASE}/schedule/now'


def test_team_enum_serializes_to_abbreviation() -> None:
    expected = f'{BASE}/club-schedule-season/TOR/20242025'
    assert schedule_club_season(Team.TORONTO, 20242025).url == expected


def test_resource_club_month_defaults_to_now() -> None:
    fake = FakeSyncRequester()
    Schedule(fake).club_month('TOR')
    assert fake.method == 'get'
    assert fake.request.url == f'{BASE}/club-schedule/TOR/month/now'


def test_resource_club_week_defaults_to_now() -> None:
    fake = FakeSyncRequester()
    Schedule(fake).club_week('TOR')
    assert fake.request.url == f'{BASE}/club-schedule/TOR/week/now'
