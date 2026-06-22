# Meta-skill: "learn from it" / postmortem

**Archetype for a `/postmortem` command.** Use this to author a skill whose deliverable is **durable,
honest improvements drawn from a finished session**. The boundary: it proposes and applies
*guidance/rule* changes; it does not commit them into open work.

Read the [README](../README.md) for the skeleton, header-wrapping, and principles. Author this skill
with [authoring-a-skill-suite](authoring-a-skill-suite.md).

**Top guardrail: don't manufacture findings or over-claim fault.** Distinguish real corrections from
plain directives; ground every claim in a verifiable anchor.

**Check from two angles, not one.** *Hardening* — what went wrong and how to prevent it (corrections, bugs,
skipped steps). *Streamlining* — what was **correct but tedious**: a multi-step manual sequence you'd
repeat next time that a new or upgraded skill could do deterministically. The streamlining angle has
nothing to do with mistakes — **a clean session with no bugs can still surface a valuable skill**, so
don't skip it just because nothing broke.

## Generalized steps (the reusable body)

1. **Recap with verifiable anchors** — SHAs, PRs, files. No vague "we did some work."
2. **Scan both lenses and capture each finding.** For a **hardening** signal write *what happened →
   what the fix was → the underlying why (the lesson)*; for a **streamlining** signal write *the steps
   you ran → how often this recurs → what a skill could do deterministically instead* (and whether a
   skill already exists that should own it). Distinguish genuine corrections from ordinary directives
   ("show the diff" is an instruction, not a correction); don't invent findings. Signals to look for:
   user corrections / "no, actually…"; bugs you introduced or rework done twice; skipped or rushed
   steps; failed or retried commands and setup snags; permission prompts that recur for safe commands;
   context that had to be rediscovered; slow/uncertain decisions a standing rule could settle; and —
   the streamlining angle — any repetitive ordered manual sequence (≈3+ steps) you'd repeat on the next
   task, *even if it went perfectly*.
3. **Diagnose root causes** and keep only the patterns likely to **recur** — drop one-offs.
4. **Propose each fix mapped to its right home — the lightest durable mechanism that removes the
   friction:**
   - **Standing-context rule** (`CLAUDE.md` / `AGENTS.md`) — settles a recurring decision/convention.
   - **Skill** — a repeatable multi-step procedure (author it via the archetypes in this library).
   - **Script** — a mechanical command sequence.
   - **Settings hook** — automation that must run every time.
   - **Memory** — a durable fact/preference across sessions.
   - **Doc update** — architecture / journal / queue.
   - **Permission allowlist** — to stop a recurring prompt for a safe command.

   Verify **tracked-vs-ignored** so "this is now shared" is never a false claim, and don't
   over-engineer — pick the smallest mechanism that lasts.
5. **Confirm which proposals to apply, apply them, don't commit.** Isolate any tracked edits onto a
   dedicated branch so they don't contaminate open work.

## Facts to discover before emitting

- Where durable guidance lives in this project (standing-context file, team rules dir, personal memory)
  and which of those paths are git-tracked vs. ignored.
- The session's verifiable anchors (recent SHAs, PRs, changed files) available at invocation.
- Branch conventions, to name the dedicated branch for tracked edits.

## Principles that especially apply

- **Honesty over optimism** — don't over-claim fault or manufacture findings.
- **Right-home mapping for durable fixes** — map each fix to where it belongs; flag tracked-vs-ignored.
- **Confirm before irreversible / outward actions** — get sign-off on which proposals to apply.
- **Respect standing project constraints** — isolate tracked edits onto their own branch.

## Notes

- Cross-reference siblings: postmortem closes the lifecycle that [start-work](start-work.md),
  implementation, and [commit-gate](commit-gate.md) opened; its fixes may sharpen any sibling's body.
- A postmortem that invents corrections to look thorough is worse than a short, true one.
