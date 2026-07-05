from __future__ import annotations

import inspect

import pytest

from slapshot.client import NHL, AsyncNHL
from slapshot.resources.draft import AsyncDraft, Draft
from slapshot.resources.games import AsyncGames, Games
from slapshot.resources.players import AsyncPlayers, Players
from slapshot.resources.records import AsyncRecords, Records
from slapshot.resources.schedule import AsyncSchedule, Schedule
from slapshot.resources.standings import AsyncStandings, Standings
from slapshot.resources.stats import AsyncStats, Stats
from slapshot.resources.teams import AsyncTeams, Teams


PAIRS = [
    (Draft, AsyncDraft),
    (Games, AsyncGames),
    (NHL, AsyncNHL),
    (Players, AsyncPlayers),
    (Records, AsyncRecords),
    (Schedule, AsyncSchedule),
    (Standings, AsyncStandings),
    (Stats, AsyncStats),
    (Teams, AsyncTeams),
]


def public_methods(cls: type) -> set[str]:
    return {name for name in dir(cls) if not name.startswith('_')}


@pytest.mark.parametrize(('synchronous', 'asynchronous'), PAIRS)
def test_method_names_match(synchronous: type, asynchronous: type) -> None:
    assert public_methods(synchronous) == public_methods(asynchronous)


@pytest.mark.parametrize(('synchronous', 'asynchronous'), PAIRS)
def test_signatures_match(synchronous: type, asynchronous: type) -> None:
    for name in public_methods(synchronous):
        assert inspect.signature(getattr(synchronous, name)) == inspect.signature(
            getattr(asynchronous, name)
        )
