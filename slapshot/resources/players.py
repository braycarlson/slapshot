from __future__ import annotations

from typing_extensions import Any

from slapshot.endpoints import SearchEndpoint, WebEndpoint
from slapshot.enums import GameType
from slapshot.exceptions import InvalidQueryError
from slapshot.models import PlayerLanding, PlayerSearchResult
from slapshot.request import Request, request_build
from slapshot.resource import AsyncResource, SyncResource
from slapshot.validation import identifier_validate, pagination_validate, season_validate


LEADERS_LIMIT_DEFAULT = 5
SEARCH_LIMIT_DEFAULT = 20


def goalie_leaders(
    season: int | None, game_type: GameType | int, categories: str | None, limit: int
) -> Request:
    pagination_validate(limit, 0)

    params = {'categories': categories, 'limit': limit}

    if season is None:
        return request_build(WebEndpoint.GOALIE_LEADERS_CURRENT, params)

    season_validate(season)

    url = WebEndpoint.GOALIE_LEADERS.format(season=season, game_type=game_type)
    return request_build(url, params)


def player_game_log(player: int, season: int | None, game_type: GameType | int) -> Request:
    identifier_validate(player, name='player')

    if season is None:
        url = WebEndpoint.PLAYER_GAME_LOG_NOW.format(player=player)
        return request_build(url)

    season_validate(season)

    url = WebEndpoint.PLAYER_GAME_LOG.format(player=player, season=season, game_type=game_type)
    return request_build(url)


def player_landing(player: int) -> Request:
    identifier_validate(player, name='player')

    url = WebEndpoint.PLAYER_LANDING.format(player=player)
    return request_build(url)


def player_search(query: str, limit: int, active: bool | None, culture: str) -> Request:
    if not query:
        raise InvalidQueryError

    pagination_validate(limit, 0)

    return request_build(
        SearchEndpoint.PLAYER, {'culture': culture, 'q': query, 'limit': limit, 'active': active}
    )


def player_spotlight() -> Request:
    return request_build(WebEndpoint.PLAYER_SPOTLIGHT)


def skater_leaders(
    season: int | None, game_type: GameType | int, categories: str | None, limit: int
) -> Request:
    pagination_validate(limit, 0)

    params = {'categories': categories, 'limit': limit}

    if season is None:
        return request_build(WebEndpoint.SKATER_LEADERS_CURRENT, params)

    season_validate(season)

    url = WebEndpoint.SKATER_LEADERS.format(season=season, game_type=game_type)
    return request_build(url, params)


class Players(SyncResource):
    """The player endpoints on the web and search APIs.

    Every method may raise an NHLError subclass on a transport failure or an
    error response.
    """

    def game_log(
        self,
        player: int,
        *,
        season: int | None = None,
        game_type: GameType | int = GameType.REGULAR,
    ) -> Any:
        """It returns a player's game log, or the current log when season is omitted.

        Args:
            player: A player identifier.
            season: An eight-digit season, YYYYYYYY, or None for the current log.
            game_type: The game type to report.

        Returns:
            The decoded game log payload.

        Raises:
            InvalidIdentifierError: If player is not a positive integer.
            InvalidSeasonError: If season is not two consecutive years.
        """

        request = player_game_log(player, season, game_type)
        return self._get(request)

    def goalie_leaders(
        self,
        *,
        season: int | None = None,
        game_type: GameType | int = GameType.REGULAR,
        categories: str | None = None,
        limit: int = LEADERS_LIMIT_DEFAULT,
    ) -> Any:
        """It returns the goalie statistical leaders.

        Args:
            season: An eight-digit season, YYYYYYYY, or None for the current leaders.
            game_type: The game type to report.
            categories: A comma-separated list of categories, or None for the default.
            limit: The maximum number of leaders per category.

        Returns:
            The decoded leaders payload.

        Raises:
            InvalidLimitError: If limit is not a positive integer.
            InvalidSeasonError: If season is not two consecutive years.
        """

        request = goalie_leaders(season, game_type, categories, limit)
        return self._get(request)

    def landing(self, player: int) -> PlayerLanding:
        """It returns a player's landing profile.

        Args:
            player: A player identifier.

        Returns:
            The player profile.

        Raises:
            InvalidIdentifierError: If player is not a positive integer.
        """

        request = player_landing(player)
        return self._get_model(request, PlayerLanding)

    def search(
        self,
        query: str,
        *,
        limit: int = SEARCH_LIMIT_DEFAULT,
        active: bool | None = None,
        culture: str = 'en-us',
    ) -> list[PlayerSearchResult]:
        """It searches for players by name.

        Args:
            query: The search text. Must not be empty.
            limit: The maximum number of results.
            active: Restrict to active players, inactive players, or all when None.
            culture: The culture code for the search.

        Returns:
            The matching players.

        Raises:
            InvalidQueryError: If query is empty.
            InvalidLimitError: If limit is not a positive integer.
        """

        request = player_search(query, limit, active, culture)
        return self._get_model(request, list[PlayerSearchResult])

    def skater_leaders(
        self,
        *,
        season: int | None = None,
        game_type: GameType | int = GameType.REGULAR,
        categories: str | None = None,
        limit: int = LEADERS_LIMIT_DEFAULT,
    ) -> Any:
        """It returns the skater statistical leaders.

        Args:
            season: An eight-digit season, YYYYYYYY, or None for the current leaders.
            game_type: The game type to report.
            categories: A comma-separated list of categories, or None for the default.
            limit: The maximum number of leaders per category.

        Returns:
            The decoded leaders payload.

        Raises:
            InvalidLimitError: If limit is not a positive integer.
            InvalidSeasonError: If season is not two consecutive years.
        """

        request = skater_leaders(season, game_type, categories, limit)
        return self._get(request)

    def spotlight(self) -> Any:
        """It returns the spotlighted players."""

        request = player_spotlight()
        return self._get(request)


