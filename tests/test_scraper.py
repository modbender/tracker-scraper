"""Offline tests for tracker_scraper.

These tests never touch the network: UDP/HTTP I/O is stubbed and the bencode
parse path is fed a locally-encoded scrape response.
"""

import binascii

import bencodepy
import pytest

import tracker_scraper
from tracker_scraper import scraper

HASH = "2d88e693eda7edf3c1fd0c48e8b99b8fd5a820b2"


def test_public_api():
    assert callable(tracker_scraper.scrape)
    assert tracker_scraper.scrape is scraper.scrape


def test_unknown_scheme_raises():
    with pytest.raises(RuntimeError, match="Unknown tracker scheme"):
        scraper.scrape("ftp://example.org/announce", [HASH])


def test_http_without_announce_raises():
    with pytest.raises(RuntimeError, match="doesnt support scrape"):
        scraper.scrape("http://example.org/foo", [HASH])


def test_udp_too_many_hashes_raises():
    with pytest.raises(RuntimeError, match="74 hashes"):
        scraper.scrape("udp://tracker.example:6969", [HASH] * 75)


def test_get_decoded_dict_decodes_bytes_keys():
    raw = {b"files": {b"complete": 1, b"nested": {b"x": 2}}}
    out = scraper.get_decoded_dict(raw)
    assert out == {"files": {"complete": 1, "nested": {"x": 2}}}


def test_http_scrape_parses_bencoded_response(monkeypatch):
    info_hash = binascii.a2b_hex(HASH)
    payload = {
        b"files": {
            info_hash: {b"complete": 34, b"incomplete": 189, b"downloaded": 10}
        }
    }
    encoded = bencodepy.bencode(payload)

    class FakeResponse:
        status_code = 200
        content = encoded

    captured = {}

    def fake_get(url, *args, **kwargs):
        captured["url"] = url
        return FakeResponse()

    monkeypatch.setattr(scraper.requests, "get", fake_get)

    result = scraper.scrape("http://tracker.example/announce", [HASH])

    assert "scrape" in captured["url"]
    assert result == {HASH: {"seeds": 34, "peers": 189, "complete": 10}}


def test_http_scrape_non_200_raises(monkeypatch):
    class FakeResponse:
        status_code = 503
        content = b""

    monkeypatch.setattr(scraper.requests, "get", lambda *a, **k: FakeResponse())

    with pytest.raises(RuntimeError, match="503 status code"):
        scraper.scrape("http://tracker.example/announce", [HASH])


def test_udp_request_builders_roundtrip():
    req, txid = scraper.udp_create_connection_request()
    assert isinstance(req, bytes) and len(req) == 16
    assert isinstance(txid, int)

    req2, txid2 = scraper.udp_create_scrape_request(0x41727101980, [HASH])
    # 8 (conn id) + 4 (action) + 4 (txid) + 20 (one hash) = 36 bytes
    assert len(req2) == 36
    assert isinstance(txid2, int)


def test_cli_smoke(monkeypatch, capsys):
    from tracker_scraper import __main__ as cli

    monkeypatch.setattr(
        cli, "scrape", lambda tracker, hashes: {h: {"seeds": 1, "peers": 2, "complete": 3} for h in hashes}
    )
    rc = cli.main(["udp://tracker.example:6969", HASH])
    assert rc == 0
    out = capsys.readouterr().out
    assert HASH in out
    assert "seeds" in out


def test_cli_error_returns_nonzero(monkeypatch, capsys):
    from tracker_scraper import __main__ as cli

    def boom(tracker, hashes):
        raise RuntimeError("boom")

    monkeypatch.setattr(cli, "scrape", boom)
    rc = cli.main(["udp://tracker.example:6969", HASH])
    assert rc == 1
    assert "boom" in capsys.readouterr().err
