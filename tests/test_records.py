from __future__ import annotations

import pytest

from tests.support import FakeSyncRequester

from slapshot.endpoints import RecordsEndpoint
from slapshot.enums import Milestone, SortDirection
from slapshot.exceptions import InvalidIdentifierError, InvalidSeasonError
from slapshot.models import ResultSet
from slapshot.resources.records import (
    Records,
    records_attendance,
    records_draft,
    records_franchise_report,
    records_milestone,
    records_officials,
    records_players,
    records_playoff_series,
    records_trophies,
    records_versus_franchise,
)


BASE = 'https://records.nhl.com/site/api'


def test_franchise_report_empty_when_all_none() -> None:
    request = records_franchise_report(RecordsEndpoint.FRANCHISES, None, None, None, None, None)
    assert request.url == f'{BASE}/franchise'
    assert request.params == {}


def test_franchise_report_builds_cayenne() -> None:
    request = records_franchise_report(
        RecordsEndpoint.FRANCHISE_SKATER_RECORDS, 1, 10, 20242025, None, None
    )
    assert request.url == f'{BASE}/franchise-skater-records'
    assert request.params == {
        'cayenneExp': 'franchiseId=1 and mostRecentTeamId=10 and seasonId=20242025'
    }


def test_franchise_report_sort_and_direction() -> None:
    request = records_franchise_report(
        RecordsEndpoint.FRANCHISES, None, None, None, 'wins', SortDirection.DESCENDING
    )
    assert request.params == {'sort': 'wins', 'dir': 'DESC'}


def test_franchise_report_uppercases_string_direction() -> None:
    request = records_franchise_report(RecordsEndpoint.FRANCHISES, None, None, None, 'wins', 'asc')
    assert request.params['dir'] == 'ASC'


def test_franchise_report_rejects_bad_franchise() -> None:
    with pytest.raises(InvalidIdentifierError):
        records_franchise_report(RecordsEndpoint.FRANCHISES, 0, None, None, None, None)


def test_franchise_report_rejects_bad_season() -> None:
    with pytest.raises(InvalidSeasonError):
        records_franchise_report(RecordsEndpoint.FRANCHISES, None, None, 20242030, None, None)


def test_versus_franchise_empty_when_none() -> None:
    request = records_versus_franchise(RecordsEndpoint.ALL_TIME_RECORD, None, None)
    assert request.url == f'{BASE}/all-time-record-vs-franchise'
    assert request.params == {}


def test_versus_franchise_builds_cayenne() -> None:
    request = records_versus_franchise(RecordsEndpoint.ALL_TIME_RECORD, 5, 2)
    assert request.params == {'cayenneExp': 'teamFranchiseId=5 and gameTypeId=2'}


def test_versus_franchise_rejects_bad_franchise() -> None:
    with pytest.raises(InvalidIdentifierError):
        records_versus_franchise(RecordsEndpoint.ALL_TIME_RECORD, 0, None)


def test_attendance_url() -> None:
    assert records_attendance().url == f'{BASE}/attendance'


def test_draft_empty_when_none() -> None:
    request = records_draft(None, None)
    assert request.url == f'{BASE}/draft'
    assert request.params == {}


def test_draft_builds_cayenne() -> None:
    request = records_draft(1, 2020)
    assert request.params == {'cayenneExp': 'draftedByTeamId=1 and draftYear=2020'}


def test_draft_rejects_bad_team() -> None:
    with pytest.raises(InvalidIdentifierError):
        records_draft(0, None)


def test_milestone_url() -> None:
    assert records_milestone(Milestone.GOAL_SEASON_50).url == f'{BASE}/milestone-50-goal-season'


def test_officials_empty_when_none() -> None:
    assert records_officials(None).params == {}


def test_officials_true() -> None:
    assert records_officials(active=True).params == {'cayenneExp': 'active=true'}


def test_officials_false_is_kept() -> None:
    assert records_officials(active=False).params == {'cayenneExp': 'active=false'}


def test_players_all_when_team_none() -> None:
    request = records_players(None)
    assert request.url == f'{BASE}/player'
    assert request.params == {}


def test_players_by_team() -> None:
    assert records_players(1).url == f'{BASE}/player/byTeam/1'


def test_players_rejects_bad_team() -> None:
    with pytest.raises(InvalidIdentifierError):
        records_players(0)


def test_playoff_series_quotes_string_value() -> None:
    request = records_playoff_series('F', 20242025)
    assert request.params == {'cayenneExp': 'seriesTitle="F" and seasonId=20242025'}


def test_playoff_series_rejects_bad_season() -> None:
    with pytest.raises(InvalidSeasonError):
        records_playoff_series(None, 20242030)


def test_trophies_url() -> None:
    assert records_trophies().url == f'{BASE}/trophy'


def test_resource_franchises_uses_model() -> None:
    fake = FakeSyncRequester()
    Records(fake).franchises()
    assert fake.method == 'get_model'
    assert fake.model is ResultSet
    assert fake.request.url == f'{BASE}/franchise'


def test_resource_milestone_uses_model() -> None:
    fake = FakeSyncRequester()
    Records(fake).milestone(Milestone.POINT_CAREER_1000)
    assert fake.model is ResultSet
    assert fake.request.url == f'{BASE}/milestone-1000-point-career'
