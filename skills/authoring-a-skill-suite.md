# Meta-skill: authoring a skill suite

**This is the entry-point meta-skill.** It tells an AI agent how to turn the archetypes in this
library into a concrete, project-specific skill suite for whichever target agent the project uses. It
produces *skill files*, not application code.

Read the [README](../README.md) first for the two primitives, the activation taxonomy, the portable
skeleton, the agent-mapping table, and the universal design principles. This document is the
*procedure* that consumes all of those.

**Top guardrail: never guess a project fact.** A wrong command or path baked into a skill is worse
than a gap. When a fact can't be derived from the repo, **ask the user** before writing it.

## 1. Identify the target agent(s)

Look for existing customization directories to infer the agent in play: `.claude/`, `.cursor/`,
`.github/`, `.windsurf/`, `.gemini/`, `AGENTS.md`, `.roomodes`. If none exist or several do, **ask the
user** which agent(s) to target. This picks the row(s) in the README's agent-mapping table. If
multiple agents are in play, write each skill body once and wrap a header per agent — the body prose
is reusable verbatim.

## 2. Choose the skills

Confirm which archetypes the user wants. Default to the lifecycle set for a dev repo:
[start-work](start-work.md) → [run-it](run-it.md) → [commit-gate](commit-gate.md) →
[postmortem](postmortem.md). Layer in the supporting archetypes where the project calls for them:
[capture-repro](capture-repro.md) for bug-heavy work, [invariant-audit](invariant-audit.md) when the
project has hard rules a diff can violate, [session-journal](session-journal.md) +
[task-queue](task-queue.md) for durable
cross-session record-keeping, and [suspend-unsuspend](suspend-unsuspend.md) for fast task-switching
via a throwaway WIP checkpoint. For projects that ship work outward, add [open-pr](open-pr.md) (push
and open a PR on sign-off) and [repo-housekeeping](repo-housekeeping.md) (sweep merged branches); for
review-heavy work add [adversarial-skeptic](adversarial-skeptic.md) (red-team a change or a decision)
and [walkthrough](walkthrough.md) (explain a change in depth). Add or drop archetypes to fit; the same
skeleton extends to `/review`, `/verify`, `/deploy`, etc.

The discovery-heavy archetypes — [open-pr](open-pr.md) and [repo-housekeeping](repo-housekeeping.md)
especially — are where the **authoring-time discovery** model (see the README) earns its keep: infer
the merge style, PR conventions, tracker linkage, and VCS from the repo, propose them, and bake the
*confirmed* answers into the instance so the running skill never re-discovers them.

Before adopting any pattern, run the **action vs. standard test** (see the README): if the pattern
bundles a *standard* with an *action* (audit an invariant, record a metric, reconcile a queue), the
action becomes the skill and the standard goes into standing context as a rule the skill references —
this library only authors the skills.

## 3. Run the discovery pass

Fill a fact sheet from the repo — **don't guess**. Each archetype lists the specific facts it needs;
this is the union of them:

| Fact needed | Where to find it |
|---|---|
| Test / lint / typecheck commands | `package.json` scripts, `Makefile`, `pyproject.toml`, CI workflows, README, instruction files |
| Build / run / dev-server commands + ports + URLs | README, `package.json`, `docker-compose`, `Procfile`, start scripts |
| Env setup quirks (venv, env vars, secret sourcing) | instruction files, setup scripts, `.tool-versions` |
| Branch + commit-message conventions | `git log --oneline -20`, existing branches, CONTRIBUTING, commit-lint config |
| VCS in use + whether deletes are recoverable | repo dir (`.git` / `.jj` / `.hg`), the user |
| Merge style (squash / merge / rebase) + PR description conventions | history shape (`git log --graph --oneline`), one or two recent merged PRs, host repo settings |
| PR host CLI + auth account/scope + fork-vs-origin topology | `git remote -v`, `gh`/`glab` presence, the user |
| Issue tracker + id format (and whether the project tracks at all) | branch names, commit messages, PR templates, the user |
| Editing-surface rules (fair-game vs. off-limits dirs) | instruction files, code owners, existing rules |
| Hard constraints / "never do X" (invariants an audit enforces) | instruction files, existing rules, the user |
| North-star metric + ledger location + regression policy | README, docs, the user |
| Durable-record conventions (journal, task queue) + their file paths | `docs/`, existing logs, instruction files |
| Available integrations (tracker / browser / MCP) | the agent's tool list; ask the user |

When a fact can't be derived, **ask**.

## 4. Write each skill

Take the archetype body from its meta-skill document, replace every placeholder with a discovered
fact, inject the relevant universal design principles, and wrap the README agent-mapping header for the
target. Add helper scripts for any long-running or deterministic step (a launcher especially).

## 5. Put invariants in standing context

Move the repo's hard constraints into the agent's always-on file (`CLAUDE.md` / `AGENTS.md` / etc.) so
every skill inherits them instead of each skill re-stating them. Skills then reference the standing
context.

## 6. Cross-link the suite

Each skill references its siblings by command name (e.g. commit-gate tells the user to start the app
with the run-it launcher if it isn't up). The suite is a workflow, not isolated tools.

## 7. Sanity-check

- name / filename / directory match.
- description stands alone and carries concrete trigger phrases.
- body has the top guardrail + numbered ordered steps + a `## Notes` section.
- every command, path, and script the skill references **actually exists in the repo**.

## 8. Hand back

List what was created, note where each file lives and whether it's **local-only vs. team-shared** (and
what that implies), and suggest the user try one.

## Notes

- Re-derive commands, paths, conventions, constraints, and header syntax **per project and per agent**.
  Never carry another repo's or another agent's specifics across.
- Prefer asking over guessing — a lying skill is worse than no skill.
- Keep each skill focused on one job; let the suite compose. Resist the mega-skill.
- Skills are cheap to iterate, especially in local-only dirs — refine wording after the first real run.
