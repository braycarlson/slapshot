from __future__ import annotations

import msgspec
import pytest

from slapshot.models import (
    LocalizedName,
    PlayerLanding,
    PlayerSearchResult,
    ResultSet,
    Roster,
    RosterPlayer,
    StandingsResponse,
    StandingsTeam,
)


REQUIRED_FIELD_MODELS = [PlayerLanding, ResultSet, Roster, StandingsResponse]


def test_localized_name() -> None:
    value = msgspec.json.decode(b'{"default":"Edmonton","fr":"Edmonton"}', type=LocalizedName)
    assert value.default == 'Edmonton'
    assert value.fr == 'Edmonton'


def test_localized_name_optional_languages_default_none() -> None:
    value = msgspec.json.decode(b'{"default":"x"}', type=LocalizedName)
    assert value.cs is None
    assert value.sv is None


def test_result_set() -> None:
    value = msgspec.json.decode(b'{"data":[{"a":1}],"total":1}', type=ResultSet)
    assert value.total == 1
    assert value.data == [{'a': 1}]


def test_standings_response() -> None:
    payload = (
        b'{"standings":[{"teamAbbrev":{"default":"EDM"},'
        b'"teamName":{"default":"OIL"},"points":100}]}'
    )
    value = msgspec.json.decode(payload, type=StandingsResponse)
    assert value.standings[0].points == 100


def test_standings_team_optionals_default_none() -> None:
    payload = b'{"teamAbbrev":{"default":"EDM"},"teamName":{"default":"Oilers"}}'
    value = msgspec.json.decode(payload, type=StandingsTeam)
    assert value.points is None
    assert value.wins is None
    assert value.team_abbrev.default == 'EDM'


def test_roster() -> None:
    value = msgspec.json.decode(
        b'{"forwards":[{"id":1}],"defensemen":[],"goalies":[]}', type=Roster
    )
    assert value.forwards[0].id == 1


def test_roster_player_optionals_default_none() -> None:
    value = msgspec.json.decode(b'{"id":1}', type=RosterPlayer)
    assert value.id == 1
    assert value.sweater_number is None


def test_roster_player_camel_rename_on_decode() -> None:
    value = msgspec.json.decode(b'{"id":1,"heightInCentimeters":185}', type=RosterPlayer)
    assert value.height_in_centimeters == 185


def test_roster_player_camel_rename_on_encode() -> None:
    encoded = msgspec.json.encode(RosterPlayer(id=1))
    assert b'"positionCode"' in encoded
    assert b'"position_code"' not in encoded


def test_player_landing() -> None:
    payload = (
        b'{"playerId":1,"isActive":true,"firstName":{"default":"A"},"lastName":{"default":"B"}}'
    )
    value = msgspec.json.decode(payload, type=PlayerLanding)
    assert value.player_id == 1


def test_player_landing_in_hhof_custom_rename() -> None:
    payload = (
        b'{"playerId":1,"isActive":true,'
        b'"firstName":{"default":"A"},"lastName":{"default":"B"},"inHHOF":1}'
    )
    value = msgspec.json.decode(payload, type=PlayerLanding)
    assert value.in_hhof == 1


def test_player_search_result() -> None:
    value = msgspec.json.decode(
        b'{"playerId":"8478402","name":"Connor McDavid"}', type=PlayerSearchResult
    )
    assert value.name == 'Connor McDavid'


def test_player_search_result_accepts_int_last_season() -> None:
    value = msgspec.json.decode(
        b'{"playerId":"1","name":"x","lastSeasonId":20242025}', type=PlayerSearchResult
    )
    assert value.last_season_id == 20242025


def test_player_search_result_accepts_string_last_season() -> None:
    value = msgspec.json.decode(
        b'{"playerId":"1","name":"x","lastSeasonId":"20242025"}', type=PlayerSearchResult
    )
    assert value.last_season_id == '20242025'


def test_ignores_unknown_fields() -> None:
    value = msgspec.json.decode(b'{"default":"x","unknownField":1}', type=LocalizedName)
    assert value.default == 'x'


def test_standings_team_ignores_unknown_fields() -> None:
    payload = (
        b'{"teamAbbrev":{"default":"EDM"},"teamName":{"default":"Oilers"},"somethingBrandNew":42}'
    )
    value = msgspec.json.decode(payload, type=StandingsTeam)
    assert value.team_name.default == 'Oilers'


@pytest.mark.parametrize('model', REQUIRED_FIELD_MODELS)
def test_required_fields_reject_empty_object(model: type) -> None:
    with pytest.raises(msgspec.ValidationError):
        msgspec.json.decode(b'{}', type=model)
