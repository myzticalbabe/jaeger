# Security Policy

## Supported versions

Jaeger is at version **0.1.0** and pre-1.0. Security fixes are made on `main` and
released with the next version; there is no long-term-support branch.

| Version | Supported |
| --- | --- |
| `0.1.0` (current release, tag `v0.1.0`) | yes |
| `main` (unreleased development) | yes |
| anything older than `0.1.0` | no — upgrade to `0.1.0` |

The package has **no runtime dependencies** (standard library only), and its
attack surface is small: it reads and appends to a JSONL ledger file at a path you
choose. Two areas are worth particular attention in a report:

- **Ledger parsing.** `SpanStore` reads a JSONL file back with `json.loads` per
  line and skips any line that fails to parse. Behaviour on hostile or malformed
  ledger content is in scope.
- **Path handling.** `SpanStore.__init__` resolves the ledger path with
  `os.path.abspath` and creates the parent directory with `os.makedirs`. How that
  interacts with untrusted paths is in scope.

## Reporting a vulnerability

**Please do not open a public issue for a security vulnerability.** A public issue
tells everyone about the problem before it is fixed.

This project has no public mailing list and no security-specific email address.
The private reporting channel is GitHub's own private vulnerability reporting form
for this repository:

**<https://github.com/myzticalbabe/jaeger/security/advisories/new>**

Open that page and use **"Report a vulnerability"**. A report filed there is
visible only to the maintainer. It creates a private advisory that you and the
maintainer can discuss, and that you can withdraw or publish later with your
agreement — nothing becomes public without you choosing to publish it.

Private vulnerability reporting is enabled on this repository; if for any reason the
button is missing when you visit the page, open an issue that says only
"I would like to report a security vulnerability privately" and contact details
will be arranged in the reply. Do not put the vulnerability details in that issue.

### What to include

- the version or commit you tested (`pip show krampus-jaeger`, or `git rev-parse HEAD`);
- your operating system and Python version;
- what an attacker could do, and what they would need in order to do it;
- a minimal reproduction — a few lines of Python, or a ledger file that triggers
  the behaviour;
- the impact you believe it has.

### What to expect

- An acknowledgement within **7 days**.
- An assessment of the report — whether it is accepted, and a severity judgement —
  within **30 days** of the acknowledgement.
- A fix, or a published explanation of why no fix is planned, as soon as
  practical. You will be credited in the advisory unless you ask not to be.
- If a report is declined, you will get the reason, and you are free to publish it
  yourself.

### Disclosure

Please give the maintainer **90 days** from acknowledgement before disclosing
publicly, so that a fix can be prepared and released. If a fix is not ready within
that window, say so in the advisory thread and the timeline can be extended.

## What is *not* a security vulnerability

- A crash or a `ValueError` from a malformed span that you constructed yourself.
  Those are refused by design and are reported with the offending field named;
  please open a normal bug report instead.
- The absence of a `__main__` entry point or a console script. Jaeger is a library
  and is not intended to be executable.
- Reports that depend on the machine already being compromised, or on the reporter
  already having write access to the ledger file.
- Missing hardening against an attacker who can already modify the repository or
  its GitHub settings.

## Security-relevant configuration

There is nothing to configure. The ledger path is the only input, and it is chosen
by the calling code. If you deploy Jaeger somewhere that lets untrusted callers
choose the ledger path, keep that path inside a directory the caller cannot escape.
