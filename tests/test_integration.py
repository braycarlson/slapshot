from __future__ import annotations

import pytest

from typing_extensions import Any, Callable

from tests.support import (
    VALID_EMPTY,
    VALID_LIST,
    VALID_PLAYER_LANDING,
    VALID_RESULT_SET,
    VALID_ROSTER,
    VALID_STANDINGS,
    Recorder,
    async_nhl,
    sync_nhl,
)

from slapshot.enums import Milestone


WEB = 'https://api-web.nhle.com/v1'
RECORDS = 'https://records.nhl.com/site/api'
STATS = 'https://api.nhle.com/stats/rest'
SEARCH = 'https://search.d3.nhle.com/api/v1'

GAME = 2023020001
PLAYER = 8478402

CLEAN_CASES = [
    (VALID_EMPTY, lambda nhl: nhl.draft.picks(), f'{WEB}/draft/picks/now'),
    (VALID_EMPTY, lambda nhl: nhl.draft.picks(2023, draft_round=2), f'{WEB}/draft/picks/2023/2'),
    (VALID_EMPTY, lambda nhl: nhl.draft.rankings(), f'{WEB}/draft/rankings/now'),
    (VALID_EMPTY, lambda nhl: nhl.draft.rankings(2023, category=2), f'{WEB}/draft/rankings/2023/2'),
    (VALID_EMPTY, lambda nhl: nhl.games.boxscore(GAME), f'{WEB}/gamecenter/{GAME}/boxscore'),
    (VALID_EMPTY, lambda nhl: nhl.games.landing(GAME), f'{WEB}/gamecenter/{GAME}/landing'),
    (
        VALID_EMPTY,
        lambda nhl: nhl.games.play_by_play(GAME),
        f'{WEB}/gamecenter/{GAME}/play-by-play',
    ),
    (VALID_EMPTY, lambda nhl: nhl.games.right_rail(GAME), f'{WEB}/gamecenter/{GAME}/right-rail'),
    (VALID_EMPTY, lambda nhl: nhl.games.story(GAME), f'{WEB}/wsc/game-story/{GAME}'),
    (VALID_EMPTY, lambda nhl: nhl.games.scoreboard(), f'{WEB}/scoreboard/now'),
    (VALID_EMPTY, lambda nhl: nhl.games.scores(), f'{WEB}/score/now'),
    (VALID_EMPTY, lambda nhl: nhl.games.scores('2025-01-01'), f'{WEB}/score/2025-01-01'),
    (VALID_EMPTY, lambda nhl: nhl.players.game_log(PLAYER), f'{WEB}/player/{PLAYER}/game-log/now'),
    (
        VALID_PLAYER_LANDING,
        lambda nhl: nhl.players.landing(PLAYER),
        f'{WEB}/player/{PLAYER}/landing',
    ),
    (VALID_EMPTY, lambda nhl: nhl.players.spotlight(), f'{WEB}/player-spotlight'),
    (
        VALID_RESULT_SET,
        lambda nhl: nhl.records.all_time_record(),
        f'{RECORDS}/all-time-record-vs-franchise',
    ),
    (VALID_RESULT_SET, lambda nhl: nhl.records.attendance(), f'{RECORDS}/attendance'),
    (VALID_RESULT_SET, lambda nhl: nhl.records.draft(), f'{RECORDS}/draft'),
    (VALID_RESULT_SET, lambda nhl: nhl.records.franchise_details(), f'{RECORDS}/franchise-detail'),
    (
        VALID_RESULT_SET,
        lambda nhl: nhl.records.franchise_goalie_records(),
        f'{RECORDS}/franchise-goalie-records',
    ),
    (
        VALID_RESULT_SET,
        lambda nhl: nhl.records.franchise_season_records(),
        f'{RECORDS}/franchise-season-records',
    ),
    (
        VALID_RESULT_SET,
        lambda nhl: nhl.records.franchise_season_results(),
        f'{RECORDS}/franchise-season-results',
    ),
    (
        VALID_RESULT_SET,
        lambda nhl: nhl.records.franchise_skater_records(),
        f'{RECORDS}/franchise-skater-records',
    ),
    (
        VALID_RESULT_SET,
        lambda nhl: nhl.records.franchise_team_totals(),
        f'{RECORDS}/franchise-team-totals',
    ),
    (VALID_RESULT_SET, lambda nhl: nhl.records.franchises(), f'{RECORDS}/franchise'),
    (
        VALID_RESULT_SET,
        lambda nhl: nhl.records.milestone(Milestone.GOAL_SEASON_50),
        f'{RECORDS}/milestone-50-goal-season',
    ),
    (VALID_RESULT_SET, lambda nhl: nhl.records.officials(), f'{RECORDS}/officials'),
    (VALID_RESULT_SET, lambda nhl: nhl.records.players(), f'{RECORDS}/player'),
    (VALID_RESULT_SET, lambda nhl: nhl.records.playoff_series(), f'{RECORDS}/playoff-series'),
    (VALID_RESULT_SET, lambda nhl: nhl.records.trophies(), f'{RECORDS}/trophy'),
    (VALID_EMPTY, lambda nhl: nhl.schedule.by_date('2025-01-01'), f'{WEB}/schedule/2025-01-01'),
    (VALID_EMPTY, lambda nhl: nhl.schedule.club_month('TOR'), f'{WEB}/club-schedule/TOR/month/now'),
    (
        VALID_EMPTY,
        lambda nhl: nhl.schedule.club_season('TOR', 20242025),
        f'{WEB}/club-schedule-season/TOR/20242025',
    ),
    (VALID_EMPTY, lambda nhl: nhl.schedule.club_week('TOR'), f'{WEB}/club-schedule/TOR/week/now'),
    (VALID_EMPTY, lambda nhl: nhl.schedule.now(), f'{WEB}/schedule/now'),
    (
        VALID_STANDINGS,
        lambda nhl: nhl.standings.by_date('2025-01-01'),
        f'{WEB}/standings/2025-01-01',
    ),
    (VALID_STANDINGS, lambda nhl: nhl.standings.now(), f'{WEB}/standings/now'),
    (VALID_EMPTY, lambda nhl: nhl.standings.seasons(), f'{WEB}/standings-season'),
    (
        VALID_EMPTY,
        lambda nhl: nhl.teams.club_stats('TOR', season=20242025),
        f'{WEB}/club-stats/TOR/20242025/2',
    ),
    (VALID_EMPTY, lambda nhl: nhl.teams.club_stats('TOR'), f'{WEB}/club-stats/TOR/now'),
    (VALID_EMPTY, lambda nhl: nhl.teams.club_stats_seasons('TOR'), f'{WEB}/club-stats-season/TOR'),
    (VALID_EMPTY, lambda nhl: nhl.teams.prospects('TOR'), f'{WEB}/prospects/TOR'),
    (
        VALID_ROSTER,
        lambda nhl: nhl.teams.roster('TOR', season=20242025),
        f'{WEB}/roster/TOR/20242025',
    ),
    (VALID_ROSTER, lambda nhl: nhl.teams.roster('TOR'), f'{WEB}/roster/TOR/current'),
    (VALID_EMPTY, lambda nhl: nhl.teams.roster_seasons('TOR'), f'{WEB}/roster-season/TOR'),
    (VALID_EMPTY, lambda nhl: nhl.stats.config(), f'{STATS}/en/config'),
    (VALID_RESULT_SET, lambda nhl: nhl.stats.franchises(), f'{STATS}/en/franchise'),
    (VALID_RESULT_SET, lambda nhl: nhl.stats.glossary(), f'{STATS}/en/glossary'),
    (VALID_RESULT_SET, lambda nhl: nhl.stats.seasons(), f'{STATS}/en/season'),
]

