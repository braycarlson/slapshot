# slapshot

## Purpose

slapshot is a synchronous and asynchronous client for the unofficial NHL API. It covers the four public NHL services behind a single, typed interface: `api-web.nhle.com`, `api.nhle.com/stats/rest`, `records.nhl.com`, and the player search at `search.d3.nhle.com`.

## Why slapshot?

The NHL exposes a large, undocumented surface of endpoints spread across several hosts, each with its own path conventions, query parameters, and payload shapes. slapshot standardizes access to them so you can work with the data rather than with URL construction and response parsing.

Stable payloads decode into `msgspec` structs with `snake_case` attributes, while volatile payloads are returned as decoded JSON. Unknown fields are ignored during decoding, so new NHL fields never break existing code. Every URL template lives in an enum, so no path is ever built from a loose string.

## How It Works

slapshot is organized in four layers:

- **Client** (`NHL`, `AsyncNHL`): owns the `httpx` transport and exposes one attribute per resource.
- **Resources** (`client.standings`, `client.players`, ...): group related endpoints into methods.
- **Request builders** (`slapshot.resources.*`): validate arguments and produce a `Request` of URL and query parameters.
- **Endpoints** (`WebEndpoint`, `StatsEndpoint`, `RecordsEndpoint`, `SearchEndpoint`): hold every URL template as a `StrEnum`.

The synchronous `NHL` and asynchronous `AsyncNHL` clients expose the same resources and the same method names. The only difference is that `AsyncNHL` methods are awaitable.

## Core Features

- **Synchronous and Asynchronous**: an identical API on `NHL` and `AsyncNHL`, chosen per call site.
- **Typed Models**: stable payloads decode into `msgspec` structs; volatile payloads return raw JSON.
- **Forward Compatible**: unknown response fields are ignored, so new NHL fields do not break decoding.
- **No Loose Paths**: every endpoint is a `StrEnum` template, and identifiers, seasons, and dates are validated before a request is sent.
- **Bring Your Own Transport**: inject a preconfigured `httpx` client for proxies, retries, or custom headers.
- **Typed Errors**: a single `NHLError` hierarchy covers transport, HTTP status, decode, and parameter failures.

## Backing APIs

| Service | Base URL | Resources |
|---------|----------|-----------|
| Web | `https://api-web.nhle.com/v1` | `standings`, `schedule`, `games`, `players`, `teams`, `draft` |
| Stats | `https://api.nhle.com/stats/rest` | `stats` |
| Records | `https://records.nhl.com/site/api` | `records` |
| Search | `https://search.d3.nhle.com/api/v1` | `players.search` |

## Ready to Go?

Get started with slapshot:

- [Installation](setup/installation.md): How to install slapshot and its dependencies
- [Quickstart](setup/quickstart.md): A first synchronous and asynchronous request
- [Client](reference/client.md): Constructing `NHL` and `AsyncNHL`, timeouts, and custom transports
- [Resources](reference/resources.md): Every resource and method, with parameters and return types
- [Models](reference/models.md): The `msgspec` structs returned by typed endpoints
- [Enums](reference/enums.md): `Team`, `GameType`, `Language`, `Milestone`, and `SortDirection`
- [Errors](reference/errors.md): The exception hierarchy and when each error is raised
- [Raw Requests](reference/raw_requests.md): Dropping down to request builders and endpoints
