from __future__ import annotations

import pytest

from tests.support import FakeSyncRequester

from slapshot.enums import GameType, Team
from slapshot.exceptions import InvalidSeasonError
from slapshot.models import Roster
from slapshot.resources.teams import (
    Teams,
    club_stats,
    club_stats_seasons,
    prospects,
    roster,
    roster_seasons,
)


BASE = 'https://api-web.nhle.com/v1'


def test_club_stats_now_when_season_none() -> None:
    assert club_stats('TOR', None, GameType.REGULAR).url == f'{BASE}/club-stats/TOR/now'


def test_club_stats_with_season_and_game_type() -> None:
    assert club_stats('TOR', 20242025, GameType.REGULAR).url == f'{BASE}/club-stats/TOR/20242025/2'


def test_club_stats_accepts_int_game_type() -> None:
    assert club_stats('TOR', 20242025, 3).url == f'{BASE}/club-stats/TOR/20242025/3'


def test_club_stats_rejects_bad_season() -> None:
    with pytest.raises(InvalidSeasonError):
        club_stats('TOR', 20242030, GameType.REGULAR)


def test_club_stats_seasons_url() -> None:
    assert club_stats_seasons('TOR').url == f'{BASE}/club-stats-season/TOR'


def test_prospects_url() -> None:
    assert prospects('TOR').url == f'{BASE}/prospects/TOR'


def test_roster_current_when_season_none() -> None:
    assert roster('TOR', None).url == f'{BASE}/roster/TOR/current'


def test_roster_with_season() -> None:
    assert roster('TOR', 20242025).url == f'{BASE}/roster/TOR/20242025'


def test_roster_rejects_bad_season() -> None:
    with pytest.raises(InvalidSeasonError):
        roster('TOR', 20242030)


def test_roster_seasons_url() -> None:
    assert roster_seasons('TOR').url == f'{BASE}/roster-season/TOR'


def test_team_enum_serializes_to_abbreviation() -> None:
    assert prospects(Team.TORONTO).url == f'{BASE}/prospects/TOR'


def test_resource_club_stats_defaults_to_regular_season() -> None:
    fake = FakeSyncRequester()
    Teams(fake).club_stats('TOR', season=20242025)
    assert fake.method == 'get'
    assert fake.request.url == f'{BASE}/club-stats/TOR/20242025/2'


def test_resource_roster_uses_model() -> None:
    fake = FakeSyncRequester()
    Teams(fake).roster('TOR', season=20242025)
    assert fake.method == 'get_model'
    assert fake.model is Roster
    assert fake.request.url == f'{BASE}/roster/TOR/20242025'
