from __future__ import annotations

import httpx

from slapshot import NHL


def main() -> None:
    transport = httpx.HTTPTransport(retries=3)

    http_client = httpx.Client(
        follow_redirects=True,
        timeout=10.0,
        transport=transport,
        headers={'User-Agent': 'my-app/1.0'},
    )

    client = NHL(client=http_client)

    standings = client.standings.now()
    print('Teams:', len(standings.standings))

    http_client.close()

    with NHL(timeout=5.0) as managed:
        player = managed.players.landing(8478402)
        print('Player:', player.first_name.default)


if __name__ == '__main__':
    main()
