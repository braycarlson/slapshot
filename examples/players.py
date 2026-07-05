from __future__ import annotations

from slapshot import NHL, GameType


def main() -> None:
    with NHL() as client:
        landing = client.players.landing(8478402)
        print('Player:', landing.first_name.default, landing.last_name.default)
        print('Position:', landing.position, 'Number:', landing.sweater_number)

        results = client.players.search('mcdavid', limit=5)

        for row in results:
            print(row.player_id, row.name, row.position_code)

        log = client.players.game_log(8478402, season=20252026, game_type=GameType.REGULAR)
        print('Games logged:', len(log['gameLog']))

        skaters = client.players.skater_leaders(categories='points', limit=5)
        print('Skater leaders:', skaters)

        goalies = client.players.goalie_leaders(categories='wins', limit=5)
        print('Goalie leaders:', goalies)


if __name__ == '__main__':
    main()
