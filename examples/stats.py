from __future__ import annotations

from slapshot import NHL, Language, SortDirection


def main() -> None:
    with NHL() as client:
        skaters = client.stats.skaters(season=20252026, limit=5)

        print('Top scorers:')

        for row in skaters.data:
            print(' ', row['skaterFullName'], row.get('points'))

        goalies = client.stats.goalies(season=20252026, limit=5)
        print('Goalie rows:', goalies.total)

        teams = client.stats.teams(season=20252026, limit=5)
        print('Team rows:', teams.total)

        custom = client.stats.report(
            'skater',
            'summary',
            season=20252026,
            sort=({'property': 'goals', 'direction': SortDirection.DESCENDING},),
            limit=3,
        )

        print('Top goal scorers:', [row['skaterFullName'] for row in custom.data])

        config = client.stats.config(Language.ENGLISH)
        print('Config keys:', list(config.keys()))


if __name__ == '__main__':
    main()
