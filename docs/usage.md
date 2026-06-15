---
title: Usage
description: Use the scrape() function from Python and the tracker-scraper command-line tool — arguments, the returned stats dictionary, and how UDP vs HTTP trackers are handled.
sidebar:
  order: 3
---

There are two ways to use Tracker Scraper: the `scrape()` function in your own Python code, and the `tracker-scraper` command-line tool. Both do the same thing — contact a tracker and return per-torrent stats.

## The Python API

The package exposes a single public function:

```python
from tracker_scraper import scrape

results = scrape(tracker, hashes)
```

| Argument | Type | Description |
| --- | --- | --- |
| `tracker` | `str` | The tracker's **announce URL**, taken straight from a torrent's metadata. Scheme must be `udp`, `http`, or `https`. |
| `hashes` | `list[str]` | One or more torrent `info_hash` values as 40-character hex strings. |

It returns a `dict` keyed by `info_hash`, where each value is a `dict` with three counts:

| Key | Meaning |
| --- | --- |
| `seeds` | Number of complete copies currently seeding. |
| `peers` | Number of incomplete peers (leechers) currently downloading. |
| `complete` | Number of times the torrent has been downloaded to completion. |

```python
from tracker_scraper import scrape

results = scrape(
    tracker="udp://exodus.desync.com:6969",
    hashes=["2d88e693eda7edf3c1fd0c48e8b99b8fd5a820b2"],
)

for info_hash, stats in results.items():
    print(info_hash, stats["seeds"], stats["peers"], stats["complete"])
```

:::tip
The keys in the returned dictionary are exactly the hash strings you passed in (for the HTTP path they are re-derived from the response and lower-cased). Pass hashes in a consistent case if you plan to look results up by key.
:::

## UDP vs HTTP/HTTPS trackers

The scheme of the announce URL decides the protocol — you don't choose it explicitly:

- **`udp://…`** → the binary UDP tracker protocol. Fast and the most common form for modern trackers.
- **`http://…`** or **`https://…`** → the bencoded HTTP scrape endpoint. The URL's `announce` path segment is automatically rewritten to `scrape`, as the convention requires.

```python
# UDP
scrape("udp://tracker.opentrackr.org:1337/announce", hashes)

# HTTP — the /announce path is rewritten to /scrape for you
scrape("http://tracker.example.org/announce", hashes)
```

:::caution
HTTP/HTTPS scraping only works when the announce URL contains `announce` in its path — that's how the scrape endpoint is located (`announce` → `scrape`). A tracker whose announce URL has no `announce` segment, or that doesn't expose a scrape endpoint, raises a `RuntimeError`. This is a tracker limitation, not a bug.
:::

## Batch scraping multiple torrents

Pass several hashes to query them all in one round trip:

```python
results = scrape(
    tracker="udp://exodus.desync.com:6969",
    hashes=[
        "2d88e693eda7edf3c1fd0c48e8b99b8fd5a820b2",
        "8929b29b83736ae650ee8152789559355275bd5c",
    ],
)
```

:::caution
The UDP protocol limits a single scrape request to **74 hashes**. Asking for more on a `udp://` tracker raises a `RuntimeError` — split larger batches into chunks of 74 or fewer. HTTP/HTTPS trackers have no fixed library limit, but individual trackers may impose their own.
:::

## The command-line tool

Installing the package also installs a `tracker-scraper` command. It takes the tracker as the first argument and one or more hashes after it, and prints the results as JSON:

```bash
tracker-scraper udp://exodus.desync.com:6969 \
  2d88e693eda7edf3c1fd0c48e8b99b8fd5a820b2 \
  8929b29b83736ae650ee8152789559355275bd5c
```

```json
{
  "2d88e693eda7edf3c1fd0c48e8b99b8fd5a820b2": {
    "seeds": 34,
    "peers": 189,
    "complete": 10
  },
  "8929b29b83736ae650ee8152789559355275bd5c": {
    "seeds": 12,
    "peers": 0,
    "complete": 290
  }
}
```

| Flag / argument | Description |
| --- | --- |
| `tracker` | Announce URL of the tracker (`udp://`, `http://`, or `https://`). |
| `hashes` | One or more 40-character hex `info_hash` values. |
| `--indent N` | JSON indentation for the printed output (default `2`). |
| `-h`, `--help` | Show the usage summary. |

The command exits with status `0` on success and `1` if the scrape fails (the error message is written to stderr), which makes it easy to use in shell scripts.

The same tool is available as a module if you prefer:

```bash
python -m tracker_scraper udp://exodus.desync.com:6969 2d88e693eda7edf3c1fd0c48e8b99b8fd5a820b2
```

## Handling errors

Network and protocol problems surface as exceptions (Python API) or a non-zero exit code (CLI). Wrap calls you don't control:

```python
from tracker_scraper import scrape

try:
    results = scrape("udp://tracker.example:6969", hashes)
except RuntimeError as exc:
    print(f"Scrape failed: {exc}")
except OSError as exc:
    # socket timeout / DNS failure / connection refused
    print(f"Network error: {exc}")
```

## Next steps

- [Configuration](/tracker-scraper/configuration/) — argument reference, the return shape, timeouts, and logging.
- [Examples](/tracker-scraper/examples/basic/) — runnable UDP, HTTP, and CLI recipes.
