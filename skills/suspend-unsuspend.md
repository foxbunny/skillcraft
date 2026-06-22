# Meta-skill: "suspend / unsuspend" — task-switch via a WIP checkpoint

**Archetype for a paired `/suspend` + `/unsuspend` command.** Use this to author the two halves of a
task-switch checkpoint: `/suspend` **parks the current branch as a single throwaway "WIP" checkpoint
commit** (so the user can switch tasks with a clean working tree), and `/unsuspend` **unwinds that
checkpoint** (restoring the working tree to exactly where suspension left it). They are a stash
push/pop pair — authored and documented together because they share one contract.

**Why one file:** the pair depends on a single shared convention — *the exact WIP commit message
`/suspend` writes must equal the one `/unsuspend` detects*. Split across two files, that contract is a
cross-reference an authoring agent can miss, and an agent might emit one half without the other.
Co-located, the contract is unmissable and the pair is emitted as a unit. (Same reasoning by which
[run-it](run-it.md) keeps `/up` and `/up-full` in one file.)

Read the [README](../README.md) for the skeleton, header-wrapping, and principles. Author both halves
with [authoring-a-skill-suite](authoring-a-skill-suite.md).

The git commands shown in parentheses below are the **example VCS** — emit the discovered VCS's
equivalents (see *Facts to discover*); a project on jj/hg has no `--no-verify` or `HEAD~1`, so don't
carry git's literals across verbatim.

**Top guardrail (both halves): a WIP checkpoint is local and disposable — never push it, never treat
it as a real commit, and only ever unwind it with a *soft*, WIP-gated reset.** This is the library's
one *permitted* hook-bypass (contrast the real, gated commit path in [commit-gate](commit-gate.md)):
`/suspend` skips hook checks precisely because the checkpoint is a parking spot the user will reverse,
not a change entering history.

## `/suspend` — park work as a WIP checkpoint

Deliverable: the branch ends in one `WIP` checkpoint commit capturing the whole working state; the
tree is clean and the user can switch tasks.

1. **Confirm there's something to suspend.** If the working tree is clean (nothing staged, unstaged,
   or untracked), **stop and report** "nothing to suspend" — don't create an empty checkpoint.
   (`git status --porcelain` empty → clean.)
2. **Stage everything, including untracked files** — the checkpoint must capture the whole working
   state. (`git add -A`.)
3. **Commit the checkpoint, bypassing hooks**, with the project's WIP message (default `WIP`).
   (`git commit --no-verify -m "WIP"`.) Bypassing hooks is intentional and required — a checkpoint
   must succeed even mid-edit, when lint/tests would fail.
4. **Report the result and the boundary:** the branch now ends in a WIP checkpoint; the working tree is
   clean; the user can switch tasks. Remind them **not to push** this branch and to run `/unsuspend`
   to resume.

## `/unsuspend` — unwind the WIP checkpoint

Deliverable: the checkpoint is gone and the suspended changes are back in the working tree, ready to
resume.

1. **Check the branch tip is a WIP checkpoint.** Read HEAD's commit subject and compare it to the WIP
   convention (default exactly `WIP`). (`git log -1 --pretty=%s`.) If it doesn't match, **stop and
   report** "no WIP checkpoint to unwind" — resetting would destroy a real commit.
2. **Confirm a parent commit exists.** If the WIP checkpoint is the branch's root commit (no parent),
   don't `reset HEAD~1` — report it and offer to simply unstage, so no history is lost.
3. **Soft-reset to the previous commit.** (`git reset --soft HEAD~1`.) This drops the checkpoint commit
   while keeping all its changes in the index — the working state is restored exactly as at suspension.
4. **Report what was restored:** the checkpoint is gone, the prior commit is the tip again, and the
   suspended changes are back (staged). Note the user can unstage them for an unstaged start.

## Facts to discover before emitting

- The exact WIP commit message convention (default `WIP`) — **write it once and use the same string in
  both halves**; this is the contract the whole archetype rests on.
- Whether the repo has pre-commit / commit-msg hooks that would block a mid-edit commit, and the target
  agent's flag for bypassing them (`--no-verify` for git).
- Whether commit signing is enforced — leave signing **on** unless the user says otherwise (bypass
  hooks, not signing).
- Whether the project prefers restored changes left **staged** (soft reset, the default contract) or
  unstaged (a follow-up mixed reset).
- The target agent's git invocation for staging untracked files, reading the HEAD subject, and a
  **soft** reset.

## Principles that especially apply

- **Gate-and-stop discipline** — `/unsuspend`'s WIP-check is a hard gate; refuse on a non-WIP tip, and
  never escalate to `--hard`. `/suspend` stops on a clean tree.
- **Honesty over optimism** — report "nothing to suspend" / "no WIP checkpoint" plainly rather than
  faking a checkpoint or resetting anyway; never imply a WIP commit is real, reviewed, or pushed.
- **Confirm before irreversible / outward actions** — the pair stays reversible and local by design;
  the guardrail is "never push," not "ask before checkpointing."
- **Respect standing project constraints, with the one permitted exception** — hooks are bypassed
  *only* for this disposable checkpoint, never for a real commit.

## Notes

- Cross-reference siblings: pairs with [start-work](start-work.md) when switching to a different task;
  `/unsuspend` is the only supported way to unwind a `/suspend` checkpoint.
- Keep `/suspend` safe to repeat: if HEAD is already a WIP checkpoint, note that rather than
  stacking a second one — one checkpoint per suspension. `/unsuspend` is a safe no-op (with a clear
  message) on any branch whose tip isn't a WIP checkpoint.
- A WIP checkpoint must never reach a shared branch or a PR; if the branch is already pushed, warn the
  user before checkpointing.
