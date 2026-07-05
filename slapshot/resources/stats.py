from __future__ import annotations

from typing_extensions import Any, Sequence

from slapshot.endpoints import StatsEndpoint
from slapshot.enums import GameType, Language, SortDirection
from slapshot.models import ResultSet
from slapshot.request import Request, cayenne_build, request_build, sort_build
from slapshot.resource import AsyncResource, SyncResource
from slapshot.validation import pagination_validate, season_validate


REPORT_LIMIT_DEFAULT = 50

GOALIE_SORT_DEFAULT = ({'property': 'wins', 'direction': SortDirection.DESCENDING},)
SKATER_SORT_DEFAULT = ({'property': 'points', 'direction': SortDirection.DESCENDING},)
TEAM_SORT_DEFAULT = ({'property': 'points', 'direction': SortDirection.DESCENDING},)


def stats_config(language: Language | str) -> Request:
    url = StatsEndpoint.CONFIG.format(language=language)
    return request_build(url)


def stats_franchises(language: Language | str) -> Request:
    url = StatsEndpoint.FRANCHISES.format(language=language)
    return request_build(url)


def stats_glossary(language: Language | str) -> Request:
    url = StatsEndpoint.GLOSSARY.format(language=language)
    return request_build(url)


def stats_report(
    language: Language | str,
    subject: str,
    report: str,
    season: int | None,
    game_type: GameType | int | None,
    sort: str | Sequence[dict[str, str]] | None,
    limit: int,
    start: int,
    aggregate: bool,
    game: bool,
    cayenne: str | dict[str, Any] | None,
) -> Request:
    if season is not None:
        season_validate(season)

    pagination_validate(limit, start)

    if isinstance(cayenne, str):
        expression = cayenne
    else:
        conditions: dict[str, Any] = {'seasonId': season, 'gameTypeId': game_type}

        if cayenne is not None:
            conditions.update(cayenne)

        expression = cayenne_build(conditions)

    url = StatsEndpoint.REPORT.format(language=language, subject=subject, report=report)

    aggregate_flag = 'true' if aggregate else None
    game_flag = 'true' if game else None

    return request_build(
        url,
        {
            'limit': limit,
            'start': start,
            'sort': sort_build(sort),
            'isAggregate': aggregate_flag,
            'isGame': game_flag,
            'cayenneExp': expression,
        },
    )


def stats_seasons(language: Language | str) -> Request:
    url = StatsEndpoint.SEASONS.format(language=language)
    return request_build(url)


