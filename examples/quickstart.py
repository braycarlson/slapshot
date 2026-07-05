from __future__ import annotations

from slapshot import NHL, GameType, Milestone, Team


def main() -> None:
    with NHL() as client:
        standings = client.standings.now()

        leader = standings.standings[0]
        print('Top team:', leader.team_name.default, leader.points)

        player = client.players.landing(8478402)
        print('Player:', player.first_name.default, player.last_name.default, player.position)

        skaters = client.stats.skaters(season=20252026, limit=5)
        print('Top scorers:', [row['skaterFullName'] for row in skaters.data])

        roster = client.teams.roster(Team.EDMONTON)
        print('Roster:', len(roster.forwards), len(roster.defensemen), len(roster.goalies))

        milestone = client.records.milestone(Milestone.GOAL_CAREER_500)
        print('500-goal scorers:', milestone.total)

        log = client.players.game_log(8478402, season=20252026, game_type=GameType.REGULAR)
        print('Games logged:', len(log['gameLog']))


if __name__ == '__main__':
    main()
