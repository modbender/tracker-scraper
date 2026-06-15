---
title: Command Line
description: Use the tracker-scraper command-line tool — scrape from the shell, format the JSON output, and use the exit code in scripts.
sidebar:
  order: 3
---

Installing the package adds a `tracker-scraper` command. It's the quickest way to check a torrent's stats without writing any Python.

## Scrape one torrent

```bash
tracker-scraper udp://exodus.desync.com:6969 2d88e693eda7edf3c1fd0c48e8b99b8fd5a820b2
```

```json
{
  "2d88e693eda7edf3c1fd0c48e8b99b8fd5a820b2": {
    "seeds": 34,
    "peers": 189,
    "complete": 10
  }
}
```

## Scrape several at once

List multiple hashes after the tracker URL:

```bash
tracker-scraper udp://exodus.desync.com:6969 \
  2d88e693eda7edf3c1fd0c48e8b99b8fd5a820b2 \
  8929b29b83736ae650ee8152789559355275bd5c
```

## Compact output

The output is pretty-printed with an indent of `2` by default. Pass `--indent 0` for compact JSON, handy when piping:

```bash
tracker-scraper --indent 0 udp://exodus.desync.com:6969 2d88e693eda7edf3c1fd0c48e8b99b8fd5a820b2
```

## Pipe into other tools

Because the output is plain JSON on stdout, you can pipe it straight into [`jq`](https://jqlang.github.io/jq/):

```bash
tracker-scraper udp://exodus.desync.com:6969 2d88e693eda7edf3c1fd0c48e8b99b8fd5a820b2 \
  | jq '.[].seeds'
```

## Use the exit code in scripts

The command exits `0` on success and `1` on failure (with the error written to stderr), so it composes cleanly in shell scripts:

```bash
if tracker-scraper udp://exodus.desync.com:6969 "$HASH" > stats.json; then
  echo "Scrape succeeded"
else
  echo "Scrape failed" >&2
fi
```

## Run it as a module

If the console script isn't on your `PATH`, the same tool runs via `-m`:

```bash
python -m tracker_scraper udp://exodus.desync.com:6969 2d88e693eda7edf3c1fd0c48e8b99b8fd5a820b2
```

:::tip
Run `tracker-scraper --help` any time for the full argument list.
:::

## Next steps

- [Usage](/tracker-scraper/usage/) — the Python API behind the CLI.
- [Configuration](/tracker-scraper/configuration/) — argument reference and protocol limits.
