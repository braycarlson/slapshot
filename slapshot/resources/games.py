from __future__ import annotations

from typing_extensions import Any

from slapshot.endpoints import WebEndpoint
from slapshot.request import Request, request_build
from slapshot.resource import AsyncResource, SyncResource
from slapshot.validation import date_validate, identifier_validate


def game_boxscore(game: int) -> Request:
    identifier_validate(game, name='game')

    url = WebEndpoint.GAME_BOXSCORE.format(game=game)
    return request_build(url)


def game_landing(game: int) -> Request:
    identifier_validate(game, name='game')

    url = WebEndpoint.GAME_LANDING.format(game=game)
    return request_build(url)


def game_play_by_play(game: int) -> Request:
    identifier_validate(game, name='game')

    url = WebEndpoint.GAME_PLAY_BY_PLAY.format(game=game)
    return request_build(url)


def game_right_rail(game: int) -> Request:
    identifier_validate(game, name='game')

    url = WebEndpoint.GAME_RIGHT_RAIL.format(game=game)
    return request_build(url)


def game_story(game: int) -> Request:
    identifier_validate(game, name='game')

    url = WebEndpoint.GAME_STORY.format(game=game)
    return request_build(url)


def scoreboard_now() -> Request:
    return request_build(WebEndpoint.SCOREBOARD_NOW)


def scores_by_date(date: str | None) -> Request:
    if date is None:
        return request_build(WebEndpoint.SCORES_NOW)

    date_validate(date)

    url = WebEndpoint.SCORES_BY_DATE.format(date=date)
    return request_build(url)


class Games(SyncResource):
    """The game endpoints on the web API.

    Every method may raise an NHLError subclass on a transport failure or an
    error response.
    """

    def boxscore(self, game: int) -> Any:
        """It returns the boxscore for a game.

        Args:
            game: A game identifier.

        Returns:
            The decoded boxscore payload.

        Raises:
            InvalidIdentifierError: If game is not a positive integer.
        """

        request = game_boxscore(game)
        return self._get(request)

    def landing(self, game: int) -> Any:
        """It returns the landing summary for a game.

        Args:
            game: A game identifier.

        Returns:
            The decoded landing payload.

        Raises:
            InvalidIdentifierError: If game is not a positive integer.
        """

        request = game_landing(game)
        return self._get(request)

    def play_by_play(self, game: int) -> Any:
        """It returns the play-by-play events for a game.

        Args:
            game: A game identifier.

        Returns:
            The decoded play-by-play payload.

        Raises:
            InvalidIdentifierError: If game is not a positive integer.
        """

        request = game_play_by_play(game)
        return self._get(request)

    def right_rail(self, game: int) -> Any:
        """It returns the right-rail content for a game.

        Args:
            game: A game identifier.

        Returns:
            The decoded right-rail payload.

        Raises:
            InvalidIdentifierError: If game is not a positive integer.
        """

        request = game_right_rail(game)
        return self._get(request)

    def scoreboard(self) -> Any:
        """It returns the current scoreboard."""

        request = scoreboard_now()
        return self._get(request)

    def scores(self, date: str | None = None) -> Any:
        """It returns the scores for a date, or the current day when omitted.

        Args:
            date: An ISO date, YYYY-MM-DD, or None for the current day.

        Returns:
            The decoded scores payload.

        Raises:
            InvalidDateError: If date is not ISO format YYYY-MM-DD.
        """

        request = scores_by_date(date)
        return self._get(request)

    def story(self, game: int) -> Any:
        """It returns the editorial story for a game.

        Args:
            game: A game identifier.

        Returns:
            The decoded story payload.

        Raises:
            InvalidIdentifierError: If game is not a positive integer.
        """

        request = game_story(game)
        return self._get(request)


class AsyncGames(AsyncResource):
    """The asynchronous game endpoints on the web API.

    Every method may raise an NHLError subclass on a transport failure or an
    error response.
    """

    async def boxscore(self, game: int) -> Any:
        """It returns the boxscore for a game.

        Args:
            game: A game identifier.

        Returns:
            The decoded boxscore payload.

        Raises:
            InvalidIdentifierError: If game is not a positive integer.
        """

        request = game_boxscore(game)
        return await self._get(request)

    async def landing(self, game: int) -> Any:
        """It returns the landing summary for a game.

        Args:
            game: A game identifier.

        Returns:
            The decoded landing payload.

        Raises:
            InvalidIdentifierError: If game is not a positive integer.
        """

        request = game_landing(game)
        return await self._get(request)

    async def play_by_play(self, game: int) -> Any:
        """It returns the play-by-play events for a game.

        Args:
            game: A game identifier.

        Returns:
            The decoded play-by-play payload.

        Raises:
            InvalidIdentifierError: If game is not a positive integer.
        """

        request = game_play_by_play(game)
        return await self._get(request)

    async def right_rail(self, game: int) -> Any:
        """It returns the right-rail content for a game.

        Args:
            game: A game identifier.

        Returns:
            The decoded right-rail payload.

        Raises:
            InvalidIdentifierError: If game is not a positive integer.
        """

        request = game_right_rail(game)
        return await self._get(request)

    async def scoreboard(self) -> Any:
        """It returns the current scoreboard."""

        request = scoreboard_now()
        return await self._get(request)

    async def scores(self, date: str | None = None) -> Any:
        """It returns the scores for a date, or the current day when omitted.

        Args:
            date: An ISO date, YYYY-MM-DD, or None for the current day.

        Returns:
            The decoded scores payload.

        Raises:
            InvalidDateError: If date is not ISO format YYYY-MM-DD.
        """

        request = scores_by_date(date)
        return await self._get(request)

    async def story(self, game: int) -> Any:
        """It returns the editorial story for a game.

        Args:
            game: A game identifier.

        Returns:
            The decoded story payload.

        Raises:
            InvalidIdentifierError: If game is not a positive integer.
        """

        request = game_story(game)
        return await self._get(request)
