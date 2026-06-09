# Meta-skill: "suspend" / park work as a WIP checkpoint

**Archetype for a `/suspend` command.** Use this to author a skill whose deliverable is **the current
branch parked as a single throwaway "WIP" checkpoint commit**, so the user can switch to another task
with a clean working tree and resume later. The boundary: this is a **local checkpoint, not a real
commit** — it captures *everything* (staged, unstaged, and untracked) and is meant to be unwound by
[unsuspend](unsuspend.md).

Read the [README](../README.md) for the skeleton, header-wrapping, and principles. Author this skill
with [authoring-a-skill-suite](authoring-a-skill-suite.md).

**Top guardrail: a WIP checkpoint is local and disposable — never push it, and never treat it as a
real commit.** This is the library's one *sanctioned* hook-bypass (see [commit-gate](commit-gate.md)
for the real, gated commit path): the checkpoint skips hook checks precisely because it is a
stash-like parking spot the user will reverse with [unsuspend](unsuspend.md), not a change entering
history.

## Generalized steps (the reusable body)

1. **Confirm there's something to suspend.** If the working tree is clean (nothing staged, unstaged,
   or untracked), **stop and report** "nothing to suspend" — don't create an empty checkpoint.
   (`git status --porcelain` empty → clean.)
2. **Stage everything, including untracked files** — the checkpoint must capture the whole working
   state. (`git add -A`.)
3. **Commit the checkpoint, bypassing hooks**, with the project's WIP message (default `WIP`).
   (`git commit --no-verify -m "WIP"`.) Bypassing hooks is intentional and required here — a checkpoint
   must succeed even when the tree is mid-edit and would fail lint/tests.
4. **Report the result and the boundary:** the branch now ends in a WIP checkpoint; the working tree is
   clean; the user can switch tasks. Remind them **not to push** this branch and to run
   [unsuspend](unsuspend.md) to resume.

## Facts to discover before emitting

- The exact WIP commit message convention (default `WIP`) — it must match what
  [unsuspend](unsuspend.md) detects, so keep the two in lockstep.
- Whether the repo has pre-commit / commit-msg hooks that would otherwise block a mid-edit commit, and
  the target agent's flag for bypassing them (`--no-verify` for git).
- Whether commit signing is enforced — leave signing **on** unless the user says otherwise (bypass
  hooks, not signing).
- The target agent's git invocation and how it stages untracked files.

## Principles that especially apply

- **Honesty over optimism** — report a clean tree as "nothing to suspend" rather than faking a
  checkpoint; never imply the WIP commit is real, reviewed, or pushed.
- **Confirm before irreversible / outward actions** — this stays *reversible and local* by design; the
  guardrail is "never push," not "ask before committing."
- **Respect standing project constraints, with the one sanctioned exception** — hooks are bypassed
  *only* for this disposable checkpoint, never for a real commit.

## Notes

- Cross-reference siblings: [unsuspend](unsuspend.md) is the inverse and the only supported way to
  unwind the checkpoint; pairs with [start-work](start-work.md) when switching to a different task.
- Keep it idempotent in spirit: if HEAD is already a WIP checkpoint, note that rather than stacking a
  second one — one checkpoint per suspension.
- A WIP checkpoint must never reach a shared branch or a PR; if the branch is already pushed, warn the
  user before checkpointing.
