# Meta-skill: "run it" / launchers

**Archetype for `/up` and `/up-full` commands.** Use this to author launcher skills whose deliverable
is **the app (or full stack) running as a tracked background task**. Author one launcher per
meaningfully different runtime size (e.g. lightweight UI vs. full stack), not one per service.

Read the [README](../README.md) for the skeleton, header-wrapping, and principles. Author this skill
with [authoring-a-skill-suite](authoring-a-skill-suite.md).

**Top guardrail: never block the turn.** The process launches detached as a tracked background task,
with a readiness check and a documented stop method.

## Generalized steps (the reusable body)

1. **Wrap the launch in a helper script** that runs the server in the foreground (so the harness can
   track it). The skill invokes that script detached. Pass user args through.
2. **Before (re)launching, reconcile what's already running.** Detect port listeners and process
   names and compare against the agent's own background-task list. **Stop only the tasks this agent
   started**; for a matching process the agent did *not* start (a user's other terminal, an orphaned
   port-holder), surface it and ask before killing it — **never kill a process you didn't start silently.** If
   the port is held by something unexpected, surface it and stop rather than guessing.
3. **Confirm readiness honestly — but don't invent a signal.** If the runtime emits a cheap, reliable
   readiness signal, wait for it in the captured output (don't block on the process itself) and report
   the URL(s). If it doesn't (a watcher, a long multi-stage build with no single "ready" line), don't
   block the turn polling for one — launch detached and hand back the task id and stop method, stating
   plainly that readiness wasn't waited on.
4. **Note port conflicts** and which launcher fits which work (lightweight UI vs. full stack), so the
   user picks the right one.

## Facts to discover before emitting

- Build / run / dev-server commands, ports, and URLs (README, `package.json`, `docker-compose`,
  `Procfile`, start scripts).
- The readiness signal in the server's output (a "listening on…" line, a health endpoint).
- Env setup quirks: venv activation, required env vars, secret sourcing (instruction files, setup
  scripts, `.tool-versions`).
- How the target agent tracks background tasks and what its stop method is.
- Whether more than one runtime size exists, which determines how many launchers to emit.

## Principles that especially apply

- **Long-running processes run detached** — this is the defining constraint of the archetype.
- **Confirm before irreversible / outward actions** — restart your own tracked tasks freely, but never
  kill a process you didn't start without asking.
- **Bundle helper scripts** — the launch is deterministic; script it rather than improvising.
- **Respect standing project constraints** — env setup and read-only infra rules go in `## Notes`.
- **Honesty over optimism** — if the readiness signal never appeared, report it rather than claiming
  the app is up.

## Notes

- Cross-reference siblings: [commit-gate](commit-gate.md) verifies against the running app, so it
  should tell the user to start it with this launcher if it isn't up.
- Keep one launcher per distinct runtime size; resist folding everything into a single oversized script.
