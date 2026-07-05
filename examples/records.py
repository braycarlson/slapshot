from __future__ import annotations

from slapshot import NHL, GameType, Milestone


def main() -> None:
    with NHL() as client:
        milestone = client.records.milestone(Milestone.GOAL_CAREER_500)
        print('500-goal scorers:', milestone.total)

        franchises = client.records.franchises()
        print('Franchises:', franchises.total)

        draft = client.records.draft(year=2015)
        print('2015 draft records:', draft.total)

        series = client.records.playoff_series(season=20222023)
        print('2022-2023 playoff series:', series.total)

        versus = client.records.all_time_record(franchise=1, game_type=GameType.REGULAR)
        print('All-time record rows:', versus.total)

        trophies = client.records.trophies()
        print('Trophies:', trophies.total)


if __name__ == '__main__':
    main()
