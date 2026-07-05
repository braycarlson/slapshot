from __future__ import annotations

from slapshot import NHL, WebEndpoint, request_build
from slapshot.resources.standings import standings_now


def main() -> None:
    with NHL() as client:
        url = WebEndpoint.PLAYER_LANDING.format(player=8478402)
        request = request_build(url)

        raw = client.get(request)
        print('Player name:', raw['firstName']['default'])

        request = standings_now()

        raw = client.get(request)
        print('Teams:', len(raw['standings']))


if __name__ == '__main__':
    main()
