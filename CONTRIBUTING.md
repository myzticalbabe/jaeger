# Contributing

Thanks for taking an interest in **jaeger** (`krampus-jaeger` on PyPI). It is part
of the [myzticalbabe](https://github.com/myzticalbabe) ecosystem, a set of
repositories for education and research tooling.

Jaeger is a small, **standard-library-only** Python library for durable spans: one
written record per delegated call, appended to a JSONL ledger on disk. It has no
runtime dependencies, no service to run and no command-line interface.

## Before you start

- Read the project [README.md](README.md) for what the repository actually does and
  how to use it.
- Search the existing issues and pull requests — the change you want may already be
  discussed.
- For anything larger than a typo or a one-line fix, open an issue first so the
  design can be agreed before code is written.

## Setting up

Jaeger requires **Python 3.13 or newer** (`requires-python` in `pyproject.toml`).
Python 3.13 is the version CI runs.

```bash
git clone https://github.com/myzticalbabe/jaeger.git
cd jaeger
python -m venv .venv
. .venv/Scripts/activate        # Windows
# . .venv/bin/activate         # Linux and macOS

pip install --upgrade pip
pip install -e ".[test]"
```

`pip install -e ".[test]"` installs the package in editable mode together with
`pytest`. The package itself has **no** runtime dependencies, so an editable
install is all that is needed to import it.

## Running the checks

Run the same commands CI runs, from the repository root:

```bash
python -m pytest tests/ -v --tb=short
```

The suite is fully offline — every test writes to a temporary ledger file, so no
network, no service and no credentials are involved.

CI (`.github/workflows/ci.yml`) reports the status check named **`ci`**, which is
the context `main` requires. A second workflow, `.github/workflows/test.yml`,
reports `test`. Both must be green before a pull request can merge.

If a check cannot run in your environment, say so in the pull request instead of
deleting or skipping the step.

## Ways to contribute that are not code

- Report a bug with a minimal reproduction.
- Improve the documentation or add an example.
- Report an accessibility problem (keyboard traps, missing text alternatives,
  unreadable contrast) if you add any user-facing content.
- Review a pull request and say what confused you — that is real feedback.

## Making a change

1. Fork the repository and create a branch: `git checkout -b fix/short-description`.
2. Keep the change focused. Unrelated refactors belong in a separate pull request.
3. Match the surrounding style; do not reformat whole files to make a small fix.
   The library is standard-library-only — do not add a runtime dependency without
   saying why in the pull request.
4. Run the checks above.
5. Write a commit message that explains *why* the change was made.
6. Open the pull request and fill in the template.

New behaviour needs a test in `tests/`. The suite is small and fast; a change that
cannot be tested should say why in the pull request.

## Reporting bugs

Use the **Bug report** issue form
(`.github/ISSUE_TEMPLATE/bug_report.yml`). A good report contains:

- what you expected to happen and what happened instead;
- the exact command or input that triggers it;
- the full error output, not a paraphrase;
- your operating system and Python version.

A **security vulnerability is not a bug report** — report it privately, as
described in [SECURITY.md](SECURITY.md).

## Learner-facing content

This repository currently holds no learner-facing material: it is a library, its
documentation is plain Markdown, and its only user-visible surface is the text
output of the JSONL ledger. If your change adds learner-facing content — a
tutorial page, an interactive page, example material for a class — then:

- keep the reading level age-appropriate and define any new term the first time it
  is used;
- keep the layout keyboard-navigable and give every image or canvas a text
  alternative;
- avoid examples that assume prior exposure to programming.

## Code of conduct

Participation is covered by [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). Be kind; assume
good faith.

## Licence

By contributing you agree that your contribution is licensed under the same licence
as the repository — the **SOUL FORGE License v1.0**, which is reproduced in
[LICENSE](LICENSE).