class Stats(SyncResource):
    """The stats endpoints on the stats API.

    Every method may raise an NHLError subclass on a transport failure or an
    error response.
    """

    def config(self, language: Language | str = Language.ENGLISH) -> Any:
        """It returns the configuration metadata.

        Args:
            language: The response language.

        Returns:
            The decoded configuration payload.
        """

        request = stats_config(language)
        return self._get(request)

    def franchises(self, language: Language | str = Language.ENGLISH) -> ResultSet:
        """It returns the franchises.

        Args:
            language: The response language.

        Returns:
            The franchises.
        """

        request = stats_franchises(language)
        return self._get_model(request, ResultSet)

    def glossary(self, language: Language | str = Language.ENGLISH) -> ResultSet:
        """It returns the statistic glossary.

        Args:
            language: The response language.

        Returns:
            The glossary entries.
        """

        request = stats_glossary(language)
        return self._get_model(request, ResultSet)

    def goalies(
        self,
        report: str = 'summary',
        *,
        season: int | None = None,
        game_type: GameType | int | None = None,
        sort: str | Sequence[dict[str, str]] | None = None,
        limit: int = REPORT_LIMIT_DEFAULT,
        start: int = 0,
        aggregate: bool = False,
        game: bool = False,
        cayenne: str | dict[str, Any] | None = None,
        language: Language | str = Language.ENGLISH,
    ) -> ResultSet:
        """It returns a goalie report.

        It sorts by wins descending by default. It accepts the same keyword arguments
        as report().

        Args:
            report: The report name, such as summary or bios.

        Returns:
            The report rows.

        Raises:
            InvalidSeasonError: If season is not two consecutive years.
            InvalidLimitError: If limit is not a positive integer.
            InvalidStartError: If start is negative.
            InvalidCayenneValueError: If a cayenne string value contains a double quote.
        """

        sorting = GOALIE_SORT_DEFAULT if sort is None else sort

        request = stats_report(
            language,
            'goalie',
            report,
            season,
            game_type,
            sorting,
            limit,
            start,
            aggregate,
            game,
            cayenne,
        )

        return self._get_model(request, ResultSet)

    def report(
        self,
        subject: str,
        report: str,
        *,
        season: int | None = None,
        game_type: GameType | int | None = None,
        sort: str | Sequence[dict[str, str]] | None = None,
        limit: int = REPORT_LIMIT_DEFAULT,
        start: int = 0,
        aggregate: bool = False,
        game: bool = False,
        cayenne: str | dict[str, Any] | None = None,
        language: Language | str = Language.ENGLISH,
    ) -> ResultSet:
        """It returns an arbitrary report for a subject.

        Args:
            subject: The report subject, such as skater, goalie, or team.
            report: The report name, such as summary or bios.
            season: An eight-digit season, YYYYYYYY, added to the query as seasonId.
            game_type: The game type, added to the query as gameTypeId.
            sort: A property name, a sequence of property and direction mappings, or None.
            limit: The page size.
            start: The page offset.
            aggregate: Aggregate rows across seasons.
            game: Return per-game rows.
            cayenne: A raw cayenne expression, or a mapping merged into the built expression.
            language: The response language.

        Returns:
            The report rows.

        Raises:
            InvalidSeasonError: If season is not two consecutive years.
            InvalidLimitError: If limit is not a positive integer.
            InvalidStartError: If start is negative.
            InvalidCayenneValueError: If a cayenne string value contains a double quote.
        """

        request = stats_report(
            language,
            subject,
            report,
            season,
            game_type,
            sort,
            limit,
            start,
            aggregate,
            game,
            cayenne,
        )

        return self._get_model(request, ResultSet)

    def seasons(self, language: Language | str = Language.ENGLISH) -> ResultSet:
        """It returns the seasons.

        Args:
            language: The response language.

        Returns:
            The seasons.
        """

        request = stats_seasons(language)
        return self._get_model(request, ResultSet)

    def skaters(
        self,
        report: str = 'summary',
        *,
        season: int | None = None,
        game_type: GameType | int | None = None,
        sort: str | Sequence[dict[str, str]] | None = None,
        limit: int = REPORT_LIMIT_DEFAULT,
        start: int = 0,
        aggregate: bool = False,
        game: bool = False,
        cayenne: str | dict[str, Any] | None = None,
        language: Language | str = Language.ENGLISH,
    ) -> ResultSet:
        """It returns a skater report.

        It sorts by points descending by default. It accepts the same keyword
        arguments as report().

        Args:
            report: The report name, such as summary or bios.

        Returns:
            The report rows.

        Raises:
            InvalidSeasonError: If season is not two consecutive years.
            InvalidLimitError: If limit is not a positive integer.
            InvalidStartError: If start is negative.
            InvalidCayenneValueError: If a cayenne string value contains a double quote.
        """

        sorting = SKATER_SORT_DEFAULT if sort is None else sort

        request = stats_report(
            language,
            'skater',
            report,
            season,
            game_type,
            sorting,
            limit,
            start,
            aggregate,
            game,
            cayenne,
        )

        return self._get_model(request, ResultSet)

    def teams(
        self,
        report: str = 'summary',
        *,
        season: int | None = None,
        game_type: GameType | int | None = None,
        sort: str | Sequence[dict[str, str]] | None = None,
        limit: int = REPORT_LIMIT_DEFAULT,
        start: int = 0,
        aggregate: bool = False,
        game: bool = False,
        cayenne: str | dict[str, Any] | None = None,
        language: Language | str = Language.ENGLISH,
    ) -> ResultSet:
        """It returns a team report.

        It sorts by points descending by default. It accepts the same keyword
        arguments as report().

        Args:
            report: The report name, such as summary or bios.

        Returns:
            The report rows.

        Raises:
            InvalidSeasonError: If season is not two consecutive years.
            InvalidLimitError: If limit is not a positive integer.
            InvalidStartError: If start is negative.
            InvalidCayenneValueError: If a cayenne string value contains a double quote.
        """

        sorting = TEAM_SORT_DEFAULT if sort is None else sort

        request = stats_report(
            language,
            'team',
            report,
            season,
            game_type,
            sorting,
            limit,
            start,
            aggregate,
            game,
            cayenne,
        )

        return self._get_model(request, ResultSet)


