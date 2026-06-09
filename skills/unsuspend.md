# Meta-skill: "unsuspend" / unwind a WIP checkpoint

**Archetype for an `/unsuspend` command.** Use this to author a skill whose deliverable is **the WIP
checkpoint left by [suspend](suspend.md) unwound**, restoring the working tree to exactly where
suspension left it so the user can resume. The boundary: it only ever unwinds a *WIP checkpoint* — it
must never touch a real commit.

Read the [README](../README.md) for the skeleton, header-wrapping, and principles. Author this skill
with [authoring-a-skill-suite](authoring-a-skill-suite.md).

**Top guardrail: verify HEAD is a WIP checkpoint before resetting, and use a *soft* reset only.** If
the branch tip is anything other than the WIP checkpoint, **stop and report** — never reset, never
discard real work. Soft-only means changes come back intact; a hard reset is forbidden here.

## Generalized steps (the reusable body)

1. **Check the branch tip is a WIP checkpoint.** Read HEAD's commit subject and compare it to the
   project's WIP convention (default exactly `WIP`). (`git log -1 --pretty=%s`.) If it doesn't match,
   **stop and report** "no WIP checkpoint to unwind" — there's nothing to do, and resetting would
   destroy a real commit.
2. **Confirm a parent commit exists.** If the WIP checkpoint is the branch's root commit (no parent),
   don't `reset HEAD~1` — instead report it and offer to simply unstage, so no history is lost.
3. **Soft-reset to the previous commit.** (`git reset --soft HEAD~1`.) This removes the checkpoint
   commit while keeping all its changes in the index — the working state is restored exactly as it was
   at suspension.
4. **Report what was restored:** the WIP checkpoint is gone, the prior commit is the tip again, and the
   suspended changes are back (staged). Note that the user can unstage them if they prefer an unstaged
   starting point.

## Facts to discover before emitting

- The exact WIP message convention to match — it must equal what [suspend](suspend.md) writes, or the
  detection in step 1 will silently fail. Keep the pair in lockstep.
- The target agent's git invocation for reading the HEAD subject and performing a **soft** reset.
- Whether the project prefers the restored changes left **staged** (soft reset, as specified) or
  unstaged (a follow-up `git reset` to mixed) — default to staged per the suspend/unsuspend contract.

## Principles that especially apply

- **Gate-and-stop discipline** — the WIP-check in step 1 is a hard gate; refuse on a non-WIP HEAD.
- **Honesty over optimism** — if there's no checkpoint, say so plainly instead of resetting anyway.
- **Confirm before irreversible / outward actions** — soft-only and WIP-gated keeps this safe and
  reversible; never escalate to `--hard`.

## Notes

- Cross-reference siblings: this is the inverse of [suspend](suspend.md) and the only supported way to
  unwind its checkpoint; resuming a task often pairs with [start-work](start-work.md).
- It is intentionally a no-op (with a clear message) on any branch whose tip isn't a WIP checkpoint —
  safe to run speculatively.
