# Meta-skill: repo housekeeping

**Archetype for a `/housekeeping` command.** Use this to author a skill whose deliverable is **merged
local branches deleted, stale unmerged branches flagged for the user's decision, the trunk synced to
upstream, and (optionally) older shipped backlog items condensed into a permanent archive**. The
boundary: it touches only local branch refs and the project's own backlog files — it never pushes,
never force-pushes, and never deletes unmerged work without explicit sign-off.

Read the [README](../README.md) for the skeleton, header-wrapping, and principles. Author this skill
with [authoring-a-skill-suite](authoring-a-skill-suite.md).

**Top guardrail: a branch is "merged" only when its *content* is in upstream — never trust a
heuristic.** Squash-merges, PR renames, and upstream advancing mid-session all defeat subject-line
matching, `git cherry`, and ahead/behind counts. The only reliable test is that **every file the
branch changed is identical to the trunk** (excluding files that always drift, like a changelog).

## The technique (and what to discover first)

The core idea is **content-based merge detection**, learned from real failures:

- **Squash + rename hides merges.** A branch merged as a renamed PR won't match by subject and
  `git cherry` won't flag it. Diffing content catches it; nothing else does.
- **Upstream moves while you work.** Branches merged *after* your first fetch look unmerged until you
  re-fetch. Always fetch fresh at the start, and **re-verify the remaining branches after fast-forwarding the
  trunk** — pulling new commits can reveal more merges.
- **Some files always differ** (a changelog accumulates unrelated upstream entries). Exclude them from
  the content check or every branch looks unmerged.

This technique is expressed in a specific VCS's commands, so it depends on one discovery: **detect
which VCS the project uses before assuming any branch mechanics.** The content-merged idea generalises
across git / jj / hg, but the exact commands (merge-base, ancestor test, content diff, ref deletion,
reflog recovery) do not — discover the VCS at authoring time and emit the right ones. For a project on
a tool without recoverable ref deletion, tighten the gate accordingly.

## Generalized steps (the reusable body)

1. **Fetch fresh and sync the trunk.** Fetch all integration remotes with prune — mandatory; a stale
   snapshot misclassifies merged branches. If the trunk is clean and behind, fast-forward it so every
   comparison uses current truth. Compare against the *upstream* trunk throughout (the canonical
   source), not the local trunk — they agree only when freshly synced.
2. **Classify every branch by content.** For each branch (skip the trunk), against its merge-base:
   it's **merged** if it's an ancestor of the trunk **or** every changed file (minus the
   always-changing files) is byte-identical to the trunk; **unmerged** otherwise. For unmerged
   branches compute age and mark **stale** past a threshold (default ~3 months idle). Present a table:
   merged (with the landing PR # if found), unmerged-active, unmerged-stale (with age).
3. **Delete merged branches.** This is the deliverable and is recoverable where the VCS supports it,
   so proceed once the list is shown — but **record each ref's id first** for recovery, then delete
   with the force-delete form (squash/rebase-merged branches aren't ancestors, so the safe-delete form
   refuses them even though their content is in the trunk — that's exactly why the check is
   content-based). Never delete the checked-out branch.
4. **Flag stale branches — do not auto-delete.** Stale branches hold unmerged work. List them with
   ages and **stop for explicit per-branch (or per-set) sign-off** before any deletion. This is the
   one place the skill waits on the user. Record ids before deleting any the user approves.
5. **Re-verify the remaining branches.** After the trunk fast-forward in step 1 pulled new commits, re-run the
   content check on every remaining branch — a branch can have merged in exactly those new commits.
   This is how the last unmerged branch is caught. Delete any newly-merged ones.
6. **(Optional) Condense shipped backlog items into a permanent archive.** If the project keeps a
   working backlog file, move *older* shipped items out of it into a compact, append-only archive
   file — confirmed shipped against the same authority the start-work command uses (e.g. the PR
   appearing in the upstream changelog). Condense each to a fixed field set (date, PR #, what, why,
   before/after) pulled from existing notes; **don't invent** any field the source doesn't support —
   leave it blank and say so. This *moves* information (recoverable from history), never drops it.

Offer an extended sweep behind individual confirms (gone-remote branches, leftover WIP checkpoints,
dangling stashes, local-only tags) but stay clear of large-scale destructive actions (no gc/prune, no
reflog expiry, no touching build artifacts).

## Facts to discover before emitting

- **The VCS in use** (git / jj / hg / other) and its commands for: fetch+prune, fast-forward,
  merge-base, ancestor test, content diff, ref id capture, force-delete, and reflog/recovery —
  including **whether deletion is recoverable** (which sets how aggressive step 3 may be).
- The **trunk branch name** and the integration remote(s) (`upstream`/`origin`), and which is
  canonical.
- The **always-changing files** (changelog or generated files that accumulate upstream entries) so
  the content check ignores them.
- The **staleness threshold** the user wants.
- Whether the project keeps a **working backlog + archive file** (and their paths and entry shape),
  and the **authority** that confirms an item shipped — cross-reference [start-work](start-work.md)
  and [task-queue](task-queue.md). Emit step 6 only if such files exist.

## Principles that especially apply

- **Confirm before irreversible / outward actions** — merged deletes proceed after showing the list
  (recoverable); stale/unmerged deletes never happen without explicit sign-off; nothing is ever
  pushed.
- **Honesty over optimism** — print recovery ids before every delete; leave unsupported archive
  fields blank rather than inventing them.
- **Append-only history** — the archive is append-only and the condense step moves rather than drops
  information.
- **Respect standing project constraints** — don't second-guess the WIP checkpoints owned by
  [suspend-unsuspend](suspend-unsuspend.md); surface them, don't delete them.

## Notes

- **Recovery is not optional:** every delete records the ref id first, so a mistaken removal is
  recoverable wherever the VCS supports it.
- **Siblings:** [start-work](start-work.md) does the lightweight per-session backlog reconcile;
  this skill does the heavier periodic branch sweep and archival. [suspend-unsuspend](suspend-unsuspend.md)
  owns WIP checkpoints — leave them alone here.
- Keep it a **thin maintenance skill** — its value is the content-based merge check and the
  don't-delete-unmerged gate, not complexity.
