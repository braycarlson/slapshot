# Raw Requests

## Overview

Every resource method is a thin wrapper: it calls a request builder to produce a `Request`, then hands that request to the client. When you need a payload that has no method, or want the raw response for an endpoint that normally decodes into a model, you can build the `Request` yourself and send it with `get` or `get_model`.

```python
from slapshot import NHL, WebEndpoint, request_build
```

## The Request

A `Request` is a named tuple of a URL and a mapping of query parameters. Build one with `request_build`, which drops any parameter whose value is `None`:

```python
from slapshot import request_build

request = request_build(
    'https://api-web.nhle.com/v1/standings/now',
    {'limit': 5, 'unused': None}
)

print(request.url)      # https://api-web.nhle.com/v1/standings/now
print(request.params)   # {'limit': 5}
```

When you pass no parameters, `params` is an empty mapping.

## Endpoints

Every URL template lives in an enum, so no path is built from a loose string. There are four, each a `StrEnum`:

| Enum | Backing API |
|------|-------------|
| `WebEndpoint` | Web |
| `StatsEndpoint` | Stats |
| `RecordsEndpoint` | Records |
| `SearchEndpoint` | Search |

Fill a template's placeholders with `format`, then build and send the request:

```python
from slapshot import NHL, WebEndpoint, request_build

with NHL() as client:
    url = WebEndpoint.PLAYER_LANDING.format(player=8478402)
    request = request_build(url)

    raw = client.get(request)
    print(raw['firstName']['default'])
```

## Reusing a Builder

Each resource module exposes its request builders as module-level functions. Import one to get the same validated URL a method would use, without going through the client attribute:

```python
from slapshot import NHL
from slapshot.resources.standings import standings_now

with NHL() as client:
    request = standings_now()

    raw = client.get(request)
    print('Teams:', len(raw['standings']))
```

The builders live alongside their resource:

| Module | Builders |
|--------|----------|
| `slapshot.resources.standings` | `standings_now`, `standings_by_date`, `standings_seasons` |
| `slapshot.resources.schedule` | `schedule_now`, `schedule_by_date`, `schedule_club_week`, `schedule_club_month`, `schedule_club_season` |
| `slapshot.resources.games` | `game_landing`, `game_boxscore`, `game_play_by_play`, `game_right_rail`, `game_story`, `scores_by_date`, `scoreboard_now` |
| `slapshot.resources.players` | `player_landing`, `player_game_log`, `player_spotlight`, `player_search`, `skater_leaders`, `goalie_leaders` |
| `slapshot.resources.teams` | `roster`, `roster_seasons`, `prospects`, `club_stats`, `club_stats_seasons` |
| `slapshot.resources.draft` | `draft_picks`, `draft_rankings` |
| `slapshot.resources.stats` | `stats_report`, `stats_config`, `stats_franchises`, `stats_seasons`, `stats_glossary` |
| `slapshot.resources.records` | `records_franchise_report`, `records_versus_franchise`, `records_milestone`, `records_draft`, and the remaining `records_*` functions |

## Decoding into a Model

`get` returns decoded JSON. To decode a raw request into a [model](models.md) instead, use `get_model`:

```python
from slapshot import NHL, StandingsResponse
from slapshot.resources.standings import standings_now

with NHL() as client:
    request = standings_now()

    standings = client.get_model(request, StandingsResponse)
    print(standings.standings[0].team_name.default)
```

## Query Helpers

The Stats and Records APIs filter with a cayenne expression and, for reports, a JSON sort specification. `slapshot.request` exposes the helpers the builders use:

| Function | Description |
|----------|-------------|
| `cayenne_build(conditions)` | Joins a mapping of conditions into a cayenne expression, skipping `None` values. Returns `None` when nothing remains. |
| `cayenne_build_value(value)` | Formats a single value: booleans become `true` / `false`, and strings are quoted. |
| `sort_build(sort)` | Serializes a sort specification to the JSON string the API expects. |

```python
from slapshot import NHL, StatsEndpoint, request_build
from slapshot.request import cayenne_build

with NHL() as client:
    url = StatsEndpoint.REPORT.format(language='en', subject='skater', report='summary')
    expression = cayenne_build({'seasonId': 20252026, 'gameTypeId': 2})
    request = request_build(url, {'limit': 5, 'cayenneExp': expression})

    raw = client.get(request)
```
