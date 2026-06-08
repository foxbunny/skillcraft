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
5. **Propose a commit message** in the repo's convention, then get **explicit sign-off** before
   committing. Don't push.

## Facts to discover before emitting

- Test / lint / typecheck commands (`package.json` scripts, `Makefile`, `pyproject.toml`, CI, README).
- Commit-message convention (`git log --oneline -20`, CONTRIBUTING, commit-lint config).
- Whether hooks run on commit and what they enforce (so the skill respects rather than skips them).
- How to run/reach the app for live verification (cross-reference [run-it](run-it.md)).

## Principles that especially apply

- **Gate-and-stop discipline** — stop on any red gate.
- **Confirm before irreversible / outward actions** — commit only after sign-off; push is separate.
- **Blast-radius thinking** — re-check consumers, not just edited lines.
- **Honesty over optimism** — state which criteria were verified live vs. via tests, and which were
  skipped.
- **Respect standing project constraints** — never bypass hooks; echo the repo's hard rules in `## Notes`.

## Notes

- Cross-reference siblings: tell the user to start the app with [run-it](run-it.md) if it isn't up
  before live verification; follows the implementation that [start-work](start-work.md) set up.
- Keep push as a deliberate, separate action so "committed" never implies "pushed."