PARAM_CASES = [
    (VALID_EMPTY, lambda nhl: nhl.players.goalie_leaders(), '/v1/goalie-stats-leaders/current'),
    (VALID_EMPTY, lambda nhl: nhl.players.skater_leaders(), '/v1/skater-stats-leaders/current'),
    (VALID_LIST, lambda nhl: nhl.players.search('mcdavid'), '/api/v1/search/player'),
    (VALID_RESULT_SET, lambda nhl: nhl.stats.skaters(), '/stats/rest/en/skater/summary'),
    (VALID_RESULT_SET, lambda nhl: nhl.stats.goalies(), '/stats/rest/en/goalie/summary'),
    (VALID_RESULT_SET, lambda nhl: nhl.stats.teams(), '/stats/rest/en/team/summary'),
    (
        VALID_RESULT_SET,
        lambda nhl: nhl.stats.report('skater', 'summary'),
        '/stats/rest/en/skater/summary',
    ),
]


@pytest.mark.parametrize(('payload', 'call', 'expected'), CLEAN_CASES)
def test_sync_final_url(payload: bytes, call: Callable[[Any], Any], expected: str) -> None:
    recorder = Recorder(payload)
    call(sync_nhl(recorder))
    assert recorder.url == expected


@pytest.mark.parametrize(('payload', 'call', 'expected'), CLEAN_CASES)
async def test_async_final_url(payload: bytes, call: Callable[[Any], Any], expected: str) -> None:
    recorder = Recorder(payload)
    await call(async_nhl(recorder))
    assert recorder.url == expected


@pytest.mark.parametrize(('payload', 'call', 'expected'), PARAM_CASES)
def test_sync_final_path(payload: bytes, call: Callable[[Any], Any], expected: str) -> None:
    recorder = Recorder(payload)
    call(sync_nhl(recorder))
    assert recorder.path == expected


@pytest.mark.parametrize(('payload', 'call', 'expected'), PARAM_CASES)
async def test_async_final_path(payload: bytes, call: Callable[[Any], Any], expected: str) -> None:
    recorder = Recorder(payload)
    await call(async_nhl(recorder))
    assert recorder.path == expected
