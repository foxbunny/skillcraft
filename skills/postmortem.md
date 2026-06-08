# Meta-skill: "learn from it" / postmortem

**Archetype for a `/postmortem` command.** Use this to author a skill whose deliverable is **durable,
honest improvements distilled from a finished session**. The boundary: it proposes and applies
*guidance/rule* changes; it does not commit them into open work.

Read the [README](../README.md) for the skeleton, header-wrapping, and principles. Author this skill
with [authoring-a-skill-suite](authoring-a-skill-suite.md).

**Top guardrail: don't manufacture findings or over-claim fault.** Distinguish real corrections from
plain directives; ground every claim in a verifiable anchor.

## Generalized steps (the reusable body)

1. **Recap with verifiable anchors** — SHAs, PRs, files. No vague "we did some work."
2. **Scan for every friction signal** and capture each as *what happened → why it cost time → the
   fix*. Distinguish genuine corrections from ordinary directives; don't invent findings. Signals to
   look for: user corrections / "no, actually…"; rework or anything done twice; repeated manual steps a
   script could do; failed or retried commands and setup snags; permission prompts that recur for safe
   commands; context that had to be rediscovered; slow/uncertain decisions a standing rule could settle.
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
