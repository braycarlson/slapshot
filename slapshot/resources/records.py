from __future__ import annotations

from typing_extensions import TYPE_CHECKING

from slapshot.endpoints import RecordsEndpoint
from slapshot.models import ResultSet
from slapshot.request import Request, cayenne_build, request_build
from slapshot.resource import AsyncResource, SyncResource
from slapshot.validation import identifier_validate, season_validate

if TYPE_CHECKING:
    from slapshot.enums import GameType, Milestone, SortDirection


def records_franchise_report(
    endpoint: RecordsEndpoint,
    franchise: int | None,
    team: int | None,
    season: int | None,
    sort: str | None,
    order: SortDirection | str | None,
) -> Request:
    if franchise is not None:
        identifier_validate(franchise, name='franchise')

    if team is not None:
        identifier_validate(team, name='team')

    if season is not None:
        season_validate(season)

    return request_build(
        endpoint,
        {
            'cayenneExp': cayenne_build(
                {'franchiseId': franchise, 'mostRecentTeamId': team, 'seasonId': season}
            ),
            'sort': sort,
            'dir': order.upper() if order is not None else None,
        },
    )


def records_versus_franchise(
    endpoint: RecordsEndpoint, franchise: int | None, game_type: GameType | int | None
) -> Request:
    if franchise is not None:
        identifier_validate(franchise, name='franchise')

    return request_build(
        endpoint,
        {'cayenneExp': cayenne_build({'teamFranchiseId': franchise, 'gameTypeId': game_type})},
    )


def records_attendance() -> Request:
    return request_build(RecordsEndpoint.ATTENDANCE)


def records_draft(team: int | None, year: int | None) -> Request:
    if team is not None:
        identifier_validate(team, name='team')

    if year is not None:
        identifier_validate(year, name='year')

    return request_build(
        RecordsEndpoint.DRAFT,
        {'cayenneExp': cayenne_build({'draftedByTeamId': team, 'draftYear': year})},
    )


def records_milestone(name: Milestone) -> Request:
    url = RecordsEndpoint.MILESTONE.format(name=name)
    return request_build(url)


def records_officials(active: bool | None) -> Request:
    return request_build(
        RecordsEndpoint.OFFICIALS, {'cayenneExp': cayenne_build({'active': active})}
    )


def records_players(team: int | None) -> Request:
    if team is None:
        return request_build(RecordsEndpoint.PLAYERS)

    identifier_validate(team, name='team')

    url = RecordsEndpoint.PLAYERS_BY_TEAM.format(team=team)
    return request_build(url)


def records_playoff_series(series: str | None, season: int | None) -> Request:
    if season is not None:
        season_validate(season)

    return request_build(
        RecordsEndpoint.PLAYOFF_SERIES,
        {'cayenneExp': cayenne_build({'seriesTitle': series, 'seasonId': season})},
    )


def records_trophies() -> Request:
    return request_build(RecordsEndpoint.TROPHIES)


