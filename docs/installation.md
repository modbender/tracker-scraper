---
title: Installation
description: Install Tracker Scraper from PyPI with pip, verify the import and CLI, and review the runtime requirements.
sidebar:
  order: 2
---

Tracker Scraper is published on [PyPI](https://pypi.org/project/tracker-scraper/), so installation is a single `pip` command.

## Install from PyPI

```bash
pip install tracker-scraper
```

This pulls in the two runtime dependencies for you — [`requests`](https://pypi.org/project/requests/) and [`bencode.py`](https://pypi.org/project/bencode.py/).

:::tip
Prefer to install into an isolated environment. With a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate
pip install tracker-scraper
```
:::

## Requirements

| | |
| --- | --- |
| Python | 3.9 or newer |
| Dependencies | `requests` (>= 2.20), `bencode.py` (>= 4.0) |
| Platforms | OS-independent (Linux, macOS, Windows) |

## Verify the install

Check the library import:

```bash
python -c "from tracker_scraper import scrape; print('ok')"
```

And the command-line entry point:

```bash
tracker-scraper --help
```

You should see the CLI usage summary. The same command is also available as a module:

```bash
python -m tracker_scraper --help
```

## Next steps

- [Usage](/tracker-scraper/usage/) — call `scrape()` from Python or run the CLI.
- [Examples](/tracker-scraper/examples/basic/) — end-to-end recipes you can copy and run.
