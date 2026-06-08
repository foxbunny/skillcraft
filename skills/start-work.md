# Meta-skill: "start work" / prep

**Archetype for a `/prep <ticket>` command.** Use this to author a skill whose deliverable is **a
ready workspace + an agreed plan, with no code written yet**. The boundary matters: this skill
prepares and proposes; it does not implement.

Read the [README](../README.md) for the skeleton, header-wrapping, and principles. Author this skill
with [authoring-a-skill-suite](authoring-a-skill-suite.md).

**Top guardrail: end awaiting plan sign-off. Do not start writing code inside this skill** — the
deliverable is the plan, not the change.

## Generalized steps (the reusable body)

1. **Normalize the ticket id.** Parse it from the argument; if missing, ask for it.
2. **Pull ticket context** via a fallback chain: tracker integration → browser → ask the user.
   Summarize the ticket and classify it **bug vs. feature** — the two diverge downstream.
2b. **Validate the work still serves the goal — don't build on autopilot.** In one line, say *why this
   item still earns its build right now*: is the problem real here, and does it move the project's goal
   forward? If it solves a non-problem or fights the project's intent, surface that and propose
   dropping/deferring it instead of preparing it. The plan is a living document, not a contract.
3. **Prepare the workspace.** Refuse on a dirty working tree (stop and report). Sync the main branch.
   Follow the repo's branching model: on a branch-per-ticket repo, detect an existing branch for this
   ticket and report its provenance / open-PR status / why it stalled, else create one per the naming
   convention; on a **trunk-based** repo, stay on `main` and branch only for genuinely exploratory,
   multi-hypothesis work (named for the work, e.g. `try-<slug>`).
4. **Explore the affected code.** Map the **blast radius** — every consumer of each symbol/route/API
   the change will touch, not just the obvious file. Trace history with `git log` / `git blame`.
5. **For bugs: reproduce, don't reason-only.** Produce a concrete, re-runnable reproduction plus
   copy-pasteable steps. Forbid talking oneself out of it.
6. **End awaiting plan sign-off**, using the agent's plan/confirm mechanism.

## Facts to discover before emitting

- Issue tracker + id format (branch names, commit messages, PR templates, the user).
- **Branching model** — branch-per-ticket vs. trunk-based — and the naming convention (`git log
  --oneline -20`, existing branches, CONTRIBUTING).
- Which tracker/browser/MCP integrations are available, for the fallback chain.
- Repo conventions for "dirty tree" handling and the name of the main branch.

## Principles that especially apply

- **Gate-and-stop discipline** — refuse on a dirty tree; don't paper over a missing ticket.
- **Validate the work still serves the goal** — re-justify the item before preparing it.
- **Reproduce, don't reason-only** — for the bug path (see [capture-repro](capture-repro.md)).
- **Blast-radius thinking** — map consumers, not just edited lines.
- **Load integrations deliberately, with a fallback chain** — tracker → browser → ask.
- **Honesty over optimism** — if ticket context couldn't be fetched, say so.

## Notes

- Cross-reference siblings: for the bug path, fire [capture-repro](capture-repro.md) to lock in a
  failing artifact; hand off to implementation, then [commit-gate](commit-gate.md) when done; mention
  [run-it](run-it.md) if exploring the bug needs the app running.
- Echo the repo's standing constraints (env setup, off-limits dirs) so the skill self-enforces.
