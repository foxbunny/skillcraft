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
5. **For bugs: reproduce, don't reason-only.** Try to capture a repro in the most appropriate manner
   available — a failing test, a deterministic script, or copy-pasteable steps with observed output.
   Forbid talking oneself out of it.
5b. **For bugs: plan to make it impossible, not just fixed.** Once the reproduction pins the root
   cause, design the fix to eliminate the *class* of bug, not only this instance. In the plan, name
   the smallest structural change that would make the failure unrepresentable — push the invalid state
   out of existence (a type/enum/discriminated union instead of a loose flag), guard it at the
   boundary so bad input can't enter, encode the invariant where it's enforced once rather than
   checked everywhere, or delete the code path that allowed it. Also name the regression test that
   locks it shut. If "impossible" is out of
   proportion to the bug (a one-line typo, a copy fix), say so and just fix it — propose the
   prevention, weighed against its cost, don't mandate a refactor.
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
- **Reproduce, don't reason-only** — for the bug path, capture a repro in the most appropriate manner
  available.
- **Fix the class, not the instance** — for the bug path, plan the smallest structural change that
  makes the bug *unrepresentable*, weighed against its cost; don't mandate a refactor for a trivial
  slip.
- **Blast-radius thinking** — map consumers, not just edited lines.
- **Load integrations deliberately, with a fallback chain** — tracker → browser → ask.
- **Honesty over optimism** — if ticket context couldn't be fetched, say so.

## Notes

- Cross-reference siblings: hand off to implementation, then [commit-gate](commit-gate.md) when done;
  mention [run-it](run-it.md) if exploring the bug needs the app running.
- Echo the repo's standing constraints (env setup, off-limits dirs) so the skill self-enforces.
