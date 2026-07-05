from __future__ import annotations

import asyncio

from slapshot import AsyncNHL, GameType, Team


async def main() -> None:
    async with AsyncNHL() as client:
        schedule = await client.schedule.club_week(Team.EDMONTON)
        print('Timezone:', schedule['clubTimezone'])

        log = await client.players.game_log(8478402, season=20252026, game_type=GameType.REGULAR)
        print('Games logged:', len(log['gameLog']))

        results = await client.players.search('mcdavid', limit=3)
        print('Search hits:', [row.name for row in results])

        standings = await client.standings.now()
        print('Teams ranked:', len(standings.standings))


if __name__ == '__main__':
    asyncio.run(main())
