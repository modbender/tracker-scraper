import argparse
import json
import sys

from .scraper import scrape


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="tracker-scraper",
        description="Scrape a BitTorrent tracker for seeds, peers and completed counts.",
    )
    parser.add_argument(
        "tracker",
        help="Announce URL of the tracker (udp://, http:// or https://).",
    )
    parser.add_argument(
        "hashes",
        nargs="+",
        help="One or more torrent info_hash values (40-char hex).",
    )
    parser.add_argument(
        "--indent",
        type=int,
        default=2,
        help="JSON indentation for the output (default: 2).",
    )
    args = parser.parse_args(argv)

    try:
        results = scrape(tracker=args.tracker, hashes=args.hashes)
    except Exception as exc:  # noqa: BLE001 - surface any scrape error to the CLI user
        print("error: %s" % exc, file=sys.stderr)
        return 1

    print(json.dumps(results, indent=args.indent))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
