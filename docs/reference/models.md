# Models

## Overview

slapshot decodes stable payloads into [`msgspec`](https://jcristharif.com/msgspec/) structs and returns volatile payloads as decoded JSON. A model gives you attribute access, `snake_case` names, and type checking; raw JSON gives you the payload exactly as the API returned it.

The NHL API uses `camelCase` field names. Every model is declared with `rename='camel'`, so the API's `teamName` becomes the attribute `team_name`. Unknown fields are ignored during decoding, so a new field added by the NHL never breaks an existing model.

All models are importable from the package root:

```python
from slapshot import (
    LocalizedName,
    PlayerLanding,
    PlayerSearchResult,
    ResultSet,
    Roster,
    RosterPlayer,
    StandingsResponse,
    StandingsTeam,
)
```

## Typed Endpoints

These methods decode into a model. Every other method returns decoded JSON.

| Method | Model |
|--------|-------|
| `standings.now`, `standings.by_date` | `StandingsResponse` |
| `teams.roster` | `Roster` |
| `players.landing` | `PlayerLanding` |
| `players.search` | `list[PlayerSearchResult]` |
| `stats.skaters`, `stats.goalies`, `stats.teams`, `stats.report`, `stats.franchises`, `stats.seasons`, `stats.glossary` | `ResultSet` |
| Every `records.*` method | `ResultSet` |

---

## LocalizedName

A localized string. The `default` attribute holds the English value; the remaining attributes hold translations when the API provides them.

| Attribute | Type | Description |
|-----------|------|-------------|
| `default` | `str` | The default (English) value. |
| `cs`, `de`, `es`, `fi`, `fr`, `sk`, `sv` | `str \| None` | Translations, when present. |

```python
print(team.team_name.default)
```

---

## StandingsResponse

Returned by `standings.now` and `standings.by_date`.

| Attribute | Type | Description |
|-----------|------|-------------|
| `standings` | `list[StandingsTeam]` | One entry per team. |
| `standings_date_time_utc` | `str \| None` | Timestamp of the standings. |
| `wild_card_indicator` | `bool \| None` | Whether wild-card ordering applies. |

## StandingsTeam

One team's standings row. Two fields are always present; the rest are optional and default to `None`.

| Attribute | Type | Description |
|-----------|------|-------------|
| `team_abbrev` | `LocalizedName` | Team abbreviation. |
| `team_name` | `LocalizedName` | Team name. |
| `points` | `int \| None` | Points. |
| `wins`, `losses`, `ot_losses`, `ties` | `int \| None` | Record. |
| `games_played` | `int \| None` | Games played. |
| `goal_for`, `goal_against`, `goal_differential` | `int \| None` | Goal totals. |
| `streak_code`, `streak_count` | `str \| None`, `int \| None` | Current streak. |
| `conference_name`, `division_name` | `str \| None` | Conference and division. |
| `league_sequence`, `conference_sequence`, `division_sequence`, `wildcard_sequence` | `int \| None` | Placement within each grouping. |

The struct additionally carries the full set of home, road, and last-ten (`l10_*`) splits as optional integer and float fields, following the same naming pattern.

```python
standings = client.standings.now()

for team in standings.standings:
    print(team.team_name.default, team.points, team.streak_code)
```

---

## Roster

Returned by `teams.roster`. Each attribute is a list of [`RosterPlayer`](#rosterplayer).

| Attribute | Type | Description |
|-----------|------|-------------|
| `forwards` | `list[RosterPlayer]` | Forwards. |
| `defensemen` | `list[RosterPlayer]` | Defensemen. |
| `goalies` | `list[RosterPlayer]` | Goalies. |

## RosterPlayer

One player on a roster. `id` is always present; the rest are optional.

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | `int` | Player identifier. |
| `first_name`, `last_name` | `LocalizedName \| None` | Name. |
| `position_code` | `str \| None` | Position (`C`, `L`, `R`, `D`, `G`). |
| `sweater_number` | `int \| None` | Jersey number. |
| `shoots_catches` | `str \| None` | Handedness. |
| `birth_date`, `birth_country` | `str \| None` | Birth details. |
| `birth_city`, `birth_state_province` | `LocalizedName \| None` | Birthplace. |
| `height_in_inches`, `height_in_centimeters` | `int \| None` | Height. |
| `weight_in_pounds`, `weight_in_kilograms` | `int \| None` | Weight. |
| `headshot` | `str \| None` | Headshot URL. |

```python
roster = client.teams.roster(Team.EDMONTON)

for player in roster.forwards:
    print(player.sweater_number, player.last_name.default)
```

---

## PlayerLanding

Returned by `players.landing`. Four fields are always present; the rest are optional.

| Attribute | Type | Description |
|-----------|------|-------------|
| `player_id` | `int` | Player identifier. |
| `is_active` | `bool` | Whether the player is active. |
| `first_name`, `last_name` | `LocalizedName` | Name. |
| `position` | `str \| None` | Position. |
| `sweater_number` | `int \| None` | Jersey number. |
| `current_team_abbrev`, `current_team_id` | `str \| None`, `int \| None` | Current team. |
| `birth_date`, `birth_country` | `str \| None` | Birth details. |
| `headshot`, `hero_image` | `str \| None` | Image URLs. |

Richer nested blocks (`career_totals`, `season_totals`, `featured_stats`, `draft_details`, `awards`, and `last_5_games`) are returned as raw `dict` or `list` values so the full detail is preserved.

```python
player = client.players.landing(8478402)
print(player.first_name.default, player.position, player.sweater_number)
```

---

## PlayerSearchResult

Returned as a `list[PlayerSearchResult]` by `players.search`. This endpoint is served by the Search API, whose identifiers arrive as strings.

| Attribute | Type | Description |
|-----------|------|-------------|
| `player_id` | `str` | Player identifier. |
| `name` | `str` | Full name. |
| `active` | `bool \| None` | Whether the player is active. |
| `position_code` | `str \| None` | Position. |
| `sweater_number` | `int \| None` | Jersey number. |
| `team_abbrev`, `team_id` | `str \| None`, `str \| int \| None` | Current team. |
| `last_team_abbrev`, `last_team_id`, `last_season_id` | `str \| None`, `str \| int \| None` | Most recent team and season. |
| `height`, `height_in_inches`, `height_in_centimeters` | `str \| None`, `int \| None` | Height. |
| `weight_in_pounds`, `weight_in_kilograms` | `int \| None` | Weight. |
| `birth_city`, `birth_state_province`, `birth_country` | `str \| None` | Birthplace. |

```python
results = client.players.search('mcdavid', limit=3)

for result in results:
    print(result.name, result.team_abbrev)
```

---

## ResultSet

The envelope shared by every Stats and Records report. `data` holds the rows exactly as the API returned them, so you index each row by its `camelCase` key.

| Attribute | Type | Description |
|-----------|------|-------------|
| `data` | `list[dict]` | The report rows. |
| `total` | `int` | The total number of rows available. |

```python
skaters = client.stats.skaters(season=20252026, limit=5)
print('Total rows:', skaters.total)

for row in skaters.data:
    print(row['skaterFullName'], row.get('points'))
```
