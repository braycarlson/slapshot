from __future__ import annotations

import json

from tests.support import FakeAsyncRequester

from slapshot.models import PlayerLanding, PlayerSearchResult, ResultSet, Roster, StandingsResponse
from slapshot.resources.draft import AsyncDraft
from slapshot.resources.games import AsyncGames
from slapshot.resources.players import AsyncPlayers
from slapshot.resources.records import AsyncRecords
from slapshot.resources.schedule import AsyncSchedule
from slapshot.resources.standings import AsyncStandings
from slapshot.resources.stats import AsyncStats
from slapshot.resources.teams import AsyncTeams


WEB = 'https://api-web.nhle.com/v1'


async def test_async_draft_uses_raw_get() -> None:
    fake = FakeAsyncRequester()
    await AsyncDraft(fake).picks(2023, draft_round=1)
    assert fake.method == 'get'
    assert fake.request.url == f'{WEB}/draft/picks/2023/1'


async def test_async_games_uses_raw_get() -> None:
    fake = FakeAsyncRequester()
    await AsyncGames(fake).boxscore(2023020001)
    assert fake.method == 'get'
    assert fake.request.url == f'{WEB}/gamecenter/2023020001/boxscore'


async def test_async_schedule_uses_raw_get() -> None:
    fake = FakeAsyncRequester()
    await AsyncSchedule(fake).now()
    assert fake.method == 'get'
    assert fake.request.url == f'{WEB}/schedule/now'


async def test_async_standings_uses_model() -> None:
    fake = FakeAsyncRequester()
    await AsyncStandings(fake).now()
    assert fake.method == 'get_model'
    assert fake.model is StandingsResponse


async def test_async_teams_roster_uses_model() -> None:
    fake = FakeAsyncRequester()
    await AsyncTeams(fake).roster('TOR', season=20242025)
    assert fake.model is Roster


async def test_async_players_landing_uses_model() -> None:
    fake = FakeAsyncRequester()
    await AsyncPlayers(fake).landing(8478402)
    assert fake.model is PlayerLanding


async def test_async_players_search_uses_list_model() -> None:
    fake = FakeAsyncRequester()
    await AsyncPlayers(fake).search('mcdavid')
    assert fake.model == list[PlayerSearchResult]


async def test_async_records_uses_model() -> None:
    fake = FakeAsyncRequester()
    await AsyncRecords(fake).franchises()
    assert fake.model is ResultSet


async def test_async_stats_uses_model() -> None:
    fake = FakeAsyncRequester()
    await AsyncStats(fake).franchises()
    assert fake.model is ResultSet


async def test_async_stats_injects_default_sort() -> None:
    fake = FakeAsyncRequester()
    await AsyncStats(fake).skaters()
    assert fake.request.params['sort'] == json.dumps([{'property': 'points', 'direction': 'DESC'}])
