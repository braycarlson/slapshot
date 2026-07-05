# slapshot

<p align="center">
    <img alt="Python Version" src="https://img.shields.io/badge/python-3.11%2B-blue">
    <img alt="License" src="https://img.shields.io/badge/license-MIT-green">
</p>

## Purpose

slapshot is a synchronous and asynchronous client for the unofficial NHL API. It covers the four public NHL services behind a single, typed interface: `api-web.nhle.com`, `api.nhle.com/stats/rest`, `records.nhl.com`, and the player search at `search.d3.nhle.com`.

## Why slapshot?

The NHL exposes a large, undocumented surface of endpoints spread across several hosts, each with its own path conventions, query parameters, and payload shapes. slapshot wraps them behind one typed interface, so the caller works with the data rather than with URL construction and response parsing.

Stable payloads decode into `msgspec` structs with `snake_case` attributes, while volatile payloads come back as decoded JSON. Decoding ignores unknown fields, so new NHL fields never break existing code. Every URL template lives in an enum, so no path is ever built from a loose string.

## How It Works

slapshot has four layers:

- **Client** (`NHL`, `AsyncNHL`): owns the `httpx` transport and exposes one attribute per resource.
- **Resources** (`client.standings`, `client.players`, ...): group related endpoints into methods.
- **Request builders** (`slapshot.resources.*`): validate arguments and produce a `Request` of URL and query parameters.
- **Endpoints** (`WebEndpoint`, `StatsEndpoint`, `RecordsEndpoint`, `SearchEndpoint`): hold every URL template as a `StrEnum`.

The synchronous `NHL` and asynchronous `AsyncNHL` clients expose the same resources and the same method names. `AsyncNHL` mirrors `NHL`; its methods are awaitable.

## Core Features

- **Synchronous and Asynchronous**: an identical API on `NHL` and `AsyncNHL`, chosen per call site.
- **Typed Models**: stable payloads decode into `msgspec` structs; volatile payloads return raw JSON.
- **Forward Compatible**: decoding ignores unknown response fields, so new NHL fields never break existing code.
- **No Loose Paths**: every endpoint is a `StrEnum` template, and slapshot validates identifiers, seasons, and dates before it sends a request.
- **Bring Your Own Transport**: inject a preconfigured `httpx` client for proxies, retries, or custom headers.
- **Typed Errors**: a single `NHLError` hierarchy covers transport, HTTP status, decode, and parameter failures.

## Backing APIs

| Service | Base URL | Resources |
|---------|----------|-----------|
| Web | `https://api-web.nhle.com/v1` | `standings`, `schedule`, `games`, `players`, `teams`, `draft` |
| Stats | `https://api.nhle.com/stats/rest` | `stats` |
| Records | `https://records.nhl.com/site/api` | `records` |
| Search | `https://search.d3.nhle.com/api/v1` | `players.search` |

---

## Installation

### Prerequisites