class AsyncPlayers(AsyncResource):
    """The asynchronous player endpoints on the web and search APIs.

    Every method may raise an NHLError subclass on a transport failure or an
    error response.
    """

    async def game_log(
        self,
        player: int,
        *,
        season: int | None = None,
        game_type: GameType | int = GameType.REGULAR,
    ) -> Any:
        """It returns a player's game log, or the current log when season is omitted.

        Args:
            player: A player identifier.
            season: An eight-digit season, YYYYYYYY, or None for the current log.
            game_type: The game type to report.

        Returns:
            The decoded game log payload.

        Raises:
            InvalidIdentifierError: If player is not a positive integer.
            InvalidSeasonError: If season is not two consecutive years.
        """

        request = player_game_log(player, season, game_type)
        return await self._get(request)

    async def goalie_leaders(
        self,
        *,
        season: int | None = None,
        game_type: GameType | int = GameType.REGULAR,
        categories: str | None = None,
        limit: int = LEADERS_LIMIT_DEFAULT,
    ) -> Any:
        """It returns the goalie statistical leaders.

        Args:
            season: An eight-digit season, YYYYYYYY, or None for the current leaders.
            game_type: The game type to report.
            categories: A comma-separated list of categories, or None for the default.
            limit: The maximum number of leaders per category.

        Returns:
            The decoded leaders payload.

        Raises:
            InvalidLimitError: If limit is not a positive integer.
            InvalidSeasonError: If season is not two consecutive years.
        """

        request = goalie_leaders(season, game_type, categories, limit)
        return await self._get(request)

    async def landing(self, player: int) -> PlayerLanding:
        """It returns a player's landing profile.

        Args:
            player: A player identifier.

        Returns:
            The player profile.

        Raises:
            InvalidIdentifierError: If player is not a positive integer.
        """

        request = player_landing(player)
        return await self._get_model(request, PlayerLanding)

    async def search(
        self,
        query: str,
        *,
        limit: int = SEARCH_LIMIT_DEFAULT,
        active: bool | None = None,
        culture: str = 'en-us',
    ) -> list[PlayerSearchResult]:
        """It searches for players by name.

        Args:
            query: The search text. Must not be empty.
            limit: The maximum number of results.
            active: Restrict to active players, inactive players, or all when None.
            culture: The culture code for the search.

        Returns:
            The matching players.

        Raises:
            InvalidQueryError: If query is empty.
            InvalidLimitError: If limit is not a positive integer.
        """

        request = player_search(query, limit, active, culture)
        return await self._get_model(request, list[PlayerSearchResult])

    async def skater_leaders(
        self,
        *,
        season: int | None = None,
        game_type: GameType | int = GameType.REGULAR,
        categories: str | None = None,
        limit: int = LEADERS_LIMIT_DEFAULT,
    ) -> Any:
        """It returns the skater statistical leaders.

        Args:
            season: An eight-digit season, YYYYYYYY, or None for the current leaders.
            game_type: The game type to report.
            categories: A comma-separated list of categories, or None for the default.
            limit: The maximum number of leaders per category.

        Returns:
            The decoded leaders payload.

        Raises:
            InvalidLimitError: If limit is not a positive integer.
            InvalidSeasonError: If season is not two consecutive years.
        """

        request = skater_leaders(season, game_type, categories, limit)
        return await self._get(request)

    async def spotlight(self) -> Any:
        """It returns the spotlighted players."""

        request = player_spotlight()
        return await self._get(request)
