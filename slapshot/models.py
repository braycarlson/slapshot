from __future__ import annotations

import msgspec

from typing_extensions import Any


class LocalizedName(msgspec.Struct, rename='camel'):
    """A localized string whose default attribute holds the English value."""

    default: str
    cs: str | None = None
    de: str | None = None
    es: str | None = None
    fi: str | None = None
    fr: str | None = None
    sk: str | None = None
    sv: str | None = None


class ResultSet(msgspec.Struct, rename='camel'):
    """The envelope shared by every stats and records report."""

    data: list[dict[str, Any]]
    total: int


class StandingsTeam(msgspec.Struct, rename='camel'):
    """A single team's standings row."""

    team_abbrev: LocalizedName
    team_name: LocalizedName
    clinch_indicator: str | None = None
    conference_abbrev: str | None = None
    conference_home_sequence: int | None = None
    conference_l10_sequence: int | None = None
    conference_name: str | None = None
    conference_road_sequence: int | None = None
    conference_sequence: int | None = None
    date: str | None = None
    division_abbrev: str | None = None
    division_home_sequence: int | None = None
    division_l10_sequence: int | None = None
    division_name: str | None = None
    division_road_sequence: int | None = None
    division_sequence: int | None = None
    game_type_id: int | None = None
    games_played: int | None = None
    goal_against: int | None = None
    goal_differential: int | None = None
    goal_differential_pctg: float | None = None
    goal_for: int | None = None
    goals_for_pctg: float | None = None
    home_games_played: int | None = None
    home_goal_differential: int | None = None
    home_goals_against: int | None = None
    home_goals_for: int | None = None
    home_losses: int | None = None
    home_ot_losses: int | None = None
    home_points: int | None = None
    home_regulation_plus_ot_wins: int | None = None
    home_regulation_wins: int | None = None
    home_ties: int | None = None
    home_wins: int | None = None
    l10_games_played: int | None = None
    l10_goal_differential: int | None = None
    l10_goals_against: int | None = None
    l10_goals_for: int | None = None
    l10_losses: int | None = None
    l10_ot_losses: int | None = None
    l10_points: int | None = None
    l10_regulation_plus_ot_wins: int | None = None
    l10_regulation_wins: int | None = None
    l10_ties: int | None = None
    l10_wins: int | None = None
    league_home_sequence: int | None = None
    league_l10_sequence: int | None = None
    league_road_sequence: int | None = None
    league_sequence: int | None = None
    losses: int | None = None
    ot_losses: int | None = None
    place_name: LocalizedName | None = None
    point_pctg: float | None = None
    points: int | None = None
    regulation_plus_ot_win_pctg: float | None = None
    regulation_plus_ot_wins: int | None = None
    regulation_win_pctg: float | None = None
    regulation_wins: int | None = None
    road_games_played: int | None = None
    road_goal_differential: int | None = None
    road_goals_against: int | None = None
    road_goals_for: int | None = None
    road_losses: int | None = None
    road_ot_losses: int | None = None
    road_points: int | None = None
    road_regulation_plus_ot_wins: int | None = None
    road_regulation_wins: int | None = None
    road_ties: int | None = None
    road_wins: int | None = None
    season_id: int | None = None
    shootout_losses: int | None = None
    shootout_wins: int | None = None
    streak_code: str | None = None
    streak_count: int | None = None
    team_common_name: LocalizedName | None = None
    team_logo: str | None = None
    ties: int | None = None
    waivers_sequence: int | None = None
    wildcard_sequence: int | None = None
    win_pctg: float | None = None
    wins: int | None = None


class StandingsResponse(msgspec.Struct, rename='camel'):
    """The league standings for a day, one entry per team."""

    standings: list[StandingsTeam]
    standings_date_time_utc: str | None = None
    wild_card_indicator: bool | None = None


class RosterPlayer(msgspec.Struct, rename='camel'):
    """A player on a team roster."""

    id: int
    birth_city: LocalizedName | None = None
    birth_country: str | None = None
    birth_date: str | None = None
    birth_state_province: LocalizedName | None = None
    first_name: LocalizedName | None = None
    headshot: str | None = None
    height_in_centimeters: int | None = None
    height_in_inches: int | None = None
    last_name: LocalizedName | None = None
    position_code: str | None = None
    shoots_catches: str | None = None
    sweater_number: int | None = None
    weight_in_kilograms: int | None = None
    weight_in_pounds: int | None = None


class Roster(msgspec.Struct, rename='camel'):
    """A team roster grouped by position."""

    defensemen: list[RosterPlayer]
    forwards: list[RosterPlayer]
    goalies: list[RosterPlayer]


class PlayerLanding(msgspec.Struct, rename='camel'):
    """A player's landing profile."""

    player_id: int
    is_active: bool
    first_name: LocalizedName
    last_name: LocalizedName
    awards: list[dict[str, Any]] | None = None
    badges: list[dict[str, Any]] | None = None
    birth_city: LocalizedName | None = None
    birth_country: str | None = None
    birth_date: str | None = None
    birth_state_province: LocalizedName | None = None
    career_totals: dict[str, Any] | None = None
    current_team_abbrev: str | None = None
    current_team_id: int | None = None
    current_team_roster: list[dict[str, Any]] | None = None
    draft_details: dict[str, Any] | None = None
    featured_stats: dict[str, Any] | None = None
    full_team_name: LocalizedName | None = None
    headshot: str | None = None
    height_in_centimeters: int | None = None
    height_in_inches: int | None = None
    hero_image: str | None = None
    in_hhof: int | None = msgspec.field(default=None, name='inHHOF')
    in_top_100_all_time: int | None = None
    last_5_games: list[dict[str, Any]] | None = None
    player_slug: str | None = None
    position: str | None = None
    season_totals: list[dict[str, Any]] | None = None
    shoots_catches: str | None = None
    shop_link: str | None = None
    sweater_number: int | None = None
    team_common_name: LocalizedName | None = None
    team_logo: str | None = None
    team_place_name_with_preposition: LocalizedName | None = None
    twitter_link: str | None = None
    watch_link: str | None = None
    weight_in_kilograms: int | None = None
    weight_in_pounds: int | None = None


class PlayerSearchResult(msgspec.Struct, rename='camel'):
    """A player returned by the search API."""

    player_id: str
    name: str
    active: bool | None = None
    birth_city: str | None = None
    birth_country: str | None = None
    birth_state_province: str | None = None
    height: str | None = None
    height_in_centimeters: int | None = None
    height_in_inches: int | None = None
    last_season_id: str | int | None = None
    last_team_abbrev: str | None = None
    last_team_id: str | int | None = None
    position_code: str | None = None
    sweater_number: int | None = None
    team_abbrev: str | None = None
    team_id: str | int | None = None
    weight_in_kilograms: int | None = None
    weight_in_pounds: int | None = None
