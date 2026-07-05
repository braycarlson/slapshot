from __future__ import annotations

from slapshot import NHL


def main() -> None:
    with NHL() as client:
        rankings = client.draft.rankings()
        print('Ranking draft year:', rankings['draftYear'])

        current = client.draft.picks()
        print('Current draft picks:', len(current['picks']))

        year = client.draft.picks(2023, draft_round=1)
        print('2023 round 1 picks:', len(year['picks']))


if __name__ == '__main__':
    main()
