# Enums

## Overview

slapshot ships five enums for the values the API uses most often. `Team`, `Language`, `Milestone`, and `SortDirection` are `StrEnum` members, and `GameType` is an `IntEnum`. Because they subclass `str` and `int`, each member is accepted anywhere the corresponding raw value is; you can pass `Team.EDMONTON` or `'EDM'` interchangeably.

```python
from slapshot import GameType, Language, Milestone, SortDirection, Team
```

---

## Team

A `StrEnum` of the 32 team abbreviations. Pass a member or its three-letter string.

| Member | Value | Member | Value |
|--------|-------|--------|-------|
| `ANAHEIM` | `ANA` | `NASHVILLE` | `NSH` |
| `BOSTON` | `BOS` | `NEW_JERSEY` | `NJD` |
| `BUFFALO` | `BUF` | `NY_ISLANDERS` | `NYI` |
| `CALGARY` | `CGY` | `NY_RANGERS` | `NYR` |
| `CAROLINA` | `CAR` | `OTTAWA` | `OTT` |
| `CHICAGO` | `CHI` | `PHILADELPHIA` | `PHI` |
| `COLORADO` | `COL` | `PITTSBURGH` | `PIT` |
| `COLUMBUS` | `CBJ` | `SAN_JOSE` | `SJS` |
| `DALLAS` | `DAL` | `SEATTLE` | `SEA` |
| `DETROIT` | `DET` | `ST_LOUIS` | `STL` |
| `EDMONTON` | `EDM` | `TAMPA_BAY` | `TBL` |
| `FLORIDA` | `FLA` | `TORONTO` | `TOR` |
| `LOS_ANGELES` | `LAK` | `UTAH` | `UTA` |
| `MINNESOTA` | `MIN` | `VANCOUVER` | `VAN` |
| `MONTREAL` | `MTL` | `VEGAS` | `VGK` |
| `WASHINGTON` | `WSH` | `WINNIPEG` | `WPG` |

```python
from slapshot import Team

client.teams.roster(Team.EDMONTON)
client.teams.roster('EDM')
```

---

## GameType

An `IntEnum` of the game types. Pass a member or its integer value.

| Member | Value | Description |
|--------|-------|-------------|
| `PRESEASON` | `1` | Preseason. |
| `REGULAR` | `2` | Regular season. |
| `PLAYOFF` | `3` | Playoffs. |

Methods that accept `game_type` default to `GameType.REGULAR`.

---

## Language

A `StrEnum` of the languages served by the Stats API.

| Member | Value |
|--------|-------|
| `ENGLISH` | `en` |
| `FRENCH` | `fr` |

Stats methods that accept `language` default to `Language.ENGLISH`.

---

## Milestone

A `StrEnum` of the milestone lists on the Records API. Pass a member to `records.milestone`.

| Member | Value |
|--------|-------|
| `GOAL_CAREER_500` | `500-goal-career` |
| `GOAL_GAME_5` | `5-goal-game` |
| `GOAL_SEASON_50` | `50-goal-season` |
| `POINT_CAREER_1000` | `1000-point-career` |
| `POINT_SEASON_100` | `100-point-season` |

```python
from slapshot import Milestone

client.records.milestone(Milestone.GOAL_CAREER_500)
```

---

## SortDirection

A `StrEnum` of sort directions, used in `stats` sort specifications and the `order` argument of `records` franchise reports.

| Member | Value |
|--------|-------|
| `ASCENDING` | `ASC` |
| `DESCENDING` | `DESC` |

```python
from slapshot import SortDirection

client.stats.skaters(
    season=20252026,
    sort=({'property': 'goals', 'direction': SortDirection.DESCENDING},)
)
```
