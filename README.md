# Tracker Scraper

[![PyPI](https://img.shields.io/pypi/v/tracker-scraper.svg)](https://pypi.org/project/tracker-scraper/)
[![Python versions](https://img.shields.io/pypi/pyversions/tracker-scraper.svg)](https://pypi.org/project/tracker-scraper/)
[![Downloads](https://pepy.tech/badge/tracker-scraper)](https://pepy.tech/project/tracker-scraper)
[![Downloads](https://pepy.tech/badge/tracker-scraper/month)](https://pepy.tech/project/tracker-scraper/month)

A simple BitTorrent tracker scraper — query a tracker for the seeds, peers, and completed counts of one or more torrents, over both UDP and HTTP/HTTPS.

## Documentation

Full documentation lives at **[modbender.in/tracker-scraper](https://modbender.in/tracker-scraper/)**.

## Installation

```bash
pip install tracker-scraper
```

## Usage

### Python

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

`scrape(tracker, hashes)` returns a dict of dicts. The key is each torrent `info_hash` from the `hashes` argument, and the value is a dict with `seeds`, `peers`, and `complete`:

```json
{
  "2d88e693eda7edf3c1fd0c48e8b99b8fd5a820b2": {
    "seeds": 34,
    "peers": 189,
    "complete": 10
  }
}
```

**Arguments**

- `tracker` (`str`): the announce URL for a tracker (`udp://`, `http://`, or `https://`), usually taken directly from the torrent metadata.
- `hashes` (`list[str]`): a list of torrent `info_hash` values to query.

> **Note:** HTTP/HTTPS tracker scraping works from version 1.1 onwards. UDP scrapes are limited to 74 hashes per request.

### Command line

Installing the package also adds a `tracker-scraper` command that prints results as JSON:

```bash
tracker-scraper udp://exodus.desync.com:6969 2d88e693eda7edf3c1fd0c48e8b99b8fd5a820b2
```

Run `tracker-scraper --help` for all options.

## Requirements

- Python 3.9+
- [`requests`](https://pypi.org/project/requests/), [`bencode.py`](https://pypi.org/project/bencode.py/)

## Development

```bash
pip install -e ".[test]"
pytest
```

## Credits

Code originally adapted from the [m2t](https://github.com/erindru/m2t/blob/master/m2t/scraper.py) project by Erin Drummond ([erindru](https://github.com/erindru)). Originally written for Python 2.7; updated to Python 3 and `requests`.
