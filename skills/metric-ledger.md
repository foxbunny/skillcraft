# Meta-skill: "metric ledger" / record a north-star measurement

**Archetype for a `/log-<metric>` command** (e.g. `/latency-log`, `/bundle-size`, `/p99`). Use this to
author a skill whose deliverable is **a measurement appended to a tracked ledger, compared against the
previous best, with regressions flagged as a release blocker**. The boundary: it records and compares;
it does not optimize.

**Skill vs. rule boundary:** that a given metric is the project's *north star* and that *regressions
block release* are **rules** — they live in standing context. This skill performs the **action** of
recording one measurement and applying the regression gate. It references the standard; it doesn't
declare it.

Read the [README](../README.md) for the skeleton, header-wrapping, and principles. Author this skill
with [authoring-a-skill-suite](authoring-a-skill-suite.md).

**Top guardrail: prefer an objective measurement over a felt estimate** — and if only an estimate is
available, **label it as such** in the row. An unlabelled guess pollutes the ledger.

## Generalized steps (the reusable body)

1. **Gather the row's fields:** date, build/commit, the relevant environment (device, OS, config,
   buffer size — whatever moves the number), **the measurement**, and the **method** used.
2. **Append a row** to the ledger file (newest tracked consistently).
3. **Compare to the previous best:**
   - Improved or equal → note what helped in the row.
   - **Regressed → flag it loudly** and add a follow-up item to the task queue. A regression on the
     north-star metric is a release blocker.
4. **Record influences** on the number (a config change, throttling, a tweak) in the row's notes so the
   ledger is interpretable later.

## Facts to discover before emitting

- Which metric is the north star and the ledger file's location + column format.
- The measurement method/tooling and what environment fields actually affect the number.
- The regression policy (block release? warn?) — a **rule** the skill references.
- Where follow-up items go (see [task-queue](task-queue.md)).

## Principles that especially apply

- **Objective measurement over impression** — diffable numbers, labelled estimates.
- **Gate-and-stop discipline** — a regression is a loud blocker, not a quiet row.
- **Append-only history** — add rows; don't rewrite past measurements.
- **Honesty over optimism** — record the real number and method, even when it regressed.

## Notes

- Cross-reference siblings: the measurement may come from a [capture-repro](capture-repro.md) artifact;
  regressions feed [task-queue](task-queue.md) and surface in [postmortem](postmortem.md).
- One ledger per distinct metric. Don't co-mingle unrelated numbers in one file.
