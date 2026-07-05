from __future__ import annotations

import json

import pytest

from typing_extensions import TYPE_CHECKING

from tests.support import FakeSyncRequester

from slapshot.enums import Language
from slapshot.exceptions import InvalidLimitError, InvalidSeasonError, InvalidStartError
from slapshot.models import ResultSet
from slapshot.resources.stats import (
    Stats,
    stats_config,
    stats_franchises,
    stats_glossary,
    stats_report,
    stats_seasons,
)

if TYPE_CHECKING:
    from slapshot.request import Request


BASE = 'https://api.nhle.com/stats/rest'

SKATER_SORT = json.dumps([{'property': 'points', 'direction': 'DESC'}])
GOALIE_SORT = json.dumps([{'property': 'wins', 'direction': 'DESC'}])


def report(**overrides: object) -> Request:
    kwargs: dict[str, object] = {
        'language': Language.ENGLISH,
        'subject': 'skater',
        'report': 'summary',
        'season': None,
        'game_type': None,
        'sort': None,
        'limit': 50,
        'start': 0,
        'aggregate': False,
        'game': False,
        'cayenne': None,
    }
    kwargs.update(overrides)
    return stats_report(**kwargs)


def test_config_url() -> None:
    assert stats_config(Language.ENGLISH).url == f'{BASE}/en/config'


def test_franchises_url() -> None:
    assert stats_franchises(Language.FRENCH).url == f'{BASE}/fr/franchise'


def test_glossary_url() -> None:
    assert stats_glossary(Language.ENGLISH).url == f'{BASE}/en/glossary'


def test_seasons_url() -> None:
    assert stats_seasons(Language.ENGLISH).url == f'{BASE}/en/season'


def test_report_url_and_default_params() -> None:
    request = report()
    assert request.url == f'{BASE}/en/skater/summary'
    assert request.params == {'limit': 50, 'start': 0}


def test_report_builds_cayenne_from_season_and_game_type() -> None:
    request = report(season=20242025, game_type=2)
    assert request.params['cayenneExp'] == 'seasonId=20242025 and gameTypeId=2'


def test_report_passes_string_cayenne_through() -> None:
    request = report(cayenne='goals>=10')
    assert request.params['cayenneExp'] == 'goals>=10'


def test_report_merges_dict_cayenne() -> None:
    request = report(season=20242025, cayenne={'nationalityCode': 'CAN'})
    assert request.params['cayenneExp'] == 'seasonId=20242025 and nationalityCode="CAN"'


def test_report_sets_flags() -> None:
    request = report(aggregate=True, game=True)
    assert request.params['isAggregate'] == 'true'
    assert request.params['isGame'] == 'true'


def test_report_passes_string_sort_through() -> None:
    assert report(sort='points').params['sort'] == 'points'


def test_report_encodes_sequence_sort() -> None:
    request = report(sort=({'property': 'goals', 'direction': 'ASC'},))
    assert request.params['sort'] == json.dumps([{'property': 'goals', 'direction': 'ASC'}])


def test_report_rejects_bad_limit() -> None:
    with pytest.raises(InvalidLimitError):
        report(limit=0)


def test_report_rejects_negative_start() -> None:
    with pytest.raises(InvalidStartError):
        report(start=-1)


def test_report_rejects_bad_season() -> None:
    with pytest.raises(InvalidSeasonError):
        report(season=20242030)


def test_resource_config_uses_raw_get() -> None:
    fake = FakeSyncRequester()
    Stats(fake).config()
    assert fake.method == 'get'
    assert fake.request.url == f'{BASE}/en/config'


def test_resource_franchises_uses_model() -> None:
    fake = FakeSyncRequester()
    Stats(fake).franchises()
    assert fake.method == 'get_model'
    assert fake.model is ResultSet
    assert fake.request.url == f'{BASE}/en/franchise'


def test_resource_skaters_injects_default_sort() -> None:
    fake = FakeSyncRequester()
    Stats(fake).skaters()
    assert fake.request.url == f'{BASE}/en/skater/summary'
    assert fake.request.params['sort'] == SKATER_SORT


def test_resource_goalies_injects_default_sort() -> None:
    fake = FakeSyncRequester()
    Stats(fake).goalies()
    assert fake.request.url == f'{BASE}/en/goalie/summary'
    assert fake.request.params['sort'] == GOALIE_SORT


def test_resource_teams_subject_and_default_sort() -> None:
    fake = FakeSyncRequester()
    Stats(fake).teams()
    assert fake.request.url == f'{BASE}/en/team/summary'
    assert fake.request.params['sort'] == json.dumps([{'property': 'points', 'direction': 'DESC'}])


def test_resource_report_omits_default_sort() -> None:
    fake = FakeSyncRequester()
    Stats(fake).report('skater', 'summary')
    assert 'sort' not in fake.request.params
