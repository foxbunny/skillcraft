# Meta-skill: "run it" / launchers

**Archetype for `/up` and `/up-full` commands.** Use this to author launcher skills whose deliverable
is **the app (or full stack) running as a tracked background task**. Author one launcher per
meaningfully different runtime footprint (e.g. lightweight UI vs. full stack), not one per service.

Read the [README](../README.md) for the skeleton, header-wrapping, and principles. Author this skill
with [authoring-a-skill-suite](authoring-a-skill-suite.md).

**Top guardrail: never block the turn.** The process launches detached as a tracked background task,
with a readiness check and a documented stop method.

## Generalized steps (the reusable body)

1. **Wrap the launch in a helper script** that runs the server in the foreground (so the harness can
   track it). The skill invokes that script detached. Pass user args through.
2. **Wait for a readiness signal** in the captured output — don't block on the process itself. Report
   the URL(s), the background task id, and the stop method.
3. **Note port conflicts** and which launcher fits which work (lightweight UI vs. full stack), so the
   user picks the right one.

## Facts to discover before emitting

- Build / run / dev-server commands, ports, and URLs (README, `package.json`, `docker-compose`,
  `Procfile`, start scripts).
- The readiness signal in the server's output (a "listening on…" line, a health endpoint).
- Env setup quirks: venv activation, required env vars, secret sourcing (instruction files, setup
  scripts, `.tool-versions`).
- How the target agent tracks background tasks and what its stop method is.
- Whether more than one runtime footprint exists, which determines how many launchers to emit.

## Principles that especially apply

- **Long-running processes run detached** — this is the defining constraint of the archetype.
- **Bundle helper scripts** — the launch is deterministic; script it rather than improvising.
- **Respect standing project constraints** — env setup and read-only infra rules go in `## Notes`.
- **Honesty over optimism** — if the readiness signal never appeared, report it rather than claiming
  the app is up.

## Notes

- Cross-reference siblings: [commit-gate](commit-gate.md) verifies against the running app, so it
  should tell the user to start it with this launcher if it isn't up.
- Keep one launcher per distinct runtime footprint; resist folding everything into a single mega-script.
