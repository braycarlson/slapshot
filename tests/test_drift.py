from __future__ import annotations

import pytest

from typing_extensions import Any, TYPE_CHECKING

from slapshot.client import NHL
from slapshot.enums import Team
from slapshot.introspect import unknown_fields
from slapshot.models import PlayerLanding, PlayerSearchResult, Roster, StandingsResponse
from slapshot.resources.players import player_landing, player_search
from slapshot.resources.standings import standings_now
from slapshot.resources.teams import roster

if TYPE_CHECKING:
    from slapshot.request import Request


pytestmark = pytest.mark.network


CASES: list[tuple[str, Request, Any]] = [
    ('standings.now', standings_now(), StandingsResponse),
    ('teams.roster', roster(Team.TORONTO, None), Roster),
    ('players.landing', player_landing(8478402), PlayerLanding),
    ('players.search', player_search('mcdavid', 20, None, 'en-us'), list[PlayerSearchResult]),
]


@pytest.mark.parametrize(('label', 'built', 'model'), CASES, ids=[case[0] for case in CASES])
def test_no_unknown_fields(label: str, built: Request, model: Any) -> None:
    with NHL() as nhl:
        raw = nhl.get(built)

    missing = unknown_fields(raw, model)

    assert not missing, f'{label}: {len(missing)} undefined field(s): {missing}'
