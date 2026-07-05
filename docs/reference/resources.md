# Resources

## Overview

A resource groups related endpoints into methods on the client. Every resource is available in both synchronous and asynchronous form under the same attribute name and with the same method signatures; the asynchronous methods are awaitable. The examples below use the synchronous client.

```python
from slapshot import NHL

with NHL() as client:
    client.standings.now()
    client.players.landing(8478402)
```

### Argument Conventions

Several argument shapes recur across resources and are validated before a request is sent. An invalid value raises a subclass of `InvalidParameterError`; see [Errors](errors.md).

| Argument | Format | Example |
|----------|--------|---------|
| `season` | An eight-digit integer of two consecutive years, `YYYYYYYY`, starting at 1917. | `20252026` |
| `date` | An ISO date string, `YYYY-MM-DD`. | `'2025-01-15'` |
| `month` | A year and month string, `YYYY-MM`. | `'2025-01'` |
| `team` | A [`Team`](enums.md#team) enum or a three-letter abbreviation string. | `Team.EDMONTON`, `'EDM'` |
| `game_type` | A [`GameType`](enums.md#gametype) enum or its integer value. | `GameType.REGULAR`, `2` |
| Identifiers | A positive integer (`player`, `game`, `franchise`, `team` id, `year`). | `8478402` |

Many methods accept a "current" form: when `season`, `date`, or `month` is omitted, the request targets the current day or season.

### Return Types

A method returns a **typed model** when the payload is stable and **decoded JSON** (`dict` or `list`) when it is volatile. The return type of each method is listed in the tables below. See [Models](models.md) for the structs.

---

## standings

Backed by the Web API. Standings decode into a [`StandingsResponse`](models.md#standingsresponse).

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `now()` | none | `StandingsResponse` | Current standings. |
| `by_date(date)` | `date: str` | `StandingsResponse` | Standings as of a date. |
| `seasons()` | none | `dict` / `list` | Season identifiers and standings metadata. |

```python
standings = client.standings.now()

for team in standings.standings:
    print(team.team_name.default, team.points)
```

---

## schedule

Backed by the Web API. Every method returns decoded JSON.

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `now()` | none | `dict` | League schedule for the current day. |
| `by_date(date)` | `date: str` | `dict` | League schedule for a date. |
| `club_week(team, *, date=None)` | `team`, `date: str \| None` | `dict` | A team's week; the current week when `date` is omitted. |
| `club_month(team, *, month=None)` | `team`, `month: str \| None` | `dict` | A team's month; the current month when `month` is omitted. |
| `club_season(team, season)` | `team`, `season: int` | `dict` | A team's full season. |

```python
from slapshot import Team

week = client.schedule.club_week(Team.EDMONTON)
print(week['clubTimezone'])
```

---

## games

Backed by the Web API. Every method returns decoded JSON. The `game` argument is a positive game identifier.

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `landing(game)` | `game: int` | `dict` | Game landing summary. |
| `boxscore(game)` | `game: int` | `dict` | Boxscore. |
| `play_by_play(game)` | `game: int` | `dict` | Play-by-play events. |
| `right_rail(game)` | `game: int` | `dict` | Right-rail content (scoring, team stats). |
| `story(game)` | `game: int` | `dict` | Editorial game story. |
| `scores(date=None)` | `date: str \| None` | `dict` | Scores for a date; the current day when `date` is omitted. |
| `scoreboard()` | none | `dict` | Current scoreboard. |

```python
boxscore = client.games.boxscore(2024020500)
```

---

## players

Backed by the Web API and the Search API. `landing` and `search` decode into models; the remaining methods return decoded JSON.

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `landing(player)` | `player: int` | `PlayerLanding` | Player profile. |
| `game_log(player, *, season=None, game_type=GameType.REGULAR)` | `player: int`, `season: int \| None`, `game_type` | `dict` | Game log; the current log when `season` is omitted. |
| `spotlight()` | none | `list` | Spotlighted players. |
| `search(query, *, limit=20, active=None, culture='en-us')` | `query: str`, `limit: int`, `active: bool \| None`, `culture: str` | `list[PlayerSearchResult]` | Player search. `query` must not be empty. |
| `skater_leaders(*, season=None, game_type=GameType.REGULAR, categories=None, limit=5)` | `season`, `game_type`, `categories: str \| None`, `limit: int` | `dict` | Skater statistical leaders. |
| `goalie_leaders(*, season=None, game_type=GameType.REGULAR, categories=None, limit=5)` | `season`, `game_type`, `categories: str \| None`, `limit: int` | `dict` | Goalie statistical leaders. |

```python
player = client.players.landing(8478402)
print(player.first_name.default, player.last_name.default)

results = client.players.search('mcdavid', limit=3)
print([row.name for row in results])
```

---

## teams

Backed by the Web API. `roster` decodes into a [`Roster`](models.md#roster); the remaining methods return decoded JSON.

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `roster(team, *, season=None)` | `team`, `season: int \| None` | `Roster` | Team roster; the current roster when `season` is omitted. |
| `roster_seasons(team)` | `team` | `list` | Seasons for which a roster exists. |
| `prospects(team)` | `team` | `dict` | Team prospects. |
| `club_stats(team, *, season=None, game_type=GameType.REGULAR)` | `team`, `season: int \| None`, `game_type` | `dict` | Club statistics; the current stats when `season` is omitted. |
| `club_stats_seasons(team)` | `team` | `list` | Seasons with club statistics. |

```python
from slapshot import Team

roster = client.teams.roster(Team.EDMONTON)
print(len(roster.forwards), len(roster.defensemen), len(roster.goalies))
```

---

## draft

Backed by the Web API. Every method returns decoded JSON.

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `rankings(year=None, *, category=1)` | `year: int \| None`, `category: int` | `dict` | Draft prospect rankings; the current rankings when `year` is omitted. |
| `picks(year=None, *, draft_round=1)` | `year: int \| None`, `draft_round: int \| str` | `dict` | Draft picks; the current picks when `year` is omitted. |

`draft_round` accepts a round number of at least 1, or a string such as `'all'`.

```python
picks = client.draft.picks(2015, draft_round=1)
rankings = client.draft.rankings(2015, category=1)
```

---

## stats

Backed by the Stats API. `config` returns decoded JSON; every other method decodes into a [`ResultSet`](models.md#resultset).

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `skaters(report='summary', *, ...)` | See report parameters below | `ResultSet` | Skater report. Defaults to sorting by points, descending. |
| `goalies(report='summary', *, ...)` | See report parameters below | `ResultSet` | Goalie report. Defaults to sorting by wins, descending. |
| `teams(report='summary', *, ...)` | See report parameters below | `ResultSet` | Team report. Defaults to sorting by points, descending. |
| `report(subject, report, *, ...)` | `subject: str`, `report: str`, then report parameters | `ResultSet` | An arbitrary report for any subject. No default sort. |
| `config(language=Language.ENGLISH)` | `language` | `dict` | Configuration metadata. |
| `franchises(language=Language.ENGLISH)` | `language` | `ResultSet` | Franchises. |
| `seasons(language=Language.ENGLISH)` | `language` | `ResultSet` | Seasons. |
| `glossary(language=Language.ENGLISH)` | `language` | `ResultSet` | Statistic glossary. |

The report methods (`skaters`, `goalies`, `teams`, `report`) share these keyword-only parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `report` | `str` | `'summary'` | The report name, such as `summary` or `bios`. A positional argument on `skaters`, `goalies`, and `teams`. |
| `season` | `int \| None` | `None` | Season filter, added to the query expression as `seasonId`. |
| `game_type` | `GameType \| int \| None` | `None` | Game-type filter, added as `gameTypeId`. |
| `sort` | `str` / `Sequence[dict]` / `None` | `None` | Sort specification; a property name or a sequence of `{'property', 'direction'}` mappings. |
| `limit` | `int` | `50` | Page size. Must be greater than zero. |
| `start` | `int` | `0` | Page offset. Must be zero or greater. |
| `aggregate` | `bool` | `False` | Aggregate rows across seasons. |
| `game` | `bool` | `False` | Return per-game rows. |
| `cayenne` | `str` / `dict` / `None` | `None` | A raw cayenne expression, or a mapping merged into the built expression. |
| `language` | `Language \| str` | `Language.ENGLISH` | Response language. |

```python
from slapshot import SortDirection

skaters = client.stats.skaters(season=20252026, limit=5)
print([row['skaterFullName'] for row in skaters.data])

custom = client.stats.report(
    'skater',
    'summary',
    season=20252026,
    sort=({'property': 'goals', 'direction': SortDirection.DESCENDING},),
    limit=3
)
```

---

## records

Backed by the Records API. Every method decodes into a [`ResultSet`](models.md#resultset).

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `attendance()` | none | `ResultSet` | Attendance records. |
| `draft(*, team=None, year=None)` | `team: int \| None`, `year: int \| None` | `ResultSet` | Draft records. |
| `franchises(*, ...)` | See franchise filters below | `ResultSet` | Franchise index. |
| `franchise_details(*, ...)` | See franchise filters below | `ResultSet` | Franchise detail. |
| `franchise_season_records(*, ...)` | See franchise filters below | `ResultSet` | Single-season franchise records. |
| `franchise_season_results(*, ...)` | See franchise filters below | `ResultSet` | Season-by-season franchise results. |
| `franchise_team_totals(*, ...)` | See franchise filters below | `ResultSet` | All-time team totals. |
| `franchise_goalie_records(*, ...)` | See franchise filters below | `ResultSet` | Franchise goalie records. |
| `franchise_skater_records(*, ...)` | See franchise filters below | `ResultSet` | Franchise skater records. |
| `milestone(name)` | `name: Milestone` | `ResultSet` | Milestone lists, such as 500-goal careers. |
| `officials(active=None)` | `active: bool \| None` | `ResultSet` | Officials, optionally filtered by active status. |
| `players(team=None)` | `team: int \| None` | `ResultSet` | Players; filtered by team when an id is given. |
| `playoff_series(*, series=None, season=None)` | `series: str \| None`, `season: int \| None` | `ResultSet` | Playoff series. |
| `all_time_record(franchise=None, game_type=None)` | `franchise: int \| None`, `game_type` | `ResultSet` | All-time record versus a franchise. |
| `trophies()` | none | `ResultSet` | Trophies. |

The `franchises` and `franchise_*` methods share these keyword-only filters, all optional:

| Parameter | Type | Description |
|-----------|------|-------------|
| `franchise` | `int \| None` | Franchise identifier (`franchiseId`). |
| `team` | `int \| None` | Most recent team identifier (`mostRecentTeamId`). |
| `season` | `int \| None` | Season filter (`seasonId`). |
| `sort` | `str \| None` | Sort property. |
| `order` | `SortDirection \| str \| None` | Sort direction, `ASC` or `DESC`. |

```python
from slapshot import GameType, Milestone

milestone = client.records.milestone(Milestone.GOAL_CAREER_500)
print('500-goal scorers:', milestone.total)

versus = client.records.all_time_record(franchise=1, game_type=GameType.REGULAR)
print('Rows:', versus.total)
```
