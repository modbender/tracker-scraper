---
title: Configuration
description: The full argument reference for scrape(), the shape of the returned stats, the UDP socket timeout, logging behaviour, and protocol limits.
sidebar:
  order: 4
---

Tracker Scraper is intentionally small — there's no config file and no options object. Everything you control is passed directly to `scrape()` (or as CLI arguments). This page is the reference for those inputs, the output shape, and the few runtime behaviours worth knowing about.

## Function signature

```python
scrape(tracker: str, hashes: list[str]) -> dict
```

### Arguments

| Argument | Type | Required | Description |
| --- | --- | --- | --- |
| `tracker` | `str` | yes | The tracker announce URL. The scheme (`udp`, `http`, `https`) selects the protocol. The URL is lower-cased before parsing. |
| `hashes` | `list[str]` | yes | Torrent `info_hash` values as 40-character hex strings. Each is converted to its 20-byte binary form internally. |

### Return value

A `dict` mapping each `info_hash` to a stats `dict`:

```python
{
    "<info_hash>": {
        "seeds": int,      # UDP   |  str: HTTP/HTTPS
        "peers": int,      # UDP   |  str: HTTP/HTTPS
        "complete": int,   # UDP   |  str: HTTP/HTTPS
    },
    ...
}
```

| Key | Description |
| --- | --- |
| `seeds` | Peers with a complete copy (the tracker's "complete" / seeders count). |
| `peers` | Peers still downloading (the tracker's "incomplete" / leechers count). |
| `complete` | Total number of completed downloads the tracker has recorded ("downloaded"). |

:::caution
The value **types differ by protocol**. The UDP path unpacks fixed-width integers, so its counts are Python `int`. The HTTP/HTTPS path returns the values as the tracker bencoded them, which are typically `str`. If you do arithmetic on the results, coerce with `int(value)` to be safe across both transports.
:::

## Timeouts

UDP scrapes use a socket timeout of **8 seconds** for both the connection handshake and the scrape response. If the tracker doesn't answer within that window, the underlying socket call raises `socket.timeout` (a subclass of `OSError`).

HTTP/HTTPS scrapes use `requests` with its default behaviour (no explicit timeout is set), so they rely on the server eventually responding or the connection failing.

## Protocol limits and requirements

| Constraint | Applies to | Behaviour |
| --- | --- | --- |
| Max 74 hashes per request | UDP | More than 74 raises `RuntimeError`. Split into chunks. |
| `announce` must be in the URL path | HTTP/HTTPS | The path's `announce` segment is rewritten to `scrape`; a URL without it raises `RuntimeError`. |
| Non-200 HTTP response | HTTP/HTTPS | Raises `RuntimeError` with the status code. |
| Unknown URL scheme | all | Anything other than `udp`/`http`/`https` raises `RuntimeError`. |

## Logging

The library logs each scrape at **WARNING** level through a standard `logging` logger named `tracker_scraper.scraper` (so it's silent unless your application configures logging). To see those messages:

```python
import logging

logging.basicConfig(level=logging.WARNING)
```

To silence them even when your app logs at WARNING globally, raise the threshold for just this logger:

```python
import logging

logging.getLogger("tracker_scraper.scraper").setLevel(logging.ERROR)
```

## CLI options

The command-line tool exposes the same two inputs plus output formatting:

| Argument / flag | Description |
| --- | --- |
| `tracker` | Announce URL (positional, first). |
| `hashes` | One or more `info_hash` values (positional, after the tracker). |
| `--indent N` | JSON indent width for the output. Default `2`. Use `--indent 0` for compact output. |

The CLI prints the results as JSON to stdout and exits `0`; on any error it prints the message to stderr and exits `1`.

## Next steps

- [Examples](/tracker-scraper/examples/basic/) — runnable recipes for each protocol and the CLI.
- [Usage](/tracker-scraper/usage/) — the narrative walkthrough of the API and CLI.
