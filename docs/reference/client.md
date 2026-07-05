# Client

## Overview

slapshot exposes two clients: `NHL` (synchronous) and `AsyncNHL` (asynchronous). Both own an `httpx` client, validate the timeout, and attach one attribute per resource. They share the same resources and method names; only the call convention differs.

```python
from slapshot import NHL, AsyncNHL
```

## Constructing a Client

Both clients take the same keyword-only arguments:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `timeout` | `float` | `30.0` | Request timeout in seconds. Must be greater than zero. |
| `client` | `httpx.Client` / `httpx.AsyncClient` / `None` | `None` | A preconfigured transport. When `None`, slapshot creates one. |

```python
from slapshot import NHL, AsyncNHL

client = NHL(timeout=10.0)
async_client = AsyncNHL(timeout=10.0)
```

A `timeout` of zero or less raises `InvalidParameterError`. When slapshot creates the transport itself, it sets `follow_redirects=True` and a `User-Agent` of `slapshot/<version>`.

## Lifecycle

Use a client as a context manager so its transport is closed on exit:

```python
with NHL() as client:
    standings = client.standings.now()
```

```python
async with AsyncNHL() as client:
    standings = await client.standings.now()
```

You may also close a client explicitly:

```python
client = NHL()

try:
    standings = client.standings.now()
finally:
    client.close()
```

!!! note
    When you pass your own `client`, slapshot uses it as-is and does not close it; you own its lifecycle. When slapshot creates the transport, it closes it for you on exit.

## Resources

Each client attaches the same eight resources:

| Attribute | Type (sync / async) | Backing API |
|-----------|---------------------|-------------|
| `client.standings` | `Standings` / `AsyncStandings` | Web |
| `client.schedule` | `Schedule` / `AsyncSchedule` | Web |
| `client.games` | `Games` / `AsyncGames` | Web |
| `client.players` | `Players` / `AsyncPlayers` | Web, Search |
| `client.teams` | `Teams` / `AsyncTeams` | Web |
| `client.draft` | `Draft` / `AsyncDraft` | Web |
| `client.stats` | `Stats` / `AsyncStats` | Stats |
| `client.records` | `Records` / `AsyncRecords` | Records |

See [Resources](resources.md) for every method.

## Requests

Both clients expose two low-level methods that resources use internally, and that you can call directly with a hand-built `Request`:

| Method | Returns | Description |
|--------|---------|-------------|
| `get(request)` | `dict` / `list` | Sends the request and returns decoded JSON. |
| `get_model(request, model)` | `model` | Sends the request and decodes the body into `model`. |

See [Raw Requests](raw_requests.md) for building a `Request` by hand.

## Custom Transport

Pass a preconfigured `httpx` client to control headers, proxies, retries, or connection limits. slapshot uses it as-is and leaves closing it to you:

```python
import httpx

from slapshot import NHL


def main() -> None:
    transport = httpx.HTTPTransport(retries=3)

    http_client = httpx.Client(
        follow_redirects=True,
        timeout=10.0,
        transport=transport,
        headers={'User-Agent': 'my-app/1.0'}
    )

    client = NHL(client=http_client)

    standings = client.standings.now()
    print('Teams:', len(standings.standings))

    http_client.close()
```

For `AsyncNHL`, pass an `httpx.AsyncClient` the same way.

## Errors

Every method can raise a subclass of `NHLError`: transport failures, HTTP status errors, decode errors, and parameter validation errors. See [Errors](errors.md) for the full hierarchy and handling patterns.
