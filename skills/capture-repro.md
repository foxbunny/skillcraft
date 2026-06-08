# Meta-skill: "capture repro" / prove the bug first

**Archetype for a `/capture-repro` command.** Use this to author a skill whose deliverable is **a
durable artifact that proves a bug exists *before* the fix, so it can be proven gone *after* and
guarded against regression**. The boundary: it captures and confirms-failing; it does not fix.

This is the standalone, promoted form of the "reproduce, don't reason-only" principle. A suite can
fold it into [start-work](start-work.md)'s bug path or fire it on its own whenever a defect surfaces.

Read the [README](../README.md) for the skeleton, header-wrapping, and principles. Author this skill
with [authoring-a-skill-suite](authoring-a-skill-suite.md).

**Top guardrail: no "looked wrong on my device" without a captured, re-runnable artifact.** Numbers and
recordings are reproducible; impressions are not.

## Generalized steps (the reusable body)

1. **Reproduce deterministically.** Find the smallest reliable trigger.
2. **Capture as the cheapest durable artifact, in priority order:**
   - An automated **failing test** (preferred) — added to the suite, named for the bug.
   - If it can't be unit-tested (timing / feel / UI), a **deterministic repro script or exact steps**
     plus the **observed measurement** (rendered buffer, latency number, log excerpt, screenshot)
     stored under a conventional repros directory with a README: exact steps, expected vs. actual.
3. **Confirm it fails now** ("before") and record the failing output.
4. **Hand off to the fix.** After the fix, **re-run the same artifact** to confirm it passes ("after");
   record both.
5. **Keep the test in the suite** as a permanent regression guard.

## Facts to discover before emitting

- Test framework + how to add/run a single new test (so the failing test lands in the real suite).
- Where repro artifacts are conventionally stored (a `tests/repros/` or fixtures dir).
- What a *diffable* measurement looks like for this domain (a buffer, a metric, a snapshot) — see
  [metric-ledger](metric-ledger.md) if the project tracks a north-star number.
- The session-log convention, if fixes are noted there (see [session-journal](session-journal.md)).

## Principles that especially apply

- **Reproduce, don't reason-only** — the defining constraint of this archetype.
- **Objective measurement over impression** — capture a number/artifact you can diff; label any
  estimate as such.
- **Honesty over optimism** — record the actual before/after output, not a claim that it's fixed.

## Notes

- Cross-reference siblings: feeds [start-work](start-work.md) (the bug path) and the fix that
  [commit-gate](commit-gate.md) later verifies; the kept test becomes part of the commit gate's suite.
- The repro must be runnable by anyone, not just on the author's machine.
