# Installation

## Prerequisites

- Python 3.11 or newer
- [uv](https://github.com/astral-sh/uv) (recommended) or `pip`

## Dependencies

slapshot depends on three packages, installed automatically:

| Package | Purpose |
|---------|---------|
| [`httpx`](https://www.python-httpx.org/) | Synchronous and asynchronous HTTP transport |
| [`msgspec`](https://jcristharif.com/msgspec/) | Fast decoding of stable payloads into typed structs |
| [`typing-extensions`](https://pypi.org/project/typing-extensions/) | Backports of newer typing features |

## From PyPI

Add slapshot to your project with uv:

```
uv add slapshot
```

Or install it with `pip`:

```
pip install slapshot
```

## From Source

Clone the repository and sync the environment with uv:

```
git clone https://github.com/braycarlson/slapshot
cd slapshot
uv sync
```

`uv sync` creates a virtual environment in `.venv` and installs slapshot together with its runtime and development dependencies from the locked `uv.lock`.

## Verifying the Installation

Confirm the import and check the version:

```python
import slapshot

print(slapshot.__version__)
```

Then make a live request against the API:

```python
from slapshot import NHL

with NHL() as client:
    standings = client.standings.now()
    print(standings.standings[0].team_name.default)
```

## Development

The development dependencies are declared in the `dev` dependency group and installed by `uv sync`. The project is checked with three tools:

| Command | Purpose |
|---------|---------|
| `uv run ruff check` | Lint |
| `uv run ty check` | Type check |
| `uv run python -m pytest` | Run the test suite |

By default the test suite deselects tests marked `network`, which hit the live NHL API over the network. Run them explicitly with:

```
uv run python -m pytest -m network
```
