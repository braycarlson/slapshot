from __future__ import annotations

import pytest

from tests.support import FakeSyncRequester

from slapshot.exceptions import InvalidDateError
from slapshot.models import StandingsResponse
from slapshot.resources.standings import (
    Standings,
    standings_by_date,
    standings_now,
    standings_seasons,
)


BASE = 'https://api-web.nhle.com/v1'


def test_by_date_url() -> None:
    assert standings_by_date('2025-01-01').url == f'{BASE}/standings/2025-01-01'


def test_by_date_rejects_bad_date() -> None:
    with pytest.raises(InvalidDateError):
        standings_by_date('2025-13-01')


def test_now_url() -> None:
    assert standings_now().url == f'{BASE}/standings/now'


def test_seasons_url() -> None:
    assert standings_seasons().url == f'{BASE}/standings-season'


def test_resource_now_uses_model() -> None:
    fake = FakeSyncRequester()
    Standings(fake).now()
    assert fake.method == 'get_model'
    assert fake.model is StandingsResponse
    assert fake.request.url == f'{BASE}/standings/now'


def test_resource_by_date_uses_model() -> None:
    fake = FakeSyncRequester()
    Standings(fake).by_date('2025-01-01')
    assert fake.model is StandingsResponse
    assert fake.request.url == f'{BASE}/standings/2025-01-01'


def test_resource_seasons_uses_raw_get() -> None:
    fake = FakeSyncRequester()
    Standings(fake).seasons()
    assert fake.method == 'get'
    assert fake.request.url == f'{BASE}/standings-season'