class AsyncStats(AsyncResource):
    """The asynchronous stats endpoints on the stats API.

    Every method may raise an NHLError subclass on a transport failure or an
    error response.
    """

    async def config(self, language: Language | str = Language.ENGLISH) -> Any:
        """It returns the configuration metadata.

        Args:
            language: The response language.

        Returns:
            The decoded configuration payload.
        """

        request = stats_config(language)
        return await self._get(request)

    async def franchises(self, language: Language | str = Language.ENGLISH) -> ResultSet:
        """It returns the franchises.

        Args:
            language: The response language.

        Returns:
            The franchises.
        """

        request = stats_franchises(language)
        return await self._get_model(request, ResultSet)

    async def glossary(self, language: Language | str = Language.ENGLISH) -> ResultSet:
        """It returns the statistic glossary.

        Args:
            language: The response language.

        Returns:
            The glossary entries.
        """

        request = stats_glossary(language)
        return await self._get_model(request, ResultSet)

    async def goalies(
        self,
        report: str = 'summary',
        *,
        season: int | None = None,
        game_type: GameType | int | None = None,
        sort: str | Sequence[dict[str, str]] | None = None,
        limit: int = REPORT_LIMIT_DEFAULT,
        start: int = 0,
        aggregate: bool = False,
        game: bool = False,
        cayenne: str | dict[str, Any] | None = None,
        language: Language | str = Language.ENGLISH,
    ) -> ResultSet:
        """It returns a goalie report.

        It sorts by wins descending by default. It accepts the same keyword arguments
        as report().

        Args:
            report: The report name, such as summary or bios.

        Returns:
            The report rows.

        Raises:
            InvalidSeasonError: If season is not two consecutive years.
            InvalidLimitError: If limit is not a positive integer.
            InvalidStartError: If start is negative.
            InvalidCayenneValueError: If a cayenne string value contains a double quote.
        """

        sorting = GOALIE_SORT_DEFAULT if sort is None else sort

        request = stats_report(
            language,
            'goalie',
            report,
            season,
            game_type,
            sorting,
            limit,
            start,
            aggregate,
            game,
            cayenne,
        )

        return await self._get_model(request, ResultSet)

    async def report(
        self,
        subject: str,
        report: str,
        *,
        season: int | None = None,
        game_type: GameType | int | None = None,
        sort: str | Sequence[dict[str, str]] | None = None,
        limit: int = REPORT_LIMIT_DEFAULT,
        start: int = 0,
        aggregate: bool = False,
        game: bool = False,
        cayenne: str | dict[str, Any] | None = None,
        language: Language | str = Language.ENGLISH,
    ) -> ResultSet:
        """It returns an arbitrary report for a subject.

        Args:
            subject: The report subject, such as skater, goalie, or team.
            report: The report name, such as summary or bios.
            season: An eight-digit season, YYYYYYYY, added to the query as seasonId.
            game_type: The game type, added to the query as gameTypeId.
            sort: A property name, a sequence of property and direction mappings, or None.
            limit: The page size.
            start: The page offset.
            aggregate: Aggregate rows across seasons.
            game: Return per-game rows.
            cayenne: A raw cayenne expression, or a mapping merged into the built expression.
            language: The response language.

        Returns:
            The report rows.

        Raises:
            InvalidSeasonError: If season is not two consecutive years.
            InvalidLimitError: If limit is not a positive integer.
            InvalidStartError: If start is negative.
            InvalidCayenneValueError: If a cayenne string value contains a double quote.
        """

        request = stats_report(
            language,
            subject,
            report,
            season,
            game_type,
            sort,
            limit,
            start,
            aggregate,
            game,
            cayenne,
        )

        return await self._get_model(request, ResultSet)

    async def seasons(self, language: Language | str = Language.ENGLISH) -> ResultSet:
        """It returns the seasons.

        Args:
            language: The response language.

        Returns:
            The seasons.
        """

        request = stats_seasons(language)
        return await self._get_model(request, ResultSet)

    async def skaters(
        self,
        report: str = 'summary',
        *,
        season: int | None = None,
        game_type: GameType | int | None = None,
        sort: str | Sequence[dict[str, str]] | None = None,
        limit: int = REPORT_LIMIT_DEFAULT,
        start: int = 0,
        aggregate: bool = False,
        game: bool = False,
        cayenne: str | dict[str, Any] | None = None,
        language: Language | str = Language.ENGLISH,
    ) -> ResultSet:
        """It returns a skater report.

        It sorts by points descending by default. It accepts the same keyword
        arguments as report().

        Args:
            report: The report name, such as summary or bios.

        Returns:
            The report rows.

        Raises:
            InvalidSeasonError: If season is not two consecutive years.
            InvalidLimitError: If limit is not a positive integer.
            InvalidStartError: If start is negative.
            InvalidCayenneValueError: If a cayenne string value contains a double quote.
        """

        sorting = SKATER_SORT_DEFAULT if sort is None else sort

        request = stats_report(
            language,
            'skater',
            report,
            season,
            game_type,
            sorting,
            limit,
            start,
            aggregate,
            game,
            cayenne,
        )

        return await self._get_model(request, ResultSet)

    async def teams(
        self,
        report: str = 'summary',
        *,
        season: int | None = None,
        game_type: GameType | int | None = None,
        sort: str | Sequence[dict[str, str]] | None = None,
        limit: int = REPORT_LIMIT_DEFAULT,
        start: int = 0,
        aggregate: bool = False,
        game: bool = False,
        cayenne: str | dict[str, Any] | None = None,
        language: Language | str = Language.ENGLISH,
    ) -> ResultSet:
        """It returns a team report.

        It sorts by points descending by default. It accepts the same keyword
        arguments as report().

        Args:
            report: The report name, such as summary or bios.

        Returns:
            The report rows.

        Raises:
            InvalidSeasonError: If season is not two consecutive years.
            InvalidLimitError: If limit is not a positive integer.
            InvalidStartError: If start is negative.
            InvalidCayenneValueError: If a cayenne string value contains a double quote.
        """

        sorting = TEAM_SORT_DEFAULT if sort is None else sort

        request = stats_report(
            language,
            'team',
            report,
            season,
            game_type,
            sorting,
            limit,
            start,
            aggregate,
            game,
            cayenne,
        )

        return await self._get_model(request, ResultSet)
