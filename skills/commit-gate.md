# Meta-skill: "finish it" / commit gate

**Archetype for a `/commit` command.** Use this to author a skill whose deliverable is **a verified
change committed only on explicit approval**. The boundary: it commits, it does **not** push — pushing
is a separate, explicit step.

Read the [README](../README.md) for the skeleton, header-wrapping, and principles. Author this skill
with [authoring-a-skill-suite](authoring-a-skill-suite.md).

**Top guardrail: stop on red and never bypass hooks.** Do not commit past a failing test, lint, or
typecheck, and do not propose a commit until the user has signed off on the message.

## Generalized steps (the reusable body)

1. **Recover acceptance criteria** from the conversation + the diff; write them back as a checklist so
   the user can see what's being verified.
2. **Map scope of impact** — a blast-radius list of *other* behaviors to re-check, not just the edited
   lines.
3. **Verify against the running app.** Exercise the criteria **and** the blast radius live; lean on
   tests for paths that can't be reached live — and **say which** were covered by tests vs. live.
4. **Run the full relevant suite** — test + lint + typecheck, not just the nearest file. Stop on red.
   Never bypass hooks.
5. **Scan the diff for review-class issues — as flags, not gates.** Before proposing the message,
   catch the classes of problem the project's own review rules target, so they don't surface a review
   round later. Surface the specific lines with a recommendation; **don't auto-rewrite, and don't
   block the commit on them** — the user decides (re-run the suite after any change they accept).
   Three high-value, broadly-applicable classes:
   - **Comment cross-references that will rot** — an added comment that names other code (a function,
     file, route-name string, another module's flow). Keep the genuine "why," strip the named pointer
     that silently decays into a lie. Also flag comments that merely restate the code or have gone
     stale after an edit.
   - **Test isolation leaks** — global state mutated and not restored (module globals, env vars,
     module registries) so a test passes alone yet breaks a sibling; mocks whose shape doesn't mirror
     the real state. Run a new test alone *and* beside a sibling that imports the same real modules.
   - **Silent error-swallowing** — an added empty `catch` / `except …: pass` that drops an error
     without logging, especially when a sibling path in the same diff *does* log (the inconsistency is
     the giveaway).
   For a **non-trivial logic diff, dispatch the project's own review/detector agents** (or a small
   fan-out of adversarial reviewers — see [adversarial-skeptic](adversarial-skeptic.md)) over the
   staged diff before proposing the message — your own read has blind spots a green suite won't cover.
   **Author each detector as a read-only, single-purpose agent that sees only the diff slice** — never
   your transcript or the wider refactor — with its reviewing model **pinned in the agent's own
   definition** so dispatch can't silently downgrade to a cheaper default. Have it emit findings as a
   structured list (`file:line`, verbatim quote, one-line why, one-line minimal fix) with no
   prose, charge it to *flag every candidate and let the parent verify*, and require it to **return an
   explicit empty result rather than narrating "looks fine."** Pair the structured per-concern
   detectors with one free-form "catch what the others miss" pass whose categories are deliberately
   not enumerated.
   Each agent sees only a diff slice, so **you are the validation layer**: give every candidate its
   own verdict + a one-line citation of the rule or upstream code that settles it, and never act on an
   untagged finding. **Expect a high false-positive rate (commonly 30–50%)** — "apply just to be safe"
   is how a green review *introduces* a regression. Process every candidate to a verdict ("the rest
   look minor" is a process miss, not a judgement), never bundle a real fix into a collective "these
   look like minor style" dismissal, fix the real ones, and re-run the gates. A genuinely trivial diff
   may skip the dispatch — say so rather than implying it ran.
6. **Propose a commit message** in the repo's convention, then get **explicit sign-off** before
   committing. Don't push.

## Facts to discover before emitting

- Test / lint / typecheck commands (`package.json` scripts, `Makefile`, `pyproject.toml`, CI, README).
- Commit-message convention (`git log --oneline -20`, CONTRIBUTING, commit-lint config).
- Whether hooks run on commit and what they enforce (so the skill respects rather than skips them).
- The project's **own review-checklist rules and any detector/review subagents** — so the
  diff-quality scan (step 5) is grounded in the repo's standards, not generic taste — and which diff
  classes they target.
- How to run/reach the app for live verification (cross-reference [run-it](run-it.md)).

## Principles that especially apply

- **Gate-and-stop discipline** — stop on any red gate.
- **Confirm before irreversible / outward actions** — commit only after sign-off; push is separate.
- **Blast-radius thinking** — re-check consumers, not just edited lines.
- **Honesty over optimism** — state which criteria were verified live vs. via tests, and which were
  skipped; if the detector pass was skipped as trivial, say so rather than implying it ran.
- **Ground quality flags in the repo's own rules, and keep them flags** — the step-5 scan recommends
  and the user decides; only red gates (failing tests/lint/typecheck) block the commit. Verify every
  subagent finding before reacting — expect a high (commonly 30–50%) false-positive rate, give each
  finding its own tagged verdict, and never bundle a real fix into a blanket "minor" dismissal.
- **Respect standing project constraints** — never bypass hooks; echo the repo's hard rules in `## Notes`.

## Notes

- Cross-reference siblings: tell the user to start the app with [run-it](run-it.md) if it isn't up
  before live verification; follows the implementation that [start-work](start-work.md) set up.
- Keep push as a deliberate, separate action so "committed" never implies "pushed."
- This is the *real* commit path and never bypasses hooks. The only permitted hook-bypass is the
  disposable, never-pushed WIP checkpoint in [suspend-unsuspend](suspend-unsuspend.md); don't conflate
  the two.
