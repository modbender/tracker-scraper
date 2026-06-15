---
title: Basic
description: A minimal end-to-end example — install the package and scrape a UDP tracker for a single torrent's seed, peer and completed counts.
sidebar:
  order: 1
---

The smallest complete program: install the package, call `scrape()` once against a UDP tracker, and print the result.

## 1. Install

```bash
pip install tracker-scraper
```

## 2. Scrape a UDP tracker

```python
# scrape_basic.py
from tracker_scraper import scrape

results = scrape(
    tracker="udp://exodus.desync.com:6969",
    hashes=["2d88e693eda7edf3c1fd0c48e8b99b8fd5a820b2"],
)

print(results)
```

## 3. Run it

```bash
python scrape_basic.py
```

You get back a dictionary keyed by the `info_hash`, with the live counts:

```python
{'2d88e693eda7edf3c1fd0c48e8b99b8fd5a820b2': {'seeds': 34, 'peers': 189, 'complete': 10}}
```

## Reading individual stats

```python
from tracker_scraper import scrape

info_hash = "2d88e693eda7edf3c1fd0c48e8b99b8fd5a820b2"
stats = scrape("udp://exodus.desync.com:6969", [info_hash])[info_hash]

print(f"Seeders:   {stats['seeds']}")
print(f"Leechers:  {stats['peers']}")
print(f"Completed: {stats['complete']}")
```

:::tip
The `info_hash` you pass is the same key you read back, so a one-liner like `scrape(tracker, [h])[h]` is a handy way to fetch the stats for a single torrent.
:::

## Next steps

- [HTTP Tracker](/tracker-scraper/examples/http-tracker/) — scrape an `http://` / `https://` tracker and batch multiple torrents.
- [Command Line](/tracker-scraper/examples/cli/) — do the same thing straight from your shell.
