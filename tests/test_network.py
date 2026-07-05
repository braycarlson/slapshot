from __future__ import annotations

import pytest

from slapshot.client import NHL, AsyncNHL
from slapshot.enums import Team
from slapshot.models import PlayerSearchResult, ResultSet, Roster, StandingsResponse


pytestmark = pytest.mark.network


def test_standings_now() -> None:
    with NHL() as nhl:
        value = nhl.standings.now()
    assert isinstance(value, StandingsResponse)
    assert value.standings


def test_roster() -> None:
    with NHL() as nhl:
        value = nhl.teams.roster(Team.TORONTO)
    assert isinstance(value, Roster)


def test_player_search() -> None:
    with NHL() as nhl:
        results = nhl.players.search('mcdavid')
    assert results
    assert isinstance(results[0], PlayerSearchResult)


def test_stats_franchises() -> None:
    with NHL() as nhl:
        value = nhl.stats.franchises()
    assert isinstance(value, ResultSet)
    assert value.total > 0


def test_scores_now_is_json() -> None:
    with NHL() as nhl:
        value = nhl.games.scores()
    assert isinstance(value, dict)


async def test_async_standings_now() -> None:
    async with AsyncNHL() as nhl:
        value = await nhl.standings.now()
    assert isinstance(value, StandingsResponse)
    assert value.standings