class Records(SyncResource):
    """The records endpoints on the records API.

    Every method may raise an NHLError subclass on a transport failure or an
    error response.
    """

    def all_time_record(
        self, franchise: int | None = None, game_type: GameType | int | None = None
    ) -> ResultSet:
        """It returns the all-time record versus a franchise.

        Args:
            franchise: A franchise identifier filter.
            game_type: A game type filter.

        Returns:
            The report rows.

        Raises:
            InvalidIdentifierError: If franchise is not a positive integer.
        """

        request = records_versus_franchise(RecordsEndpoint.ALL_TIME_RECORD, franchise, game_type)
        return self._get_model(request, ResultSet)

    def attendance(self) -> ResultSet:
        """It returns the attendance records."""

        request = records_attendance()
        return self._get_model(request, ResultSet)

    def draft(self, *, team: int | None = None, year: int | None = None) -> ResultSet:
        """It returns the draft records.

        Args:
            team: A drafting-team identifier filter.
            year: A draft-year filter.

        Returns:
            The report rows.

        Raises:
            InvalidIdentifierError: If team or year is not a positive integer.
        """

        request = records_draft(team, year)
        return self._get_model(request, ResultSet)

    def franchise_details(
        self,
        *,
        franchise: int | None = None,
        team: int | None = None,
        season: int | None = None,
        sort: str | None = None,
        order: SortDirection | str | None = None,
    ) -> ResultSet:
        """It returns the franchise details.

        It accepts the same keyword arguments as franchises().

        Returns:
            The report rows.

        Raises:
            InvalidIdentifierError: If franchise or team is not a positive integer.
            InvalidSeasonError: If season is not two consecutive years.
        """

        request = records_franchise_report(
            RecordsEndpoint.FRANCHISE_DETAILS, franchise, team, season, sort, order
        )
        return self._get_model(request, ResultSet)

    def franchise_goalie_records(
        self,
        *,
        franchise: int | None = None,
        team: int | None = None,
        season: int | None = None,
        sort: str | None = None,
        order: SortDirection | str | None = None,
    ) -> ResultSet:
        """It returns the franchise goalie records.

        It accepts the same keyword arguments as franchises().

        Returns:
            The report rows.

        Raises:
            InvalidIdentifierError: If franchise or team is not a positive integer.
            InvalidSeasonError: If season is not two consecutive years.
        """

        request = records_franchise_report(
            RecordsEndpoint.FRANCHISE_GOALIE_RECORDS, franchise, team, season, sort, order
        )
        return self._get_model(request, ResultSet)

    def franchise_season_records(
        self,
        *,
        franchise: int | None = None,
        team: int | None = None,
        season: int | None = None,
        sort: str | None = None,
        order: SortDirection | str | None = None,
    ) -> ResultSet:
        """It returns the single-season franchise records.

        It accepts the same keyword arguments as franchises().

        Returns:
            The report rows.

        Raises:
            InvalidIdentifierError: If franchise or team is not a positive integer.
            InvalidSeasonError: If season is not two consecutive years.
        """

        request = records_franchise_report(
            RecordsEndpoint.FRANCHISE_SEASON_RECORDS, franchise, team, season, sort, order
        )

        return self._get_model(request, ResultSet)

    def franchise_season_results(
        self,
        *,
        franchise: int | None = None,
        team: int | None = None,
        season: int | None = None,
        sort: str | None = None,
        order: SortDirection | str | None = None,
    ) -> ResultSet:
        """It returns the season-by-season franchise results.

        It accepts the same keyword arguments as franchises().

        Returns:
            The report rows.

        Raises:
            InvalidIdentifierError: If franchise or team is not a positive integer.
            InvalidSeasonError: If season is not two consecutive years.
        """

        request = records_franchise_report(
            RecordsEndpoint.FRANCHISE_SEASON_RESULTS, franchise, team, season, sort, order
        )

        return self._get_model(request, ResultSet)

    def franchise_skater_records(
        self,
        *,
        franchise: int | None = None,
        team: int | None = None,
        season: int | None = None,
        sort: str | None = None,
        order: SortDirection | str | None = None,
    ) -> ResultSet:
        """It returns the franchise skater records.

        It accepts the same keyword arguments as franchises().

        Returns:
            The report rows.

        Raises:
            InvalidIdentifierError: If franchise or team is not a positive integer.
            InvalidSeasonError: If season is not two consecutive years.
        """

        request = records_franchise_report(
            RecordsEndpoint.FRANCHISE_SKATER_RECORDS, franchise, team, season, sort, order
        )

        return self._get_model(request, ResultSet)

    def franchise_team_totals(
        self,
        *,
        franchise: int | None = None,
        team: int | None = None,
        season: int | None = None,
        sort: str | None = None,
        order: SortDirection | str | None = None,
    ) -> ResultSet:
        """It returns the all-time franchise team totals.

        It accepts the same keyword arguments as franchises().

        Returns:
            The report rows.

        Raises:
            InvalidIdentifierError: If franchise or team is not a positive integer.
            InvalidSeasonError: If season is not two consecutive years.
        """

        request = records_franchise_report(
            RecordsEndpoint.FRANCHISE_TEAM_TOTALS, franchise, team, season, sort, order
        )

        return self._get_model(request, ResultSet)

    def franchises(
        self,
        *,
        franchise: int | None = None,
        team: int | None = None,
        season: int | None = None,
        sort: str | None = None,
        order: SortDirection | str | None = None,
    ) -> ResultSet:
        """It returns the franchise index.

        Args:
            franchise: A franchise identifier filter (franchiseId).
            team: A most-recent-team identifier filter (mostRecentTeamId).
            season: An eight-digit season filter, YYYYYYYY (seasonId).
            sort: A sort property, or None.
            order: A sort direction, ASC or DESC, or None.

        Returns:
            The report rows.

        Raises:
            InvalidIdentifierError: If franchise or team is not a positive integer.
            InvalidSeasonError: If season is not two consecutive years.
        """

        request = records_franchise_report(
            RecordsEndpoint.FRANCHISES, franchise, team, season, sort, order
        )

        return self._get_model(request, ResultSet)

    def milestone(self, name: Milestone) -> ResultSet:
        """It returns a milestone list.

        Args:
            name: The milestone to return.

        Returns:
            The report rows.
        """

        request = records_milestone(name)
        return self._get_model(request, ResultSet)

    def officials(self, active: bool | None = None) -> ResultSet:
        """It returns the officials, optionally filtered by active status.

        Args:
            active: Restrict to active officials, inactive officials, or all
                when None.

        Returns:
            The report rows.
        """

        request = records_officials(active)
        return self._get_model(request, ResultSet)

    def players(self, team: int | None = None) -> ResultSet:
        """It returns the players, optionally filtered by team.

        Args:
            team: A team identifier filter, or None for all players.

        Returns:
            The report rows.

        Raises:
            InvalidIdentifierError: If team is not a positive integer.
        """

        request = records_players(team)
        return self._get_model(request, ResultSet)

    def playoff_series(self, *, series: str | None = None, season: int | None = None) -> ResultSet:
        """It returns the playoff series.

        Args:
            series: A series-title filter.
            season: An eight-digit season filter, YYYYYYYY.

        Returns:
            The report rows.

        Raises:
            InvalidSeasonError: If season is not two consecutive years.
        """

        request = records_playoff_series(series, season)
        return self._get_model(request, ResultSet)

    def trophies(self) -> ResultSet:
        """It returns the trophies."""

        request = records_trophies()
        return self._get_model(request, ResultSet)


