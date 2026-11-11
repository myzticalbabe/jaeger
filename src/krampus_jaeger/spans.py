# coding: utf-8
"""spans.py -- durable spans for routed delegations, stdlib only.

One span per delegation: who ran what capability, the verdict
(accepted / rejected / unverified), who judged it, how long it took,
and which contract violations fired. Spans append to a JSONL ledger,
so the answer to *was this the right call* survives the process --
the gap this module closes (in-memory deques and warn-only logs do
not survive anything).

Malformed spans are refused at the door with the offending field
named; a span that cannot be built is reported, never half-written.
"""

from __future__ import annotations

import json
import os
import time
import uuid
from contextlib import contextmanager

__all__ = [
    "SpanStore",
    "VERDICTS",
    "build_span",
    "timed",
]

VERDICTS = ("accepted", "rejected", "unverified")

_REQUIRED = ("capability", "verdict")


def build_span(capability, verdict, judged_by=None, success=None,
               duration_ms=None, violations=None, detail="",
               trace_id=None, parent_id=None, span_id=None, ts=None):
    """Build a well-formed span dict; raises ValueError naming the fault."""
    if not capability or not isinstance(capability, str):
        raise ValueError("span needs a non-empty str capability, got %r"
                         % (capability,))
    if verdict not in VERDICTS:
        raise ValueError("span verdict must be one of %s, got %r"
                         % (VERDICTS, verdict))
    violations = list(violations) if violations else []
    if any(not isinstance(v, str) for v in violations):
        raise ValueError("span violations must all be str")
    if success is None:
        success = verdict == "accepted"
    return {
        "span_id": span_id or uuid.uuid4().hex,
        "trace_id": trace_id or uuid.uuid4().hex,
        "parent_id": parent_id,
        "capability": capability,
        "verdict": verdict,
        "judged_by": judged_by,
        "success": bool(success),
        "duration_ms": duration_ms,
        "violations": violations,
        "detail": detail or "",
        "ts": ts if ts is not None else time.time(),
    }


class SpanStore:
    """Append-only JSONL span ledger with query + stats."""

    def __init__(self, path):
        self.path = os.path.abspath(path)
        parent = os.path.dirname(self.path)
        if parent:
            os.makedirs(parent, exist_ok=True)

    def record(self, span):
        """Validate and append; returns the span_id."""
        for key in _REQUIRED:
            if key not in span:
                raise ValueError("span missing required field: %s" % key)
        if span["verdict"] not in VERDICTS:
            raise ValueError("bad verdict: %r" % (span["verdict"],))
        with open(self.path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(span, sort_keys=True) + "\n")
        return span["span_id"]

    def _read_all(self):
        if not os.path.exists(self.path):
            return []
        spans = []
        with open(self.path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    try:
                        spans.append(json.loads(line))
                    except ValueError:
                        continue
        return spans

    def query(self, capability=None, verdict=None, since=None, limit=100):
        """Newest-first spans matching all given filters."""
        spans = self._read_all()
        spans.sort(key=lambda s: s.get("ts", 0), reverse=True)
        out = []
        for span in spans:
            if capability is not None and span.get("capability") \
                    != capability:
                continue
            if verdict is not None and span.get("verdict") != verdict:
                continue
            if since is not None and span.get("ts", 0) < since:
                continue
            out.append(span)
            if len(out) >= limit:
                break
        return out

    def get(self, span_id):
        """Fetch one span by id, or None."""
        for span in self._read_all():
            if span.get("span_id") == span_id:
                return span
        return None

    def stats(self):
        """Counts by verdict/capability + mean duration_ms."""
        spans = self._read_all()
        by_verdict = {v: 0 for v in VERDICTS}
        by_capability = {}
        durations = []
        for span in spans:
            if span.get("verdict") in by_verdict:
                by_verdict[span["verdict"]] += 1
            cap = span.get("capability", "?")
            by_capability[cap] = by_capability.get(cap, 0) + 1
            if isinstance(span.get("duration_ms"), (int, float)):
                durations.append(span["duration_ms"])
        return {
            "total": len(spans),
            "by_verdict": by_verdict,
            "by_capability": by_capability,
            "mean_duration_ms": (sum(durations) / len(durations)
                                 if durations else None),
        }


@contextmanager
def timed(store, capability, **fields):
    """Record a span measuring the block; verdict defaults unverified.

    Usage::

        with timed(store, "madi.fetch", judged_by="krampus") as span:
            ...do the work...
            span["verdict"] = "accepted"

    The span is recorded even when the block raises (as ``rejected``
    with the exception named in violations), then the error propagates.
    """
    start = time.perf_counter()
    span = build_span(capability, fields.pop("verdict", "unverified"),
                      duration_ms=None, **fields)
    try:
        yield span
    except Exception as e:
        span["verdict"] = "rejected"
        span["violations"] = list(span.get("violations", [])) + \
            ["raised: %s: %s" % (type(e).__name__, str(e)[:160])]
        raise
    finally:
        span["duration_ms"] = int((time.perf_counter() - start) * 1000)
        store.record(span)
