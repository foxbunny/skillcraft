# Meta-skill: "session journal" / append a dev diary entry

**Archetype for a `/diary` command.** Use this to author a skill whose deliverable is **a dated,
append-only entry summarizing a working session** — what changed, the decisions and their *why*, the
immediate next steps, and open questions/risks. The boundary: it records what happened; it is not a
process retrospective (that's [postmortem](postmortem.md)) and not the task backlog (that's
[task-queue](task-queue.md)).

**Skill vs. rule boundary:** that the journal is **append-only and immutable** is a **rule**; this skill
performs the **action** of adding one entry while honoring that rule.

Read the [README](../README.md) for the skeleton, header-wrapping, and principles. Author this skill
with [authoring-a-skill-suite](authoring-a-skill-suite.md).

**Top guardrail: never rewrite or edit past entries — history is immutable.** Add a new entry; record
any corrections as new entries.

## Generalized steps (the reusable body)

1. **Read the most recent entry** for continuity.
2. **Add a new entry** dated with the environment's current date, containing:
   - **Done** — what changed (link files / slices).
   - **Decisions** — choices made and the *why*, one line each.
   - **Next** — the immediate next steps.
   - **Open** — unresolved questions / risks.
3. **Keep it terse** — a log, not an essay.
4. **Reconcile the backlog** while here (check off done, add new work) — see [task-queue](task-queue.md).

## Facts to discover before emitting

- The journal file's location and ordering convention (newest-at-top vs. appended).
- The environment's current date (use it; don't guess).
- Whether decisions/links follow a house format worth matching.

## Principles that especially apply

- **Append-only history** — the defining constraint; never edit the past.
- **Honesty over optimism** — if nothing substantive happened, say so in one line rather than padding.

## Notes

- Cross-reference siblings: distinct from [postmortem](postmortem.md) (process improvements) and
  [task-queue](task-queue.md) (the backlog); the three often run together at session end.
