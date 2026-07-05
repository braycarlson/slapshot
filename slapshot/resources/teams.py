from __future__ import annotations

from typing_extensions import Any

from slapshot.endpoints import WebEndpoint
from slapshot.enums import GameType, Team
from slapshot.models import Roster
from slapshot.request import Request, request_build
from slapshot.resource import AsyncResource, SyncResource
from slapshot.validation import season_validate


def club_stats(team: Team | str, season: int | None, game_type: GameType | int) -> Request:
    if season is None:
        url = WebEndpoint.CLUB_STATS_NOW.format(team=team)
        return request_build(url)

    season_validate(season)
    url = WebEndpoint.CLUB_STATS.format(team=team, season=season, game_type=game_type)
    return request_build(url)


def club_stats_seasons(team: Team | str) -> Request:
    url = WebEndpoint.CLUB_STATS_SEASONS.format(team=team)
    return request_build(url)


def prospects(team: Team | str) -> Request:
    url = WebEndpoint.PROSPECTS.format(team=team)
    return request_build(url)


def roster(team: Team | str, season: int | None) -> Request:
    if season is None:
        url = WebEndpoint.ROSTER_CURRENT.format(team=team)
        return request_build(url)

    season_validate(season)
    url = WebEndpoint.ROSTER.format(team=team, season=season)
    return request_build(url)


def roster_seasons(team: Team | str) -> Request:
    url = WebEndpoint.ROSTER_SEASONS.format(team=team)
    return request_build(url)


class Teams(SyncResource):
    """The team endpoints on the web API.

    Every method may raise an NHLError subclass on a transport failure or an
    error response.
    """

    def club_stats(
        self,
        team: Team | str,
        *,
        season: int | None = None,
        game_type: GameType | int = GameType.REGULAR,
    ) -> Any:
        """It returns a team's club statistics, or the current stats when omitted.

        Args:
            team: A Team enum or three-letter abbreviation.
            season: An eight-digit season, YYYYYYYY, or None for the current stats.
            game_type: The game type to report.

        Returns:
            The decoded club statistics payload.

        Raises:
            InvalidSeasonError: If season is not two consecutive years.
        """

        request = club_stats(team, season, game_type)
        return self._get(request)

    def club_stats_seasons(self, team: Team | str) -> Any:
        """It returns the seasons for which a team has club statistics.

        Args:
            team: A Team enum or three-letter abbreviation.

        Returns:
            The decoded seasons payload.
        """

        request = club_stats_seasons(team)
        return self._get(request)

    def prospects(self, team: Team | str) -> Any:
        """It returns a team's prospects.

        Args:
            team: A Team enum or three-letter abbreviation.

        Returns:
            The decoded prospects payload.
        """

        request = prospects(team)
        return self._get(request)

    def roster(self, team: Team | str, *, season: int | None = None) -> Roster:
        """It returns a team's roster, or the current roster when season is omitted.

        Args:
            team: A Team enum or three-letter abbreviation.
            season: An eight-digit season, YYYYYYYY, or None for the current roster.

        Returns:
            The team roster.

        Raises:
            InvalidSeasonError: If season is not two consecutive years.
        """

        request = roster(team, season)
        return self._get_model(request, Roster)

    def roster_seasons(self, team: Team | str) -> Any:
        """It returns the seasons for which a team roster exists.

        Args:
            team: A Team enum or three-letter abbreviation.

        Returns:
            The decoded seasons payload.
        """

        request = roster_seasons(team)
        return self._get(request)


class AsyncTeams(AsyncResource):
    """The asynchronous team endpoints on the web API.

    Every method may raise an NHLError subclass on a transport failure or an
    error response.
    """

    async def club_stats(
        self,
        team: Team | str,
        *,
        season: int | None = None,
        game_type: GameType | int = GameType.REGULAR,
    ) -> Any:
        """It returns a team's club statistics, or the current stats when omitted.

        Args:
            team: A Team enum or three-letter abbreviation.
            season: An eight-digit season, YYYYYYYY, or None for the current stats.
            game_type: The game type to report.

        Returns:
            The decoded club statistics payload.

        Raises:
            InvalidSeasonError: If season is not two consecutive years.
        """

        request = club_stats(team, season, game_type)
        return await self._get(request)

    async def club_stats_seasons(self, team: Team | str) -> Any:
        """It returns the seasons for which a team has club statistics.

        Args:
            team: A Team enum or three-letter abbreviation.

        Returns:
            The decoded seasons payload.
        """

        request = club_stats_seasons(team)
        return await self._get(request)

    async def prospects(self, team: Team | str) -> Any:
        """It returns a team's prospects.

        Args:
            team: A Team enum or three-letter abbreviation.

        Returns:
            The decoded prospects payload.
        """

        request = prospects(team)
        return await self._get(request)

    async def roster(self, team: Team | str, *, season: int | None = None) -> Roster:
        """It returns a team's roster, or the current roster when season is omitted.

        Args:
            team: A Team enum or three-letter abbreviation.
            season: An eight-digit season, YYYYYYYY, or None for the current roster.

        Returns:
            The team roster.

        Raises:
            InvalidSeasonError: If season is not two consecutive years.
        """

        request = roster(team, season)
        return await self._get_model(request, Roster)

    async def roster_seasons(self, team: Team | str) -> Any:
        """It returns the seasons for which a team roster exists.

        Args:
            team: A Team enum or three-letter abbreviation.

        Returns:
            The decoded seasons payload.
        """

        request = roster_seasons(team)
        return await self._get(request)
