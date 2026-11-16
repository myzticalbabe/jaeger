# STEM learning guide — jaeger

Jaeger records durable spans: one written line per routed call, in a JSONL ledger, stdlib only. It is the smallest project here and the easiest to finish in one session.

This guide is for teachers, mentors, club leaders, parents and students who want to
use this repository as a vehicle for real STEM learning — in particular for girls and
other groups still under-represented in computing, engineering and mathematics. It
says what the project actually teaches, how to run a session with it, and what to
remove so that nobody is excluded by accident.

## What this project teaches

**Subject areas**

- observability
- tracing
- file formats
- data integrity

**Skills practised**

- designing a record that answers a future question
- appending without corrupting
- reading a ledger to reconstruct a sequence

## Prerequisites

Python 3.10 or newer. Standard library only — nothing to install, which makes this the best first repository in the set.

Nothing else is assumed for the entry-level activity below: no prior programming
experience, no particular hardware, and no home internet connection.

## Six practices this repository is set up to support

These follow the published guidance on gender-equitable STEM education — connect the
work to learners' lives, let them investigate real problems, treat struggle as part of
the work, name and challenge stereotypes, make the work collaborative, and put
learners in front of diverse role models.

1. **Connect it to their lives.** a group chat log: who said what, in what order, and how you prove it afterwards
2. **Let them investigate.** ask learners to reconstruct a sequence of calls from the ledger alone, with no access to the code that wrote it
3. **Make struggle normal.** Build the session so that the first attempt is *expected*
   to fail. Say out loud that debugging is the subject, not a penalty. Ask "what did
   that error tell you?" before offering the answer.
4. **Challenge the stereotype.** Name who does this work and why it is not a gendered
   skill. Praise the method ("you isolated the variable"), not the person ("you're a
   natural") — the second kind of praise teaches learners that ability is fixed.
5. **Make it social.** one pair writes spans, another pair investigates a failure using only the ledger and reports what they cannot determine
6. **Show diverse role models.** the engineers who turned tracing into a standard practice, and the women who wrote the specs it rests on

## A 90-minute session

1. *(15 min)* Read ten ledger lines and state what happened.
2. *(25 min)* Find a question the ledger cannot answer, and say what field is missing.
3. *(35 min)* Add that field without breaking existing readers.
4. *(15 min)* Re-run and show the new question is answered.

## Vocabulary to define before the session

Specialist vocabulary is a hidden entry test if nobody explains it. Define each of
these the first time it appears, in one sentence, in the learners' own words:

1. **span** — one recorded operation with a start and an end.
2. **ledger** — the append-only file of spans.
3. **trace** — all the spans belonging to one request.

## Accessibility

Read [ACCESSIBILITY.md](ACCESSIBILITY.md) before running a session. Two rules matter
most in a mixed-ability room:

- Every activity must be completable with a keyboard alone, with a visible focus ring.
- Every instruction names the control or the heading ("the **Run** button in the
  toolbar"), never a colour or a position.

Pair learners rather than singling anyone out, and always offer a text-only route for
a visual step.

## Contributing as a learner

Small, well-scoped contributions are the point, not a consolation prize:

- Browse issues labelled
  [`good first issue`](https://github.com/myzticalbabe/jaeger/labels/good%20first%20issue).
- Read [CONTRIBUTING.md](CONTRIBUTING.md) — it has a section written for first-time
  contributors.
- Ask in [SUPPORT.md](SUPPORT.md) if anything is unclear. Asking is expected here; it
  is not a failure.

## Licence and classroom reuse

Classroom, club and workshop use is welcome. See `LICENSE` for the exact terms, and
check whether your institution requires a separate agreement before redistributing
modified copies.
