# Meta-skill: open a pull request

**Archetype for a `/create-pr` (push-and-open-PR) command.** Use this to author a skill whose
deliverable is **a pushed branch and an opened pull/merge request, created only on explicit
sign-off**. The boundary: it publishes a PR (an outward-facing action) and optionally records its
number back into a changelog/tracker; it does **not** merge, and it assumes the change is already
committed (run the [commit-gate](commit-gate.md) command first). This is the deliberate next step that
commit-gate intentionally leaves out.

Read the [README](../README.md) for the skeleton, header-wrapping, and principles. Author this skill
with [authoring-a-skill-suite](authoring-a-skill-suite.md).

**Top guardrail: a PR is public — never create it until the user has approved the title and body.**
Prepare everything, show it, and create only on a clear yes.

## Authoring-time discovery is the point

Off-the-shelf PR commands hardcode one project's answers: squash vs merge, the commit-message shape,
what a PR description must contain, whether to push to a fork or to origin, which tracker links to
which field. This archetype instead **discovers those conventions when the skill is authored,
proposes them to the user, and bakes the resolved answers into the emitted instance** — so the
running skill already knows them and never re-asks at PR time. Discover by inspecting evidence, not by
guessing:

- **Merge style** (squash / merge / rebase) — infer from history shape (are there merge commits? is
  every feature a single commit on the trunk?) and from host repo settings if visible. This decides
  whether the skill keeps the branch as one commit.
- **Commit-message format** — sample recent subjects/bodies: Conventional Commits? a ticket prefix? a
  changelog footer? a "no co-author trailer" rule?
- **PR/MR description conventions** — open one or two recently merged PRs and read their structure:
  required sections, a checklist, a `Closes #123` linking line, screenshots-required, whether a
  generated-by footer is wanted or unwanted.
- **Target + remote setup** — the base branch, branch-naming rules, and whether contributions go
  through a **fork** (push to `origin`, PR `upstream:base ← fork:branch`) or **directly to origin**.
- **Tracker & changelog linkage — and whether the project tracks at all.** Some projects backfill the
  PR number into a changelog entry or update a ticket; many do neither. Discover which, and only
  emit the backfill step if the project actually does it. Never invent a tracking step.

Present what you inferred as a proposed default ("history looks squash-merged with Conventional
Commits; PRs use a Summary/Test-plan template; contributions go through a fork — use these?") and let
the user confirm or override. The confirmed answers become fixed instructions in the instance; at
runtime the skill follows them without re-discovery. (See the README's note on authoring-time
discovery as what separates a meta-skill recipe from a static skill definition.)

## Generalized steps (the reusable body — with the discovered answers baked in)

1. **Preconditions.** On a feature branch (not the trunk), named per the project's rule; working tree
   clean and the change committed in the project's message format — if uncommitted, stop and point to
   the commit command. The PR host CLI is installed and authenticated with the right account and
   scope; if not, stop and ask the user to authenticate. *(If the project tracks: confirm the
   changelog/ticket entry exists, with the PR-number slot still to be filled.)*
2. **Sync and push.** Fetch the integration remote, confirm the branch sits on top of the current
   base, and rebase if behind — keeping the change in the project's merge style (one commit for a
   squash project). If the rebase conflicts **only** in a generated dependency lockfile, resolve it
   deterministically — take the base's lockfile and regenerate via the project's install command,
   never hand-merge — then continue; for **any source-file conflict, stop and hand back to the user**
   (don't auto-resolve, `--skip`, or `--abort` on their behalf). Push to the discovered remote
   (`origin`, or the fork), force-with-lease only when the branch already exists and was
   amended/rebased.
3. **Draft the PR, then wait for sign-off.** Title and body in the project's discovered convention
   (sections, linking line, footer policy), base ← head set per the discovered setup. **Show the
   title and body and wait for explicit approval** before the next step.
4. **Create.** Run the host's create command with the approved title/body and the resolved base/head;
   capture the PR number and URL.
5. **Backfill the PR number — only if the project tracks it.** Add the PR reference to the
   changelog/ticket entry, amend the commit, and force-with-lease (the PR's own diff should carry its
   number). Skip this step entirely for projects that don't track.
6. **Report — and don't conflate a clean review with a green PR.** Give the PR URL and mergeable
   state. A passing automated review is not the same as passing CI: **separately confirm the host's CI
   checks concluded successfully** before reporting done, and flag any check still pending past a sane
   threshold as *hung, not slow* — treat a newly-added or changed CI step as unverified until observed
   green in a real run. Don't poll checks to completion unless asked. If the skill runs a review-fix
   loop, give it two stopping conditions: success after **N consecutive clean passes** (one stochastic
   pass isn't proof) and a hard **limit of M find-again rounds** — stop and hand back rather
   than loop forever.

## Facts to discover before emitting

- All of the **authoring-time discovery** list above: merge style, commit-message format, PR
  description conventions, base branch + naming, fork-vs-origin setup, and tracker/changelog
  linkage (including *whether the project tracks at all*).
- The PR host and its CLI/API (`gh`, `glab`, etc.), the auth account and required scope, and the
  absolute path/invocation if PATH is unreliable.
- The integration remote name(s) (`upstream`/`origin`) and how the branch relates to them.
- The fallback when the host CLI is unavailable (e.g. hand the user a compare URL to submit).

## Principles that especially apply

- **Confirm before irreversible / outward actions** — creating a PR is outward-facing and is gated on
  approval of the exact title and body; merging is out of scope entirely.
- **Honesty over optimism** — report the real mergeable/CI state; don't imply checks passed if they
  weren't observed.
- **Load integrations deliberately, with a fallback chain** — acquire the host CLI/auth first; degrade
  to a compare URL or asking the user.
- **Respect standing project constraints** — follow the discovered message/PR conventions exactly;
  echo the "never merge from this skill" rule in `## Notes`.

## Notes

- **Never merge from this skill** — review and merge are the maintainers' (or a separate command's)
  job.
- Pushing and PR creation are the deliberate outward steps [commit-gate](commit-gate.md) leaves out;
  this skill is their home. It assumes commit-gate (or its instance) already produced the commit.
- Keep the tracker/changelog backfill **conditional** — its presence in the emitted skill should
  reflect what the discovery pass actually found, not a default.
