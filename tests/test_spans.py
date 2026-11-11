# coding: utf-8
"""Tests for krampus-jaeger spans. All offline (tmp ledger files)."""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from krampus_jaeger import SpanStore, VERDICTS, build_span, timed  # noqa: E402


@pytest.fixture()
def store(tmp_path):
    return SpanStore(str(tmp_path / "spans.jsonl"))


# -- construction ------------------------------------------------------

def test_build_span_defaults():
    s = build_span("madi.fetch", "accepted", judged_by="krampus")
    assert s["success"] is True
    assert s["violations"] == []
    assert len(s["span_id"]) == 32
    assert len(s["trace_id"]) == 32
    assert isinstance(s["ts"], float)


def test_build_span_rejects_bad_verdict():
    with pytest.raises(ValueError, match="verdict"):
        build_span("x", "maybe")


def test_build_span_rejects_empty_capability():
    with pytest.raises(ValueError, match="capability"):
        build_span("", "accepted")


def test_build_span_rejects_non_str_violations():
    with pytest.raises(ValueError, match="violations"):
        build_span("x", "accepted", violations=[42])


def test_verdicts_are_the_three():
    assert set(VERDICTS) == {"accepted", "rejected", "unverified"}


# -- ledger ------------------------------------------------------------

def test_record_and_get_roundtrip(store):
    s = build_span("gamora.route", "accepted")
    assert store.record(s) == s["span_id"]
    assert store.get(s["span_id"])["capability"] == "gamora.route"


def test_record_refuses_malformed(store):
    with pytest.raises(ValueError, match="verdict"):
        store.record({"capability": "x", "verdict": "maybe"})


def test_ledger_survives_reopen(tmp_path):
    path = str(tmp_path / "spans.jsonl")
    SpanStore(path).record(build_span("a", "accepted"))
    reopened = SpanStore(path)
    assert reopened.stats()["total"] == 1


def test_query_filters_and_newest_first(store):
    old = build_span("a", "accepted", ts=1000.0)
    new = build_span("a", "rejected", ts=2000.0)
    other = build_span("b", "accepted", ts=3000.0)
    for s in (old, new, other):
        store.record(s)
    assert [s["verdict"] for s in store.query(capability="a")] == \
        ["rejected", "accepted"]
    assert len(store.query(verdict="accepted")) == 2
    assert len(store.query(since=2500.0)) == 1
    assert len(store.query(limit=2)) == 2


def test_stats_counts_and_mean(store):
    store.record(build_span("a", "accepted", duration_ms=10))
    store.record(build_span("a", "rejected", duration_ms=30))
    stats = store.stats()
    assert stats["total"] == 2
    assert stats["by_verdict"]["accepted"] == 1
    assert stats["by_capability"] == {"a": 2}
    assert stats["mean_duration_ms"] == 20.0


def test_stats_empty_ledger(store):
    stats = store.stats()
    assert stats["total"] == 0
    assert stats["mean_duration_ms"] is None


def test_get_missing_returns_none(store):
    assert store.get("nope") is None


# -- timed context -----------------------------------------------------

def test_timed_records_duration_and_verdict(store):
    with timed(store, "madi.fetch", judged_by="krampus") as span:
        span["verdict"] = "accepted"
    got = store.get(span["span_id"])
    assert got["verdict"] == "accepted"
    assert isinstance(got["duration_ms"], int)


def test_timed_records_raise_as_rejected(store):
    with pytest.raises(RuntimeError):
        with timed(store, "eve.run"):
            raise RuntimeError("boom")
    rejected = store.query(verdict="rejected")
    assert len(rejected) == 1
    assert any("boom" in v for v in rejected[0]["violations"])
