# Meta-skill: "task queue" / maintain the persistent backlog

**Archetype for a `/todo` command.** Use this to author a skill whose deliverable is **a reconciled,
persistent cross-session task queue** — explicitly distinct from the agent's *ephemeral in-session
task list*. The boundary: it maintains the durable backlog file; it doesn't do the work.

**Skill vs. rule boundary:** *where the queue lives and its format* (a tracked `docs/TODO.md` with a
`Now` section) is a **rule/convention** in standing context; this skill performs the **action** of
reading and reconciling it.

Read the [README](../README.md) for the skeleton, header-wrapping, and principles. Author this skill
with [authoring-a-skill-suite](authoring-a-skill-suite.md).

**Top guardrail: stay honest about state.** If something was skipped or deferred, leave it open with a
brief note rather than silently dropping it.

## Generalized steps (the reusable body)

1. **Read the queue file.**
2. **Reconcile with what just happened:** check off completed items, add newly discovered work,
   re-point the active-focus (`Now`) section.
3. **When picking up work, pull from the active focus / current group** — not an arbitrary item.
4. **Stay honest** — open items that were deferred keep a one-line note on why.

## Facts to discover before emitting

- The queue file's location and format (checkbox groups, a `Now` section, slice/area grouping).
- How it relates to any issue tracker (is this the source of truth, or a local mirror?).
- The distinction the project draws between this durable queue and the in-session task list.

## Principles that especially apply

- **Honesty over optimism** — don't silently drop deferred work; mark it.
- **Append-only spirit** — reconcile forward; preserve the trail of what changed.

## Notes

- Cross-reference siblings: reconciled alongside [session-journal](session-journal.md) at session end;
  started via the prep/next flow in [start-work](start-work.md).
- This is a thin maintenance skill — its value is consistency, not complexity. Keep it small.
