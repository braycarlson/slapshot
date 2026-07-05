from __future__ import annotations

from typing_extensions import Any, TYPE_CHECKING

from slapshot.endpoints import WebEndpoint
from slapshot.request import Request, request_build
from slapshot.resource import AsyncResource, SyncResource
from slapshot.validation import date_validate, month_validate, season_validate

if TYPE_CHECKING:
    from slapshot.enums import Team


def schedule_by_date(date: str) -> Request:
    date_validate(date)

    url = WebEndpoint.SCHEDULE_BY_DATE.format(date=date)
    return request_build(url)


def schedule_club_month(team: Team | str, month: str | None) -> Request:
    if month is None:
        url = WebEndpoint.SCHEDULE_CLUB_MONTH_NOW.format(team=team)
        return request_build(url)

    month_validate(month)

    url = WebEndpoint.SCHEDULE_CLUB_MONTH.format(team=team, month=month)
    return request_build(url)


def schedule_club_season(team: Team | str, season: int) -> Request:
    season_validate(season)

    url = WebEndpoint.SCHEDULE_CLUB_SEASON.format(team=team, season=season)
    return request_build(url)


def schedule_club_week(team: Team | str, date: str | None) -> Request:
    if date is None:
        url = WebEndpoint.SCHEDULE_CLUB_WEEK_NOW.format(team=team)
        return request_build(url)

    date_validate(date)

    url = WebEndpoint.SCHEDULE_CLUB_WEEK.format(team=team, date=date)
    return request_build(url)


def schedule_now() -> Request:
    return request_build(WebEndpoint.SCHEDULE_NOW)


class Schedule(SyncResource):
    """The schedule endpoints on the web API.

    Every method may raise an NHLError subclass on a transport failure or an
    error response.
    """

    def by_date(self, date: str) -> Any:
        """It returns the league schedule for a date.

        Args:
            date: An ISO date, YYYY-MM-DD.

        Returns:
            The decoded schedule payload.

        Raises:
            InvalidDateError: If date is not ISO format YYYY-MM-DD.
        """

        request = schedule_by_date(date)
        return self._get(request)

    def club_month(self, team: Team | str, *, month: str | None = None) -> Any:
        """It returns a team's monthly schedule, or the current month when omitted.

        Args:
            team: A Team enum or three-letter abbreviation.
            month: A year and month, YYYY-MM, or None for the current month.

        Returns:
            The decoded schedule payload.

        Raises:
            InvalidMonthError: If month is not YYYY-MM.
        """

        request = schedule_club_month(team, month)
        return self._get(request)

    def club_season(self, team: Team | str, season: int) -> Any:
        """It returns a team's full-season schedule.

        Args:
            team: A Team enum or three-letter abbreviation.
            season: An eight-digit season, YYYYYYYY.

        Returns:
            The decoded schedule payload.

        Raises:
            InvalidSeasonError: If season is not two consecutive years.
        """

        request = schedule_club_season(team, season)
        return self._get(request)

    def club_week(self, team: Team | str, *, date: str | None = None) -> Any:
        """It returns a team's weekly schedule, or the current week when omitted.

        Args:
            team: A Team enum or three-letter abbreviation.
            date: An ISO date, YYYY-MM-DD, or None for the current week.

        Returns:
            The decoded schedule payload.

        Raises:
            InvalidDateError: If date is not ISO format YYYY-MM-DD.
        """

        request = schedule_club_week(team, date)
        return self._get(request)

    def now(self) -> Any:
        """It returns the league schedule for the current day."""

        request = schedule_now()
        return self._get(request)


class AsyncSchedule(AsyncResource):
    """The asynchronous schedule endpoints on the web API.

    Every method may raise an NHLError subclass on a transport failure or an
    error response.
    """

    async def by_date(self, date: str) -> Any:
        """It returns the league schedule for a date.

        Args:
            date: An ISO date, YYYY-MM-DD.

        Returns:
            The decoded schedule payload.

        Raises:
            InvalidDateError: If date is not ISO format YYYY-MM-DD.
        """

        request = schedule_by_date(date)
        return await self._get(request)

    async def club_month(self, team: Team | str, *, month: str | None = None) -> Any:
        """It returns a team's monthly schedule, or the current month when omitted.

        Args:
            team: A Team enum or three-letter abbreviation.
            month: A year and month, YYYY-MM, or None for the current month.

        Returns:
            The decoded schedule payload.

        Raises:
            InvalidMonthError: If month is not YYYY-MM.
        """

        request = schedule_club_month(team, month)
        return await self._get(request)

    async def club_season(self, team: Team | str, season: int) -> Any:
        """It returns a team's full-season schedule.

        Args:
            team: A Team enum or three-letter abbreviation.
            season: An eight-digit season, YYYYYYYY.

        Returns:
            The decoded schedule payload.

        Raises:
            InvalidSeasonError: If season is not two consecutive years.
        """

        request = schedule_club_season(team, season)
        return await self._get(request)

    async def club_week(self, team: Team | str, *, date: str | None = None) -> Any:
        """It returns a team's weekly schedule, or the current week when omitted.

        Args:
            team: A Team enum or three-letter abbreviation.
            date: An ISO date, YYYY-MM-DD, or None for the current week.

        Returns:
            The decoded schedule payload.

        Raises:
            InvalidDateError: If date is not ISO format YYYY-MM-DD.
        """

        request = schedule_club_week(team, date)
        return await self._get(request)

    async def now(self) -> Any:
        """It returns the league schedule for the current day."""

        request = schedule_now()
        return await self._get(request)
