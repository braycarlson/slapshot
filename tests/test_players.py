from __future__ import annotations

import pytest

from tests.support import FakeSyncRequester

from slapshot.enums import GameType
from slapshot.exceptions import (
    InvalidIdentifierError,
    InvalidLimitError,
    InvalidQueryError,
    InvalidSeasonError,
)
from slapshot.models import PlayerLanding, PlayerSearchResult
from slapshot.resources.players import (
    Players,
    goalie_leaders,
    player_game_log,
    player_landing,
    player_search,
    player_spotlight,
    skater_leaders,
)


BASE_WEB = 'https://api-web.nhle.com/v1'
BASE_SEARCH = 'https://search.d3.nhle.com/api/v1'


def test_goalie_leaders_current_when_season_none() -> None:
    request = goalie_leaders(None, GameType.REGULAR, None, 5)
    assert request.url == f'{BASE_WEB}/goalie-stats-leaders/current'
    assert request.params == {'limit': 5}


def test_goalie_leaders_with_season() -> None:
    request = goalie_leaders(20242025, GameType.REGULAR, 'goals', 10)
    assert request.url == f'{BASE_WEB}/goalie-stats-leaders/20242025/2'
    assert request.params == {'categories': 'goals', 'limit': 10}


def test_goalie_leaders_rejects_bad_limit() -> None:
    with pytest.raises(InvalidLimitError):
        goalie_leaders(None, GameType.REGULAR, None, 0)


def test_skater_leaders_current_when_season_none() -> None:
    request = skater_leaders(None, GameType.REGULAR, None, 5)
    assert request.url == f'{BASE_WEB}/skater-stats-leaders/current'
    assert request.params == {'limit': 5}


def test_skater_leaders_with_season() -> None:
    request = skater_leaders(20242025, GameType.PLAYOFF, 'points', 3)
    assert request.url == f'{BASE_WEB}/skater-stats-leaders/20242025/3'
    assert request.params == {'categories': 'points', 'limit': 3}


def test_leaders_reject_bad_season() -> None:
    with pytest.raises(InvalidSeasonError):
        skater_leaders(20242030, GameType.REGULAR, None, 5)


def test_game_log_now_when_season_none() -> None:
    assert (
        player_game_log(8478402, None, GameType.REGULAR).url
        == f'{BASE_WEB}/player/8478402/game-log/now'
    )


def test_game_log_with_season() -> None:
    request = player_game_log(8478402, 20242025, GameType.REGULAR)
    assert request.url == f'{BASE_WEB}/player/8478402/game-log/20242025/2'


def test_game_log_rejects_nonpositive_player() -> None:
    with pytest.raises(InvalidIdentifierError):
        player_game_log(0, None, GameType.REGULAR)


def test_landing_url() -> None:
    assert player_landing(8478402).url == f'{BASE_WEB}/player/8478402/landing'


def test_landing_rejects_nonpositive_player() -> None:
    with pytest.raises(InvalidIdentifierError):
        player_landing(0)


def test_search_url_and_params() -> None:
    request = player_search('mcdavid', 20, None, 'en-us')
    assert request.url == f'{BASE_SEARCH}/search/player'
    assert request.params == {'culture': 'en-us', 'q': 'mcdavid', 'limit': 20}


def test_search_keeps_active_flag() -> None:
    request = player_search('mcdavid', 20, active=True, culture='en-us')
    assert request.params == {'culture': 'en-us', 'q': 'mcdavid', 'limit': 20, 'active': True}


def test_search_rejects_empty_query() -> None:
    with pytest.raises(InvalidQueryError):
        player_search('', 20, None, 'en-us')


def test_search_rejects_bad_limit() -> None:
    with pytest.raises(InvalidLimitError):
        player_search('mcdavid', 0, None, 'en-us')


def test_spotlight_url() -> None:
    assert player_spotlight().url == f'{BASE_WEB}/player-spotlight'


def test_resource_landing_uses_model() -> None:
    fake = FakeSyncRequester()
    Players(fake).landing(8478402)
    assert fake.method == 'get_model'
    assert fake.model is PlayerLanding


def test_resource_search_uses_list_model() -> None:
    fake = FakeSyncRequester()
    Players(fake).search('mcdavid')
    assert fake.model == list[PlayerSearchResult]
    assert fake.request.params == {'culture': 'en-us', 'q': 'mcdavid', 'limit': 20}


def test_resource_game_log_defaults_to_now() -> None:
    fake = FakeSyncRequester()
    Players(fake).game_log(8478402)
    assert fake.method == 'get'
    assert fake.request.url == f'{BASE_WEB}/player/8478402/game-log/now'


def test_resource_skater_leaders_default_limit() -> None:
    fake = FakeSyncRequester()
    Players(fake).skater_leaders()
    assert fake.request.params == {'limit': 5}
