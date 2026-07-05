from __future__ import annotations

from typing_extensions import Any

from slapshot.endpoints import WebEndpoint
from slapshot.exceptions import InvalidDraftRoundError
from slapshot.request import Request, request_build
from slapshot.resource import AsyncResource, SyncResource
from slapshot.validation import identifier_validate


def draft_picks(year: int | None, draft_round: int | str) -> Request:
    if year is None:
        return request_build(WebEndpoint.DRAFT_PICKS_NOW)

    identifier_validate(year, name='year')

    if isinstance(draft_round, int) and draft_round < 1:
        raise InvalidDraftRoundError(draft_round)

    url = WebEndpoint.DRAFT_PICKS.format(year=year, round=draft_round)
    return request_build(url)


def draft_rankings(year: int | None, category: int) -> Request:
    if year is None:
        return request_build(WebEndpoint.DRAFT_RANKINGS_NOW)

    identifier_validate(year, name='year')

    url = WebEndpoint.DRAFT_RANKINGS.format(year=year, category=category)
    return request_build(url)


class Draft(SyncResource):
    """The draft endpoints on the web API.

    Every method may raise an NHLError subclass on a transport failure or an
    error response.
    """

    def picks(self, year: int | None = None, *, draft_round: int | str = 1) -> Any:
        """It returns draft picks, or the current picks when year is omitted.

        Args:
            year: The draft year, or None for the current picks.
            draft_round: A round number of at least 1, or a string such as 'all'.

        Returns:
            The decoded draft picks payload.

        Raises:
            InvalidIdentifierError: If year is not a positive integer.
            InvalidDraftRoundError: If draft_round is an integer less than 1.
        """

        request = draft_picks(year, draft_round)
        return self._get(request)

    def rankings(self, year: int | None = None, *, category: int = 1) -> Any:
        """It returns draft rankings, or the current rankings when year is omitted.

        Args:
            year: The draft year, or None for the current rankings.
            category: The prospect category.

        Returns:
            The decoded draft rankings payload.

        Raises:
            InvalidIdentifierError: If year is not a positive integer.
        """

        request = draft_rankings(year, category)
        return self._get(request)


class AsyncDraft(AsyncResource):
    """The asynchronous draft endpoints on the web API.

    Every method may raise an NHLError subclass on a transport failure or an
    error response.
    """

    async def picks(self, year: int | None = None, *, draft_round: int | str = 1) -> Any:
        """It returns draft picks, or the current picks when year is omitted.

        Args:
            year: The draft year, or None for the current picks.
            draft_round: A round number of at least 1, or a string such as 'all'.

        Returns:
            The decoded draft picks payload.

        Raises:
            InvalidIdentifierError: If year is not a positive integer.
            InvalidDraftRoundError: If draft_round is an integer less than 1.
        """

        request = draft_picks(year, draft_round)
        return await self._get(request)

    async def rankings(self, year: int | None = None, *, category: int = 1) -> Any:
        """It returns draft rankings, or the current rankings when year is omitted.

        Args:
            year: The draft year, or None for the current rankings.
            category: The prospect category.

        Returns:
            The decoded draft rankings payload.

        Raises:
            InvalidIdentifierError: If year is not a positive integer.
        """

        request = draft_rankings(year, category)
        return await self._get(request)
