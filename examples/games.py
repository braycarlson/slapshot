from __future__ import annotations

from slapshot import NHL


def main() -> None:
    with NHL() as client:
        scores = client.games.scores()
        games = scores['games']

        if not games:
            print('No games scheduled today')
            return

        game_id = games[0]['id']
        print('Game id:', game_id)

        landing = client.games.landing(game_id)
        print('Matchup:', landing['awayTeam']['abbrev'], 'at', landing['homeTeam']['abbrev'])

        boxscore = client.games.boxscore(game_id)
        print('State:', boxscore['gameState'])

        plays = client.games.play_by_play(game_id)
        print('Play count:', len(plays['plays']))


if __name__ == '__main__':
    main()
