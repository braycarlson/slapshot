from __future__ import annotations

from enum import IntEnum, StrEnum


class GameType(IntEnum):
    """The type of game: preseason, regular season, or playoff."""

    PRESEASON = 1
    REGULAR = 2
    PLAYOFF = 3


class Language(StrEnum):
    """A language served by the stats API."""

    ENGLISH = 'en'
    FRENCH = 'fr'


class Milestone(StrEnum):
    """A milestone list on the records API."""

    GOAL_CAREER_500 = '500-goal-career'
    GOAL_GAME_5 = '5-goal-game'
    GOAL_SEASON_50 = '50-goal-season'
    POINT_CAREER_1000 = '1000-point-career'
    POINT_SEASON_100 = '100-point-season'


class SortDirection(StrEnum):
    """A sort direction, ascending or descending."""

    ASCENDING = 'ASC'
    DESCENDING = 'DESC'


class Team(StrEnum):
    """A team abbreviation."""

    ANAHEIM = 'ANA'
    BOSTON = 'BOS'
    BUFFALO = 'BUF'
    CALGARY = 'CGY'
    CAROLINA = 'CAR'
    CHICAGO = 'CHI'
    COLORADO = 'COL'
    COLUMBUS = 'CBJ'
    DALLAS = 'DAL'
    DETROIT = 'DET'
    EDMONTON = 'EDM'
    FLORIDA = 'FLA'
    LOS_ANGELES = 'LAK'
    MINNESOTA = 'MIN'
    MONTREAL = 'MTL'
    NASHVILLE = 'NSH'
    NEW_JERSEY = 'NJD'
    NY_ISLANDERS = 'NYI'
    NY_RANGERS = 'NYR'
    OTTAWA = 'OTT'
    PHILADELPHIA = 'PHI'
    PITTSBURGH = 'PIT'
    SAN_JOSE = 'SJS'
    SEATTLE = 'SEA'
    ST_LOUIS = 'STL'
    TAMPA_BAY = 'TBL'
    TORONTO = 'TOR'
    UTAH = 'UTA'
    VANCOUVER = 'VAN'
    VEGAS = 'VGK'
    WASHINGTON = 'WSH'
    WINNIPEG = 'WPG'
