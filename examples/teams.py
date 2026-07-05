from __future__ import annotations

from slapshot import NHL, GameType, Team


def main() -> None:
    with NHL() as client:
        roster = client.teams.roster(Team.EDMONTON)

        for player in roster.forwards:
            name = player.last_name.default if player.last_name else 'unknown'
            print(player.sweater_number, name, player.position_code)

        seasons = client.teams.roster_seasons(Team.EDMONTON)
        print('Roster seasons:', len(seasons))

        prospects = client.teams.prospects(Team.EDMONTON)
        print('Prospect groups:', list(prospects.keys()))

        stats = client.teams.club_stats(Team.EDMONTON, season=20252026, game_type=GameType.REGULAR)
        print('Club stats keys:', list(stats.keys()))


if __name__ == '__main__':
    main()
