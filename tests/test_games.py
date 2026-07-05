from __future__ import annotations

import pytest

from typing_extensions import Callable, TYPE_CHECKING

from tests.support import FakeSyncRequester

from slapshot.exceptions import InvalidDateError, InvalidIdentifierError
from slapshot.resources.games import (
    Games,
    game_boxscore,
    game_landing,
    game_play_by_play,
    game_right_rail,
    game_story,
    scoreboard_now,
    scores_by_date,
)

if TYPE_CHECKING:
    from slapshot.request import Request


BASE = 'https://api-web.nhle.com/v1'

GAME_BUILDERS = [
    (game_boxscore, 'boxscore'),
    (game_landing, 'landing'),
    (game_play_by_play, 'play-by-play'),
    (game_right_rail, 'right-rail'),
]


@pytest.mark.parametrize(('builder', 'suffix'), GAME_BUILDERS)
def test_game_builder_url(builder: Callable[[int], Request], suffix: str) -> None:
    assert builder(123).url == f'{BASE}/gamecenter/123/{suffix}'


@pytest.mark.parametrize('builder', [builder for builder, _ in GAME_BUILDERS])
def test_game_builder_rejects_zero(builder: Callable[[int], Request]) -> None:
    with pytest.raises(InvalidIdentifierError):
        builder(0)


def test_story_url() -> None:
    assert game_story(123).url == f'{BASE}/wsc/game-story/123'


def test_story_rejects_zero() -> None:
    with pytest.raises(InvalidIdentifierError):
        game_story(0)


def test_scoreboard_now_url() -> None:
    assert scoreboard_now().url == f'{BASE}/scoreboard/now'


def test_scores_now_when_date_none() -> None:
    assert scores_by_date(None).url == f'{BASE}/score/now'


def test_scores_by_date() -> None:
    assert scores_by_date('2025-01-01').url == f'{BASE}/score/2025-01-01'


def test_scores_rejects_bad_date() -> None:
    with pytest.raises(InvalidDateError):
        scores_by_date('2025-13-01')


def test_resource_boxscore_delegates_to_get() -> None:
    fake = FakeSyncRequester()
    Games(fake).boxscore(123)
    assert fake.method == 'get'
    assert fake.request.url == f'{BASE}/gamecenter/123/boxscore'


def test_resource_scores_defaults_to_now() -> None:
    fake = FakeSyncRequester()
    Games(fake).scores()
    assert fake.request.url == f'{BASE}/score/now'
