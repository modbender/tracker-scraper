# Changelog

All notable changes to this project are documented here. This project adheres to
[Semantic Versioning](https://semver.org/).

## [1.2.0]

### Added

- Command-line interface: a `tracker-scraper` console script (and `python -m tracker_scraper`)
  that scrapes a tracker and prints the results as JSON, with `--indent` formatting and a
  non-zero exit code on failure.
- Offline test suite (`tests/`) covering URL-scheme routing, the HTTP bencode parse path,
  UDP request builders, error handling, and the CLI — no network access required.
- GitHub Actions workflows: matrix test runs on Python 3.9–3.13, and a PyPI publish workflow
  using OIDC trusted publishing on tag push.

### Changed

- Migrated packaging from `setup.py` to `pyproject.toml` (PEP 621 metadata).
- Updated the supported Python range to 3.9–3.14 and refreshed the trove classifiers.
- Pinned minimum dependency versions (`requests>=2.20`, `bencode.py>=4.0`).
- Repointed the README "Documentation" link to https://modbender.in/tracker-scraper/.

### Removed

- The build-only `readme-renderer` dependency, which was imported but unused.
- The legacy `test.py` script that depended on a live network connection.

## [1.1.1]

- Updates to README, requirements, and test script.

## [1.1.0]

- HTTP tracker scraping fixed.

## [1.0.1]

- Maintenance release.

## [1.0.0]

- Initial release.
