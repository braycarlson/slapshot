from __future__ import annotations

from slapshot import NHL


def main() -> None:
    with NHL() as client:
        standings = client.standings.now()

        for team in standings.standings[:5]:
            print(team.team_name.default, team.points, team.wins, team.losses)

        historical = client.standings.by_date('2024-01-01')
        print('Teams on 2024-01-01:', len(historical.standings))

        seasons = client.standings.seasons()
        print('Available standings seasons:', len(seasons))


if __name__ == '__main__':
    main()
