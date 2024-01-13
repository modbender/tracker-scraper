# Tracker Scraper

[![Downloads](https://pepy.tech/badge/tracker-scraper)](https://pepy.tech/project/tracker-scraper)
[![Downloads](https://pepy.tech/badge/tracker-scraper/month)](https://pepy.tech/project/tracker-scraper/month)
[![Downloads](https://pepy.tech/badge/tracker-scraper/week)](https://pepy.tech/project/tracker-scraper/week)

A simple torrent tracker scraper

**NOTE: scrape for http trackers work after version >= 1.1 of this package**

## Installation

`pip install tracker-scraper`

## Usage

```python
from tracker_scraper import scrape

results = scrape(
  tracker='udp://exodus.desync.com:6969',
  hashes=[
    "2d88e693eda7edf3c1fd0c48e8b99b8fd5a820b2",
    "8929b29b83736ae650ee8152789559355275bd5c"
  ]
)

print(results)
```

`scrape` Returns the list of seeds, peers and downloads a torrent info_hash has, according to the specified tracker

Args:

- `tracker` (str): The announce url for a tracker, usually taken directly from the torrent metadata.
- `hashes` (list): A list of torrent info_hash's to query the tracker for

Returns:  
A dict of dicts. The key is the torrent info_hash's from the 'hashes' parameter,
and the value is a dict containing "seeds", "peers" and "complete".

#### Example:

```json
{
  "2d88e693eda7edf3c1fd0c48e8b99b8fd5a820b2": {
    "seeds": "34",
    "peers": "189",
    "complete": "10"
  },
  "8929b29b83736ae650ee8152789559355275bd5c": {
    "seeds": "12",
    "peers": "0",
    "complete": "290"
  }
}
```

## Credits

Code taken from project [m2t](https://github.com/erindru/m2t/blob/master/m2t/scraper.py) by Erin Drummond ([erindru](https://github.com/erindru)). Originally written in Python 2.7, updated code to Python 3+ and now using requests
