# jaeger

Jaeger — durable spans for routed delegations: one written record per call, JSONL ledger, stdlib only.

[![CI](https://github.com/myzticalbabe/jaeger/actions/workflows/ci.yml/badge.svg)](https://github.com/myzticalbabe/jaeger/actions/workflows/ci.yml)
[![Pages Deploy](https://github.com/myzticalbabe/jaeger/actions/workflows/pages-deploy.yml/badge.svg)](https://github.com/myzticalbabe/jaeger/actions/workflows/pages-deploy.yml)
[![License: SOUL FORGE](https://img.shields.io/badge/License-SOUL_FORGE-violet.svg)](LICENSE)
[![GitHub release](https://img.shields.io/github/v/release/myzticalbabe/jaeger)](https://github.com/myzticalbabe/jaeger/releases)
[![GitHub stars](https://img.shields.io/github/stars/myzticalbabe/jaeger?style=social)](https://github.com/myzticalbabe/jaeger/stargazers)

---

## Overview

Distributed tracing with durable JSONL ledger.

Each span records one delegated call: which capability ran, the verdict
(`accepted`, `rejected` or `unverified`), who judged it, how long it took, and
which contract violations fired. Spans are appended to a JSONL ledger on disk, so
the answer to *was this the right call* outlives the process that made it.

The ledger is plain JSONL — one JSON object per line, append-only, readable with
any text editor.

## Who it is for

- **Developers of multi-step pipelines** — agent or service pipelines — who need
  to record what each step did, who judged it and why.
- **Researchers, educators and students** who want a trace they can read back with
  nothing but the standard library: no collector to run, no dashboard, no account.
- **Anyone auditing a past run.** The ledger is a plain file, so it can be copied,
  diffed or read with `jq`.

Jaeger is a library. It is standard-library-only, has no runtime dependencies, and
has no daemon to run and no command-line interface.

## Installation

Requires **Python 3.13 or newer** (see `requires-python` in `pyproject.toml`).

```bash
pip install -e .
```

For the test suite as well:

```bash
pip install -e ".[test]"
```

## Usage

There is no command-line interface; use the library:

```python
from krampus_jaeger import SpanStore, timed

store = SpanStore("spans.jsonl")

with timed(store, "madi.fetch", judged_by="krampus") as span:
    ...                       # do the work
    span["verdict"] = "accepted"

# Every span is on disk now, one JSON object per line.
for span in store.query(verdict="accepted"):
    print(span["capability"], span["detail"])
```

`build_span(...)` builds a span by hand when `timed` does not fit.
`SpanStore.query(...)` filters by capability, verdict and time; `stats()` returns
counts by verdict and capability plus the mean duration.

## Running the tests

```bash
pip install -e ".[test]"
python -m pytest tests/ -v --tb=short
```

The suite is fully offline — every test writes to a temporary ledger file, so no
network, service or credentials are involved. The same command runs in CI
(`.github/workflows/ci.yml`), which reports the `ci` status check.

## Architecture

See [Domain Atlas](https://myzticalbabe.github.io) for interactive visualization.

## License

This project is licensed under the **SOUL FORGE License v1.0** — see [LICENSE](LICENSE) for details.

> *"Code is crystallized intention. Tend the fire."*

## Related Repositories

| Repo | Description |
|------|-------------|
| [azazael](https://github.com/myzticalbabe/azazael) | Monorepo: worm registry, cluster system, agent harness |
| [EveUnleashed](https://github.com/myzticalbabe/EveUnleashed) | Gamora, Lucy, Jaeger, Berzerker AIO native on 3.16t |
| [eliza](https://github.com/myzticalbabe/eliza) | Companion runtime: shards, adopted trees |
| [codex-video-engine](https://github.com/myzticalbabe/codex-video-engine) | CODEX Studio desktop app + video engine |
| [ecosystem-orchestrator](https://github.com/myzticalbabe/ecosystem-orchestrator) | ML platform install/orchestration |
| [scribe](https://github.com/myzticalbabe/scribe) | Documentation generation |
| [persephone-sync](https://github.com/myzticalbabe/persephone-sync) | Cross-platform env sync |
| [hydra-mlcluster](https://github.com/myzticalbabe/hydra-mlcluster) | Adaptive ML cluster processing |
| [flaming-sword](https://github.com/myzticalbabe/flaming-sword) | Defensive instrument: sentinel, compliance, formal verification |
| [shardex](https://github.com/myzticalbabe/shardex) | Shard execution engine |
| [krampus](https://github.com/myzticalbabe/krampus) | Composition: MellifluousML, Madi, Gamora, Eve, Lilith |
| [azazael-core](https://github.com/myzticalbabe/azazael-core) | Installable, interpreter-agnostic repackaging |
| [grantforge](https://github.com/myzticalbabe/grantforge) | AI-native grant tooling |
| [madi](https://github.com/myzticalbabe/madi) | Browsing instrument: fetch, challenge taxonomy, scorer |
| [jaeger](https://github.com/myzticalbabe/jaeger) | Durable spans, JSONL ledger, stdlib only |
| [cradle](https://github.com/myzticalbabe/cradle) | Composition over FLAMING SWORD, REAPER, GRIMOIRE |
| [esquire-admissibility](https://github.com/myzticalbabe/esquire-admissibility) | AI-evidence admissibility gates |
| [nurse-ratchet](https://github.com/myzticalbabe/nurse-ratchet) | Behavioural package: person state modelled |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Links

- **Monorepo**: https://github.com/myzticalbabe/azazael
- **Landing Hub**: https://myzticalbabe.github.io
- **Domain Atlas**: https://myzticalbabe.github.io/index.html
- **Issues**: https://github.com/myzticalbabe/jaeger/issues