class AsyncRecords(AsyncResource):
    """The asynchronous records endpoints on the records API.

    Every method may raise an NHLError subclass on a transport failure or an
    error response.
    """

    async def all_time_record(
        self, franchise: int | None = None, game_type: GameType | int | None = None
    ) -> ResultSet:
        """It returns the all-time record versus a franchise.

        Args:
            franchise: A franchise identifier filter.
            game_type: A game type filter.

        Returns:
            The report rows.

        Raises:
            InvalidIdentifierError: If franchise is not a positive integer.
        """

        request = records_versus_franchise(RecordsEndpoint.ALL_TIME_RECORD, franchise, game_type)
        return await self._get_model(request, ResultSet)

    async def attendance(self) -> ResultSet:
        """It returns the attendance records."""

        request = records_attendance()
        return await self._get_model(request, ResultSet)

    async def draft(self, *, team: int | None = None, year: int | None = None) -> ResultSet:
        """It returns the draft records.

        Args:
            team: A drafting-team identifier filter.
            year: A draft-year filter.

        Returns:
            The report rows.

        Raises:
            InvalidIdentifierError: If team or year is not a positive integer.
        """

        request = records_draft(team, year)
        return await self._get_model(request, ResultSet)

    async def franchise_details(
        self,
        *,
        franchise: int | None = None,
        team: int | None = None,
        season: int | None = None,
        sort: str | None = None,
        order: SortDirection | str | None = None,
    ) -> ResultSet:
        """It returns the franchise details.

        It accepts the same keyword arguments as franchises().

        Returns:
            The report rows.

        Raises:
            InvalidIdentifierError: If franchise or team is not a positive integer.
            InvalidSeasonError: If season is not two consecutive years.
        """

        request = records_franchise_report(
            RecordsEndpoint.FRANCHISE_DETAILS, franchise, team, season, sort, order
        )

        return await self._get_model(request, ResultSet)

    async def franchise_goalie_records(
        self,
        *,
        franchise: int | None = None,
        team: int | None = None,
        season: int | None = None,
        sort: str | None = None,
        order: SortDirection | str | None = None,
    ) -> ResultSet:
        """It returns the franchise goalie records.

        It accepts the same keyword arguments as franchises().

        Returns:
            The report rows.

        Raises:
            InvalidIdentifierError: If franchise or team is not a positive integer.
            InvalidSeasonError: If season is not two consecutive years.
        """

        request = records_franchise_report(
            RecordsEndpoint.FRANCHISE_GOALIE_RECORDS, franchise, team, season, sort, order
        )

        return await self._get_model(request, ResultSet)

    async def franchise_season_records(
        self,
        *,
        franchise: int | None = None,
        team: int | None = None,
        season: int | None = None,
        sort: str | None = None,
        order: SortDirection | str | None = None,
    ) -> ResultSet:
        """It returns the single-season franchise records.

        It accepts the same keyword arguments as franchises().

        Returns:
            The report rows.

        Raises:
            InvalidIdentifierError: If franchise or team is not a positive integer.
            InvalidSeasonError: If season is not two consecutive years.
        """

        request = records_franchise_report(
            RecordsEndpoint.FRANCHISE_SEASON_RECORDS, franchise, team, season, sort, order
        )

        return await self._get_model(request, ResultSet)

    async def franchise_season_results(
        self,
        *,
        franchise: int | None = None,
        team: int | None = None,
        season: int | None = None,
        sort: str | None = None,
        order: SortDirection | str | None = None,
    ) -> ResultSet:
        """It returns the season-by-season franchise results.

        It accepts the same keyword arguments as franchises().

        Returns:
            The report rows.

        Raises:
            InvalidIdentifierError: If franchise or team is not a positive integer.
            InvalidSeasonError: If season is not two consecutive years.
        """

        request = records_franchise_report(
            RecordsEndpoint.FRANCHISE_SEASON_RESULTS, franchise, team, season, sort, order
        )

        return await self._get_model(request, ResultSet)

    async def franchise_skater_records(
        self,
        *,
        franchise: int | None = None,
        team: int | None = None,
        season: int | None = None,
        sort: str | None = None,
        order: SortDirection | str | None = None,
    ) -> ResultSet:
        """It returns the franchise skater records.

        It accepts the same keyword arguments as franchises().

        Returns:
            The report rows.

        Raises:
            InvalidIdentifierError: If franchise or team is not a positive integer.
            InvalidSeasonError: If season is not two consecutive years.
        """

        request = records_franchise_report(
            RecordsEndpoint.FRANCHISE_SKATER_RECORDS, franchise, team, season, sort, order
        )

        return await self._get_model(request, ResultSet)

    async def franchise_team_totals(
        self,
        *,
        franchise: int | None = None,
        team: int | None = None,
        season: int | None = None,
        sort: str | None = None,
        order: SortDirection | str | None = None,
    ) -> ResultSet:
        """It returns the all-time franchise team totals.

        It accepts the same keyword arguments as franchises().

        Returns:
            The report rows.

        Raises:
            InvalidIdentifierError: If franchise or team is not a positive integer.
            InvalidSeasonError: If season is not two consecutive years.
        """

        request = records_franchise_report(
            RecordsEndpoint.FRANCHISE_TEAM_TOTALS, franchise, team, season, sort, order
        )

        return await self._get_model(request, ResultSet)

    async def franchises(
        self,
        *,
        franchise: int | None = None,
        team: int | None = None,
        season: int | None = None,
        sort: str | None = None,
        order: SortDirection | str | None = None,
    ) -> ResultSet:
        """It returns the franchise index.

        Args:
            franchise: A franchise identifier filter (franchiseId).
            team: A most-recent-team identifier filter (mostRecentTeamId).
            season: An eight-digit season filter, YYYYYYYY (seasonId).
            sort: A sort property, or None.
            order: A sort direction, ASC or DESC, or None.

        Returns:
            The report rows.

        Raises:
            InvalidIdentifierError: If franchise or team is not a positive integer.
            InvalidSeasonError: If season is not two consecutive years.
        """

        request = records_franchise_report(
            RecordsEndpoint.FRANCHISES, franchise, team, season, sort, order
        )

        return await self._get_model(request, ResultSet)

    async def milestone(self, name: Milestone) -> ResultSet:
        """It returns a milestone list.

        Args:
            name: The milestone to return.

        Returns:
            The report rows.
        """

        request = records_milestone(name)
        return await self._get_model(request, ResultSet)

    async def officials(self, active: bool | None = None) -> ResultSet:
        """It returns the officials, optionally filtered by active status.

        Args:
            active: Restrict to active officials, inactive officials, or all
                when None.

        Returns:
            The report rows.
        """

        request = records_officials(active)
        return await self._get_model(request, ResultSet)

    async def players(self, team: int | None = None) -> ResultSet:
        """It returns the players, optionally filtered by team.

        Args:
            team: A team identifier filter, or None for all players.

        Returns:
            The report rows.

        Raises:
            InvalidIdentifierError: If team is not a positive integer.
        """

        request = records_players(team)
        return await self._get_model(request, ResultSet)

    async def playoff_series(
        self, *, series: str | None = None, season: int | None = None
    ) -> ResultSet:
        """It returns the playoff series.

        Args:
            series: A series-title filter.
            season: An eight-digit season filter, YYYYYYYY.

        Returns:
            The report rows.

        Raises:
            InvalidSeasonError: If season is not two consecutive years.
        """

        request = records_playoff_series(series, season)
        return await self._get_model(request, ResultSet)

    async def trophies(self) -> ResultSet:
        """It returns the trophies."""

        request = records_trophies()
        return await self._get_model(request, ResultSet)
