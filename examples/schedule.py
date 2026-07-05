from __future__ import annotations

from slapshot import NHL, Team


def main() -> None:
    with NHL() as client:
        week = client.schedule.club_week(Team.EDMONTON)
        print('Games this week:', len(week['games']))

        month = client.schedule.club_month(Team.EDMONTON, month='2025-11')
        print('Games in November:', len(month['games']))

        season = client.schedule.club_season(Team.EDMONTON, 20252026)
        print('Games this season:', len(season['games']))

        day = client.schedule.by_date('2025-11-01')
        print('League games on 2025-11-01:', day['numberOfGames'])


if __name__ == '__main__':
    main()
