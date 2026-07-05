from __future__ import annotations

from slapshot.enums import Team


def test_team_abbreviations_are_unique() -> None:
    assert len({team.value for team in Team}) == len(Team)


def test_team_abbreviations_are_three_letter_uppercase() -> None:
    assert all(len(team.value) == 3 and team.value.isupper() for team in Team)
