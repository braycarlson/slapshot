# Quickstart

## Overview

This guide makes a first request with both the synchronous and asynchronous clients, then explains what each call returns. It assumes slapshot is already [installed](installation.md).

The `NHL` and `AsyncNHL` clients expose the same resources and method names. Use the synchronous client for scripts and notebooks, and the asynchronous client for concurrent or event-loop code.

## Synchronous

Use `NHL` as a context manager so its underlying `httpx` client is closed when the block exits:

```python
from slapshot import NHL, Milestone, Team

with NHL() as client:
    standings = client.standings.now()
    print(standings.standings[0].team_name.default)

    player = client.players.landing(8478402)
    print(player.first_name.default, player.last_name.default)

    skaters = client.stats.skaters(season=20252026, limit=5)
    milestone = client.records.milestone(Milestone.GOAL_CAREER_500)
    roster = client.teams.roster(Team.EDMONTON)
```

## Asynchronous

`AsyncNHL` mirrors `NHL`. Enter it with `async with` and `await` each call:

```python
import asyncio

from slapshot import AsyncNHL, GameType, Team


async def main() -> None:
    async with AsyncNHL() as client:
        schedule = await client.schedule.club_week(Team.EDMONTON)
        log = await client.players.game_log(8478402, season=20252026, game_type=GameType.REGULAR)
        results = await client.players.search('mcdavid', limit=3)


asyncio.run(main())
```

## What a Call Returns

Every resource method returns one of two things:

- A **typed model** when the payload is stable. For example, `client.standings.now()` returns a `StandingsResponse` and `client.teams.roster(...)` returns a `Roster`. Attributes are `snake_case`.
- **Decoded JSON** (`dict` or `list`) when the payload is volatile: gamecenter, play-by-play, schedules, draft, leaders, and config. For example, `client.players.game_log(...)` returns a `dict`.

See [Models](../reference/models.md) for the full list of typed endpoints, and [Resources](../reference/resources.md) for the return type of every method.

Localized text is wrapped in a `LocalizedName`, whose `default` attribute holds the English value:

```python
from slapshot import NHL, Team

with NHL() as client:
    roster = client.teams.roster(Team.EDMONTON)
    forward = roster.forwards[0]
    print(forward.first_name.default, forward.last_name.default)
```

## A Complete Example

The following script draws from five resources in a single session:

```python
from slapshot import NHL, GameType, Milestone, Team


def main() -> None:
    with NHL() as client:
        standings = client.standings.now()
        leader = standings.standings[0]
        print('Top team:', leader.team_name.default, leader.points)

        player = client.players.landing(8478402)
        print('Player:', player.first_name.default, player.last_name.default, player.position)

        skaters = client.stats.skaters(season=20252026, limit=5)
        print('Top scorers:', [row['skaterFullName'] for row in skaters.data])

        roster = client.teams.roster(Team.EDMONTON)
        print('Roster:', len(roster.forwards), len(roster.defensemen), len(roster.goalies))

        milestone = client.records.milestone(Milestone.GOAL_CAREER_500)
        print('500-goal scorers:', milestone.total)

        log = client.players.game_log(8478402, season=20252026, game_type=GameType.REGULAR)
        print('Games logged:', len(log['gameLog']))


if __name__ == '__main__':
    main()
```

Runnable scripts for every resource live in the [`examples/`](https://github.com/braycarlson/slapshot/tree/main/examples) directory. Run one with:

```
uv run python examples/quickstart.py
```

## Next Steps

- [Client](../reference/client.md): timeouts, custom transports, and lifecycle
- [Resources](../reference/resources.md): every method and its parameters
- [Errors](../reference/errors.md): handling transport, HTTP, and validation failures
