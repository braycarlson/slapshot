from __future__ import annotations

import pytest

from tests.support import FakeSyncRequester

from slapshot.exceptions import InvalidDraftRoundError, InvalidIdentifierError
from slapshot.resources.draft import Draft, draft_picks, draft_rankings


BASE = 'https://api-web.nhle.com/v1'


def test_picks_now_when_year_none() -> None:
    assert draft_picks(None, 1).url == BASE + '/draft/picks/now'


def test_picks_now_ignores_round_when_year_none() -> None:
    assert draft_picks(None, 0).url == BASE + '/draft/picks/now'


def test_picks_with_year_and_round() -> None:
    assert draft_picks(2023, 1).url == BASE + '/draft/picks/2023/1'


def test_picks_allows_string_round() -> None:
    assert draft_picks(2023, 'all').url == BASE + '/draft/picks/2023/all'


def test_picks_rejects_zero_round() -> None:
    with pytest.raises(InvalidDraftRoundError):
        draft_picks(2023, 0)


def test_picks_rejects_nonpositive_year() -> None:
    with pytest.raises(InvalidIdentifierError):
        draft_picks(0, 1)


def test_rankings_now_when_year_none() -> None:
    assert draft_rankings(None, 1).url == BASE + '/draft/rankings/now'


def test_rankings_with_year_and_category() -> None:
    assert draft_rankings(2023, 2).url == BASE + '/draft/rankings/2023/2'


def test_rankings_rejects_nonpositive_year() -> None:
    with pytest.raises(InvalidIdentifierError):
        draft_rankings(0, 1)


def test_resource_picks_delegates_to_get() -> None:
    fake = FakeSyncRequester()
    Draft(fake).picks(2023, draft_round=2)
    assert fake.method == 'get'
    assert fake.request.url == BASE + '/draft/picks/2023/2'


def test_resource_picks_defaults_to_now() -> None:
    fake = FakeSyncRequester()
    Draft(fake).picks()
    assert fake.request.url == BASE + '/draft/picks/now'


def test_resource_rankings_defaults_to_now() -> None:
    fake = FakeSyncRequester()
    Draft(fake).rankings()
    assert fake.request.url == BASE + '/draft/rankings/now'
