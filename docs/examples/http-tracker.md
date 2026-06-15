---
title: HTTP Tracker
description: Scrape an HTTP/HTTPS tracker, batch several torrents in one request, and safely chunk large hash lists.
sidebar:
  order: 2
---

UDP is the most common tracker transport, but plenty of trackers expose an HTTP or HTTPS scrape endpoint too. The same `scrape()` call handles them — the scheme decides the protocol.

## Scraping an HTTP tracker

Pass an `http://` (or `https://`) announce URL. The library rewrites the `announce` path segment to `scrape` for you, as the HTTP scrape convention requires.

```python
from tracker_scraper import scrape

results = scrape(
    tracker="http://tracker.example.org/announce",
    hashes=["2d88e693eda7edf3c1fd0c48e8b99b8fd5a820b2"],
)

print(results)
```

:::caution
The announce URL must contain `announce` in its path, because that's how the scrape endpoint is derived (`announce` → `scrape`). Trackers that don't expose a scrape endpoint, or whose URL has no `announce` segment, raise a `RuntimeError`. Note that HTTP/HTTPS counts come back as strings — coerce with `int()` if you need numbers.
:::

## Batch-scraping several torrents

Pass multiple hashes to query them in a single request:

```python
from tracker_scraper import scrape

results = scrape(
    tracker="http://tracker.example.org/announce",
    hashes=[
        "2d88e693eda7edf3c1fd0c48e8b99b8fd5a820b2",
        "8929b29b83736ae650ee8152789559355275bd5c",
    ],
)

for info_hash, stats in results.items():
    print(info_hash, "->", stats)
```

## Chunking a large list (UDP)

UDP trackers cap a single scrape at **74 hashes**. If you have more, split the list into chunks and merge the results:

```python
from tracker_scraper import scrape

def scrape_all(tracker, hashes, chunk_size=74):
    merged = {}
    for i in range(0, len(hashes), chunk_size):
        chunk = hashes[i:i + chunk_size]
        merged.update(scrape(tracker, chunk))
    return merged

all_hashes = [...]  # however many you have
stats = scrape_all("udp://exodus.desync.com:6969", all_hashes)
print(f"Scraped {len(stats)} torrents")
```

:::tip
This 74-hash limit is specific to the UDP protocol. HTTP/HTTPS trackers have no fixed library limit — though individual trackers may still impose their own — so you can often pass a long list in one call.
:::

## Next steps

- [Command Line](/tracker-scraper/examples/cli/) — run scrapes from your shell and pipe the JSON output.
- [Configuration](/tracker-scraper/configuration/) — the full argument and return-value reference.