- Python 3.11 or newer
- [uv](https://github.com/astral-sh/uv) (recommended) or `pip`

### From PyPI

```
uv add slapshot
```

Or with `pip`:

```
pip install slapshot
```

### From Source

```
git clone https://github.com/braycarlson/slapshot
cd slapshot
uv sync
```

## Usage

Runnable scripts for every resource live in [`examples/`](examples/). Run one with `uv run python examples/quickstart.py`.

### Synchronous

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

### Asynchronous

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

---

## Resources

Every resource comes in both a synchronous and an asynchronous form, under the same attribute name and with the same method signatures.

| Resource | Backing API | Methods |
|---|---|---|
| `client.standings` | api-web.nhle.com | `now`, `by_date`, `seasons` |
| `client.schedule` | api-web.nhle.com | `now`, `by_date`, `club_week`, `club_month`, `club_season` |
| `client.games` | api-web.nhle.com | `landing`, `boxscore`, `play_by_play`, `right_rail`, `story`, `scores`, `scoreboard` |
| `client.players` | api-web.nhle.com, search.d3.nhle.com | `landing`, `game_log`, `spotlight`, `search`, `skater_leaders`, `goalie_leaders` |
| `client.teams` | api-web.nhle.com | `roster`, `roster_seasons`, `prospects`, `club_stats`, `club_stats_seasons` |
| `client.draft` | api-web.nhle.com | `rankings`, `picks` |
| `client.stats` | api.nhle.com/stats/rest | `skaters`, `goalies`, `teams`, `report`, `config`, `franchises`, `seasons`, `glossary` |
| `client.records` | records.nhl.com | `attendance`, `draft`, `franchises`, `franchise_details`, `franchise_season_records`, `franchise_season_results`, `franchise_team_totals`, `franchise_goalie_records`, `franchise_skater_records`, `milestone`, `officials`, `players`, `playoff_series`, `all_time_record`, `trophies` |

## Models

Stable payloads decode into `msgspec` structs with `snake_case` attributes: `StandingsResponse` / `StandingsTeam`, `Roster` / `RosterPlayer`, `PlayerLanding`, `PlayerSearchResult`, and the `ResultSet` envelope (`data`, `total`) shared by every stats and records report. Volatile payloads (gamecenter, play-by-play, schedules, draft, leaders, config) return decoded JSON as-is.

A `LocalizedName` wraps localized text; its `default` attribute holds the English value.

The raw payload for any endpoint remains available through the request builders:

```python
from slapshot.resources.standings import standings_now

request = standings_now()
raw = client.get(request)
```

Every URL template lives in `slapshot.endpoints` as a `StrEnum` (`WebEndpoint`, `StatsEndpoint`, `RecordsEndpoint`, and `SearchEndpoint`), so no path is built from a loose string:

```python
from slapshot import WebEndpoint, request_build

url = WebEndpoint.PLAYER_LANDING.format(player=8478402)
request = request_build(url)
raw = client.get(request)
```

## Enums

`Team`, `GameType`, `Language`, `Milestone`, and `SortDirection` are `StrEnum` / `IntEnum` values accepted anywhere the corresponding string or integer is.

## Errors

Every exception inherits from `slapshot.NHLError`.

- **HTTP status**: `BadRequestError`, `UnauthorizedError`, `ForbiddenError`, `NotFoundError`, `RateLimitError`, `ServerError`, or the base `APIStatusError`.
- **Transport**: `NHLTimeoutError` or `NHLConnectionError`.
- **Response**: `UnexpectedContentTypeError` for a non-JSON response, and `ResponseDecodeError` when a body cannot be decoded or does not match the expected model.
- **Parameters**: `InvalidParameterError`, which is also a `ValueError`, so existing `except ValueError` handlers keep working.

## Detecting Unknown Fields

By default, decoding ignores fields the models do not define. To surface them instead, so nothing is silently dropped, construct a client with `warn_unknown_fields=True`. Any typed response whose payload carries an undefined field emits an `UnknownFieldWarning` naming the field paths.

```python
from slapshot import NHL

with NHL(warn_unknown_fields=True) as client:
    client.standings.now()
```

The `unknown_fields` helper performs the same check directly, and `tests/test_drift.py` (marked `network`) runs it against the live API for every typed endpoint:

```python
from slapshot import unknown_fields
from slapshot.models import StandingsResponse

missing = unknown_fields(raw_payload, StandingsResponse)
```

`client.get(request)` always returns the raw payload, so no data is lost regardless of the models.

---

## Documentation

Full documentation lives in [`docs/`](docs/), built with [MkDocs](https://www.mkdocs.org/). Serve it locally:

```
uv run --with mkdocs-material mkdocs serve
```

- [Installation](docs/setup/installation.md): How to install slapshot and its dependencies
- [Quickstart](docs/setup/quickstart.md): A first synchronous and asynchronous request
- [Client](docs/reference/client.md): Constructing `NHL` and `AsyncNHL`, timeouts, and custom transports
- [Resources](docs/reference/resources.md): Every resource and method, with parameters and return types
- [Models](docs/reference/models.md): The `msgspec` structs returned by typed endpoints
- [Enums](docs/reference/enums.md): `Team`, `GameType`, `Language`, `Milestone`, and `SortDirection`
- [Errors](docs/reference/errors.md): The exception hierarchy and when each error is raised
- [Raw Requests](docs/reference/raw_requests.md): Dropping down to request builders and endpoints

## Development

`uv sync` installs the development dependencies. Three tools check the project:

| Command | Purpose |
|---------|---------|
| `uv run ruff check` | Lint |
| `uv run ty check` | Type check |
| `uv run python -m pytest` | Run the test suite |

Tests marked `network` hit the live NHL API; pytest deselects them by default. Run them with `uv run python -m pytest -m network`.
