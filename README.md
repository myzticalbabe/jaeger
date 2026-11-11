# krampus-jaeger

Durable spans for routed delegations. One span per call — capability,
verdict (`accepted` / `rejected` / `unverified`), judge, duration,
violations — appended to a JSONL ledger so *was this the right call*
is answerable after the process exits. Stdlib only, no services.

```python
from krampus_jaeger import SpanStore, timed

store = SpanStore("spans.jsonl")

with timed(store, "madi.fetch", judged_by="krampus") as span:
    page = fetch(url)
    span["verdict"] = "accepted" if page["state"] == "ok" else "rejected"

print(store.stats())
# {'total': 1, 'by_verdict': {...}, 'by_capability': {...},
#  'mean_duration_ms': ...}
```

Malformed spans are refused with the offending field named; exceptions
inside `timed` record a `rejected` span naming the error, then propagate.
