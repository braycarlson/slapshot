from __future__ import annotations

from enum import StrEnum


BASE_RECORDS = 'https://records.nhl.com/site/api'
BASE_SEARCH = 'https://search.d3.nhle.com/api/v1'
BASE_STATS = 'https://api.nhle.com/stats/rest'
BASE_WEB = 'https://api-web.nhle.com/v1'


class WebEndpoint(StrEnum):
    """The URL templates for the web API (api-web.nhle.com)."""

    CLUB_STATS = BASE_WEB + '/club-stats/{team}/{season}/{game_type}'
    CLUB_STATS_NOW = BASE_WEB + '/club-stats/{team}/now'
    CLUB_STATS_SEASONS = BASE_WEB + '/club-stats-season/{team}'
    DRAFT_PICKS = BASE_WEB + '/draft/picks/{year}/{round}'
    DRAFT_PICKS_NOW = BASE_WEB + '/draft/picks/now'
    DRAFT_RANKINGS = BASE_WEB + '/draft/rankings/{year}/{category}'
    DRAFT_RANKINGS_NOW = BASE_WEB + '/draft/rankings/now'
    GAME_BOXSCORE = BASE_WEB + '/gamecenter/{game}/boxscore'
    GAME_LANDING = BASE_WEB + '/gamecenter/{game}/landing'
    GAME_PLAY_BY_PLAY = BASE_WEB + '/gamecenter/{game}/play-by-play'
    GAME_RIGHT_RAIL = BASE_WEB + '/gamecenter/{game}/right-rail'
    GAME_STORY = BASE_WEB + '/wsc/game-story/{game}'
    GOALIE_LEADERS = BASE_WEB + '/goalie-stats-leaders/{season}/{game_type}'
    GOALIE_LEADERS_CURRENT = BASE_WEB + '/goalie-stats-leaders/current'
    PLAYER_GAME_LOG = BASE_WEB + '/player/{player}/game-log/{season}/{game_type}'
    PLAYER_GAME_LOG_NOW = BASE_WEB + '/player/{player}/game-log/now'
    PLAYER_LANDING = BASE_WEB + '/player/{player}/landing'
    PLAYER_SPOTLIGHT = BASE_WEB + '/player-spotlight'
    PROSPECTS = BASE_WEB + '/prospects/{team}'
    ROSTER = BASE_WEB + '/roster/{team}/{season}'
    ROSTER_CURRENT = BASE_WEB + '/roster/{team}/current'
    ROSTER_SEASONS = BASE_WEB + '/roster-season/{team}'
    SCHEDULE_BY_DATE = BASE_WEB + '/schedule/{date}'
    SCHEDULE_CLUB_MONTH = BASE_WEB + '/club-schedule/{team}/month/{month}'
    SCHEDULE_CLUB_MONTH_NOW = BASE_WEB + '/club-schedule/{team}/month/now'
    SCHEDULE_CLUB_SEASON = BASE_WEB + '/club-schedule-season/{team}/{season}'
    SCHEDULE_CLUB_WEEK = BASE_WEB + '/club-schedule/{team}/week/{date}'
    SCHEDULE_CLUB_WEEK_NOW = BASE_WEB + '/club-schedule/{team}/week/now'
    SCHEDULE_NOW = BASE_WEB + '/schedule/now'
    SCOREBOARD_NOW = BASE_WEB + '/scoreboard/now'
    SCORES_BY_DATE = BASE_WEB + '/score/{date}'
    SCORES_NOW = BASE_WEB + '/score/now'
    SKATER_LEADERS = BASE_WEB + '/skater-stats-leaders/{season}/{game_type}'
    SKATER_LEADERS_CURRENT = BASE_WEB + '/skater-stats-leaders/current'
    STANDINGS_BY_DATE = BASE_WEB + '/standings/{date}'
    STANDINGS_NOW = BASE_WEB + '/standings/now'
    STANDINGS_SEASONS = BASE_WEB + '/standings-season'


class StatsEndpoint(StrEnum):
    """The URL templates for the stats API (api.nhle.com/stats/rest)."""

    CONFIG = BASE_STATS + '/{language}/config'
    FRANCHISES = BASE_STATS + '/{language}/franchise'
    GLOSSARY = BASE_STATS + '/{language}/glossary'
    REPORT = BASE_STATS + '/{language}/{subject}/{report}'
    SEASONS = BASE_STATS + '/{language}/season'


class RecordsEndpoint(StrEnum):
    """The URL templates for the records API (records.nhl.com)."""

    ALL_TIME_RECORD = BASE_RECORDS + '/all-time-record-vs-franchise'
    ATTENDANCE = BASE_RECORDS + '/attendance'
    DRAFT = BASE_RECORDS + '/draft'
    FRANCHISE_DETAILS = BASE_RECORDS + '/franchise-detail'
    FRANCHISE_GOALIE_RECORDS = BASE_RECORDS + '/franchise-goalie-records'
    FRANCHISE_SEASON_RECORDS = BASE_RECORDS + '/franchise-season-records'
    FRANCHISE_SEASON_RESULTS = BASE_RECORDS + '/franchise-season-results'
    FRANCHISE_SKATER_RECORDS = BASE_RECORDS + '/franchise-skater-records'
    FRANCHISE_TEAM_TOTALS = BASE_RECORDS + '/franchise-team-totals'
    FRANCHISES = BASE_RECORDS + '/franchise'
    MILESTONE = BASE_RECORDS + '/milestone-{name}'
    OFFICIALS = BASE_RECORDS + '/officials'
    PLAYERS = BASE_RECORDS + '/player'
    PLAYERS_BY_TEAM = BASE_RECORDS + '/player/byTeam/{team}'
    PLAYOFF_SERIES = BASE_RECORDS + '/playoff-series'
    TROPHIES = BASE_RECORDS + '/trophy'


class SearchEndpoint(StrEnum):
    """The URL templates for the search API (search.d3.nhle.com)."""

    PLAYER = BASE_SEARCH + '/search/player'
