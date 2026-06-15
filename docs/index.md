---
title: Tracker Scraper
description: A tiny Python library and CLI that queries a BitTorrent tracker for the seed, peer and completed counts of one or more torrents, over both UDP and HTTP/HTTPS.
sidebar:
  order: 1
---

Tracker Scraper is a small, dependency-light Python package that asks a BitTorrent tracker how many seeds, peers, and completed downloads a torrent has — given the tracker's announce URL and one or more torrent `info_hash` values.

It speaks both tracker scrape protocols:

- **UDP trackers** (`udp://…`) via the binary [UDP tracker protocol](https://www.bittorrent.org/beps/bep_0015.html).
- **HTTP / HTTPS trackers** (`http://…`, `https://…`) via the [bencoded scrape convention](https://www.bittorrent.org/beps/bep_0048.html).

You give it a tracker and a list of hashes; it gives you back a plain dictionary of stats. That's the whole library.

## Key features

- **One function, one call** — `scrape(tracker, hashes)` returns a `dict` of per-hash stats. Nothing to instantiate, no session to manage.
- **UDP and HTTP/HTTPS** — the announce-URL scheme is detected automatically and routed to the right protocol.
- **Batch scraping** — query many torrents in a single request (up to 74 per UDP request, a protocol limit).
- **Command-line interface** — scrape straight from your shell and get JSON on stdout, no script required.
- **Tiny footprint** — only [`requests`](https://pypi.org/project/requests/) and [`bencode.py`](https://pypi.org/project/bencode.py/) as runtime dependencies.

## A 30-second taste

Install it:

```bash
pip install tracker-scraper
```

Scrape a UDP tracker from Python:

```python
from tracker_scraper import scrape

results = scrape(
    tracker="udp://exodus.desync.com:6969",
    hashes=[
        "2d88e693eda7edf3c1fd0c48e8b99b8fd5a820b2",
        "8929b29b83736ae650ee8152789559355275bd5c",
    ],
)

print(results)
```

Or from the command line:

```bash
tracker-scraper udp://exodus.desync.com:6969 2d88e693eda7edf3c1fd0c48e8b99b8fd5a820b2
```

Either way you get a dictionary keyed by `info_hash`, each value holding `seeds`, `peers`, and `complete`:

```json
{
  "2d88e693eda7edf3c1fd0c48e8b99b8fd5a820b2": {
    "seeds": 34,
    "peers": 189,
    "complete": 10
  }
}
```

## Compatibility

| | Supported |
| --- | --- |
| Tracker Scraper | 1.x |
| Python | 3.9 – 3.14 |
| Tracker protocols | UDP, HTTP, HTTPS |

:::caution
A live tracker is contacted over the network. Scraping reaches out to whatever host the announce URL points at — make sure outbound UDP/TCP to that tracker is allowed, and expect timeouts when a tracker is down or unreachable.
:::

## Where to next

- [Installation](/tracker-scraper/installation/) — install from PyPI and confirm it works.
- [Usage](/tracker-scraper/usage/) — the `scrape()` API and the `tracker-scraper` CLI in detail.
- [Configuration](/tracker-scraper/configuration/) — arguments, return shape, timeouts, and logging.
- [Examples](/tracker-scraper/examples/basic/) — copy-pasteable recipes for UDP, HTTP, and the CLI.
