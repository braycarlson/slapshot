from __future__ import annotations

from typing_extensions import Any

from slapshot.endpoints import WebEndpoint
from slapshot.models import StandingsResponse
from slapshot.request import Request, request_build
from slapshot.resource import AsyncResource, SyncResource
from slapshot.validation import date_validate


def standings_by_date(date: str) -> Request:
    date_validate(date)

    url = WebEndpoint.STANDINGS_BY_DATE.format(date=date)
    return request_build(url)


def standings_now() -> Request:
    return request_build(WebEndpoint.STANDINGS_NOW)


def standings_seasons() -> Request:
    return request_build(WebEndpoint.STANDINGS_SEASONS)


class Standings(SyncResource):
    """The standings endpoints on the web API.

    Every method may raise an NHLError subclass on a transport failure or an
    error response.
    """

    def by_date(self, date: str) -> StandingsResponse:
        """It returns the standings as of a date.

        Args:
            date: An ISO date, YYYY-MM-DD.

        Returns:
            The standings for the date.

        Raises:
            InvalidDateError: If date is not ISO format YYYY-MM-DD.
        """

        request = standings_by_date(date)
        return self._get_model(request, StandingsResponse)

    def now(self) -> StandingsResponse:
        """It returns the current standings."""

        request = standings_now()
        return self._get_model(request, StandingsResponse)

    def seasons(self) -> Any:
        """It returns the season identifiers and standings metadata."""

        request = standings_seasons()
        return self._get(request)


class AsyncStandings(AsyncResource):
    """The asynchronous standings endpoints on the web API.

    Every method may raise an NHLError subclass on a transport failure or an
    error response.
    """

    async def by_date(self, date: str) -> StandingsResponse:
        """It returns the standings as of a date.

        Args:
            date: An ISO date, YYYY-MM-DD.

        Returns:
            The standings for the date.

        Raises:
            InvalidDateError: If date is not ISO format YYYY-MM-DD.
        """

        request = standings_by_date(date)
        return await self._get_model(request, StandingsResponse)

    async def now(self) -> StandingsResponse:
        """It returns the current standings."""

        request = standings_now()
        return await self._get_model(request, StandingsResponse)

    async def seasons(self) -> Any:
        """It returns the season identifiers and standings metadata."""

        request = standings_seasons()
        return await self._get(request)
