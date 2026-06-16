# Skillcraft — meta-skills for AI-first development

Skillcraft is a library of **meta-skills**: high-level, project-agnostic, agent-neutral descriptions
of reusable "skills" for AI coding agents. A meta-skill is not a runnable skill file. It is the
*recipe an agent reads to author* a concrete, project-specific skill — tailored to one repo's
commands, conventions, and the target agent's file format.

This repository is written **for AI agents to peruse, not for human reading**. An agent working in a
project should:

1. Read this README for the universal model and design principles that apply to every skill.
2. Pick the relevant meta-skill(s) from [`skills/`](skills/).
3. Run the discovery pass against the project, fill the archetype's placeholders with real facts, and
   emit a concrete skill file in the target agent's format.

The point of the library is that the **structure and principles are portable; the commands, paths,
conventions, and header syntax are not** — those get re-derived per project and per agent, every
time. Never carry one repo's or one agent's specifics into another.

---

## Why "meta"?

Different agents call reusable-customization artifacts different things — Claude Code "Agent Skills",
Cursor "Rules & Commands", Copilot "instructions & prompt files", Windsurf "Rules & Workflows",
Gemini CLI "custom commands", Codex "AGENTS.md & prompts", Roo Code "modes". They are one idea with a
shared structure. A meta-skill captures that shared structure once, so an agent can project it onto
whichever surface the current project targets.

The body prose of a skill is reusable verbatim across agents; only the header and argument syntax
change. So the meta-skills here describe the **portable body** and tell the authoring agent how to
**wrap the per-agent header** at emit time.

---

## Authoring-time discovery — what makes a recipe, not a definition

This is the single most important distinction in the library. An **off-the-shelf skill definition** is
a finished file with one project's facts hardcoded — its commands, its merge style, its tracker, its
paths. Copy it into a different repo and it lies: it references a test command that doesn't exist, a
fork that isn't there, a changelog the project doesn't keep. A **meta-skill recipe** ships no facts.
It ships the **portable body** plus a **discovery pass**: instructions for the authoring agent to read
the target repo, *infer the project's actual conventions from evidence* (history shape, recent merged
PRs, config, instruction files), **propose them to the user, and bake the confirmed answers into the
emitted skill.**

The consequence that matters: **discovery runs once, at authoring time — never at every invocation.**
The resolved conventions become fixed instructions inside the instance, so the running skill already
knows them and doesn't re-derive or re-ask. Discover → propose → defer → **bake in**, then the skill
just executes. Two corollaries every archetype here honors:

- **Infer from what's observable, but the user owns the final call.** Inspect the repo to propose a
  default; never silently apply an inferred convention. The user confirms or overrides, and *that* is
  what gets written into the instance. (See `/open-pr` discovering squash-vs-merge and PR-description
  conventions; `/housekeeping` detecting which VCS the project uses.)
- **Don't bake in what the project doesn't do.** Conditional steps (a changelog backfill, a ticket
  link, an archive file) are emitted *only* when discovery finds the project actually does them.
  Absence is a finding too.

So the test for whether something belongs in this library: if you can write it without ever looking at
a specific repo, it's a recipe; if it already contains repo facts, it's an instance that escaped its
discovery pass. The archetype carries the *discovery instructions*; the instance carries the *resolved
answers*.

---

## The universal model: two primitives

Reusable agent customization collapses into **two primitives**. Decide which one a skill is before
writing it — they activate differently:

| Primitive | What it is | When it loads |
|---|---|---|
| **Standing context** ("rules" / "instructions" / memory) | Always-relevant background the agent should respect on every (or path-matched) request. | Auto-injected — always-on, or attached when a file glob matches. |
| **Invokable command** ("skill" / "command" / "workflow" / "prompt") | A task template the user (or the model) fires deliberately to *do* a multi-step job. | On demand — explicit `/name`, or model-decided from its description. |

Every meta-skill in [`skills/`](skills/) is an **invokable command**. Standing-context files (a
`CLAUDE.md` / `AGENTS.md` / `copilot-instructions.md`) are where a project's *constants and hard
constraints* live, which the commands then reference. A good suite uses both: thin always-on rules
for invariants, fat on-demand commands for workflows.

**Action vs. standard — the test to run before authoring anything.** Many useful patterns bundle a
*standard* with an *action over it*: audit an invariant, record a north-star metric, reconcile a
backlog, append an immutable log. The **action is the skill** (this library); the **standard it
enforces is a rule** that belongs in standing context. Keep the standard in one place and have the
skill *reference* it — never re-author the rule inside the skill. So "no allocation on the audio
thread" is a rule; the `/audit` that checks the diff against it is a skill. "Latency is the north
star and regressions block release" is a rule; the `/latency-log` that records one measurement is a
skill. This library only covers the skills.

### The activation taxonomy

Every agent expresses some subset of four activation modes. Pick one per skill:

1. **Always-on** — injected into every request.
2. **Glob/path-attached** — injected when an in-context file matches a pattern.
3. **Model-decided** — the agent reads the skill's *description* and chooses whether to load it.
4. **Manual** — only when the user explicitly invokes it (`/name` or `@name`).

This is why **the `description` field is the single most important line you write**: in modes 3 and 4
it is both the trigger signal and the menu text. Lead with the outcome and enumerate concrete trigger
phrases.

---

## The portable skill skeleton

Author every invokable command to this shape. It maps cleanly onto all agents; only the *header
syntax* changes.

```
<HEADER>                  # frontmatter or TOML — see the agent-mapping table
  name / id               # usually also the filename; becomes the /command
  description             # what it does + when to fire it (trigger phrases). ALWAYS present.
  [activation hints]      # globs / applyTo / alwaysApply / whenToUse — per agent
  [tool & model hints]    # allowed tools, model/effort — only if the agent supports it
<BODY> (Markdown)
  # /<name> — <short imperative summary>
  <intent paragraph>      # the DELIVERABLE and the BOUNDARY ("produces X, not Y")
  <bolded top guardrail>  # the one invariant most likely to be violated
  ## 1. <bolded step lead-in> — detail
  ## 2. ...                # numbered, ordered, dependencies explicit
  ## Notes                 # standing constraints, sibling cross-refs, honesty reminders
```

Rules of thumb that hold regardless of agent:

- **Filename / directory name → the command name.** Keep them in sync with `name`.
- **Body loads only on invocation** in most agents, so it can be long and detailed; the description is
  what's cheap and always-resident, so it must stand alone.
- **Argument placeholders** exist almost everywhere but spelled differently: `$ARGUMENTS` / `$1`
  (Claude/Codex), `{{args}}` (Gemini), positional `$1`–`$9` (Codex). Use the target's form.
- **Bundle helper scripts** for anything deterministic or long-running (e.g. launching a server) so
  the model runs a script instead of improvising. Claude skills are *directories* and can ship scripts
  alongside `SKILL.md`; single-file agents reference a script in the repo instead.

---

## Agent-mapping table — where the skeleton lands

Translate the skeleton into the target agent's concrete files. (Verify against current docs — these
move; sources at the bottom.)

| Agent | Invokable-command file | Standing-context file | Header format & key fields | Invocation |
|---|---|---|---|---|
| **Claude Code** | `.claude/skills/<name>/SKILL.md` (a *directory*, can bundle scripts) | `CLAUDE.md`; `.claude/` | YAML frontmatter: `name`, `description`, `when_to_use`, `allowed-tools`, `model`, `paths`, `user-invocable`, `disable-model-invocation` | `/name`; or model-decided from `description` |
| **Cursor** | `.cursor/commands/<name>.md` (plain MD) | `.cursor/rules/*.mdc` (`description`, `globs`, `alwaysApply`); `AGENTS.md` | Commands: no frontmatter. Rules: YAML frontmatter | Commands: `/name`. Rules: Always / Auto-glob / Agent-requested / `@name` |
| **GitHub Copilot** | `.github/prompts/<name>.prompt.md` (`description`, `mode`, `model`, `tools`) | `.github/copilot-instructions.md`; `.github/instructions/*.instructions.md` (`applyTo` glob) | YAML frontmatter | Prompts: `/name`. Instructions: auto-injected |
| **Windsurf** | `.windsurf/workflows/<name>.md` (title + description + numbered steps) | `.windsurf/rules/*.md` (Activation Mode) | Markdown; rules carry activation mode | Workflows: `/name`. Rules: Manual `@` / Always / Model / Glob |
| **Gemini CLI** | `.gemini/commands/<name>.toml` (subdirs → `/ns:name`) | `GEMINI.md` | **TOML**: `prompt` (req), `description`. Templating `{{args}}`, `!{cmd}`, `@{path}` | `/name` |
| **OpenAI Codex** | `~/.codex/prompts/<name>.md` (home, not repo-shared) — *Skills now preferred* | `AGENTS.md` (hierarchical, root→leaf override) | Prompts: `description`, `argument-hint`, `$1`–`$9`, `$NAME` | `/prompts:name`. AGENTS.md auto-loaded |
| **Cline / Roo** | Cline: `.clinerules/workflows/<name>.md`. Roo: a **mode** in `.roomodes` (rebinds role + tool perms) | Cline `.clinerules/*.md` (`paths` glob). Roo `.roo/rules*/` | Cline: optional YAML (`paths`). Roo: YAML/JSON mode (`slug`, `roleDefinition`, `groups`, `whenToUse`) | Cline workflow: `/name`. Roo mode: menu or `whenToUse` auto-select |

**Cross-agent fallback:** `AGENTS.md` is read by Codex, Cursor, and Copilot; `CLAUDE.md` by Claude
(and Copilot for compat). For standing context that must work everywhere, put invariants in
`AGENTS.md` and let each agent's native rule file `@`-reference or duplicate the essentials.

**Portability caveat:** invokable *commands* do **not** share a format across agents — you maintain N
copies (one per target), differing only in the header and argument syntax. The **body prose is
reusable verbatim**; write it once, re-wrap the header per agent. Standing context is closer to
portable thanks to the `AGENTS.md` convergence.

---

## Universal design principles

These are what make a skill *reliable* rather than just a prompt. They are behavioral, so they
transfer across every agent unchanged — express each in the target's idiom (e.g. "confirm with the
user" might be a structured question UI in one agent and a plain chat prompt in another). **Bake the
relevant ones into every skill you author.**

- **Gate-and-stop discipline.** Each verification step ends with "if this fails, **stop and report** —
  don't paper over it." Never push past a red gate (failing test, broken repro, unmet criterion).
- **Validate the work still serves the goal — don't build on autopilot.** For any change or start
  skill, include a step that re-justifies the work against the project's goal *before* executing it.
  Green gates prove a change is *correct*, not that it's *worth making* — only the goal answers that.
  Treat the plan as a living document: surface work that solves a non-problem or fights the project's
  intent, and propose dropping or deferring it instead of building it.
- **Confirm before irreversible / outward actions.** Anything that commits, pushes, deletes,
  publishes, or mutates shared state is gated behind explicit user sign-off. Present the proposed
  action (e.g. the commit message) and wait for approval.
- **Honesty over optimism.** If a step was skipped, a path couldn't be reached, or a check wasn't
  actually run, **say so** instead of implying it was done. Ground claims in observed output.
- **Blast-radius thinking.** For any change skill, include a step that maps *everything the change
  could affect* (find every consumer of each touched symbol/route/API), not just the edited lines —
  and re-verify those. This is where regressions hide.
- **Reproduce, don't reason-only.** For bug work, require a concrete, re-runnable reproduction artifact
  (recording, failing test, log transcript). Forbid talking oneself out of it.
- **Objective measurement over impression.** When a skill records or verifies a measurement, capture a
  *diffable* number or artifact (a rendered buffer, a latency figure, a snapshot) rather than a felt
  estimate. If only an estimate is available, **label it as such** — an unlabelled guess pollutes the
  record.
- **Append-only history.** Skills that maintain logs, journals, or ledgers **never rewrite past
  entries** — they add new ones and reconcile forward. History is immutable; the trail is the value.
- **Right-home mapping for durable fixes.** When a skill emits guidance/rules, map each fix to the
  **lightest durable mechanism** that removes the friction, and to where it belongs: this skill's body
  / a standing-context rule (`CLAUDE.md`/`AGENTS.md`) / a script / a settings hook / personal memory /
  a doc update / a permission allowlist. Flag tracked-vs-ignored so "this is now shared" is never a
  false claim, and don't over-engineer — pick the smallest mechanism that lasts.
- **Cross-reference siblings.** Skills point at each other by command name ("if the server isn't up,
  start it with `/<launcher>`"). The suite is a workflow, not isolated tools.
- **Respect standing project constraints.** Echo the repo's hard rules (env setup, read-only infra,
  never bypass hooks, etc.) in `## Notes` so each skill self-enforces. The one *sanctioned* exception
  to hook-bypass is a disposable, never-pushed local checkpoint that will be unwound (see
  [suspend-unsuspend](skills/suspend-unsuspend.md)) — a real commit is always gated and never skips
  hooks.
- **Load integrations deliberately, with a fallback chain.** When a step needs external tools (issue
  tracker, browser, MCP), instruct the agent to acquire them via its own mechanism first, and give a
  graceful degradation path (integration → browser → ask the user).
- **Long-running processes run detached.** Servers/watchers launch as a tracked background task with a
  readiness check and a documented stop method — never in a way that blocks the turn.

---

## The meta-skills

Start with [`skills/authoring-a-skill-suite.md`](skills/authoring-a-skill-suite.md) — it is the
entry-point meta-skill that orchestrates the others: identify the target agent, choose archetypes,
run discovery, and emit concrete skills. The remaining four are the reusable command archetypes; most
dev repos want some subset.

| Meta-skill | Deliverable it teaches an agent to build |
|---|---|
| [authoring-a-skill-suite](skills/authoring-a-skill-suite.md) | The procedure for turning these archetypes into a concrete, project-specific skill suite. |
| [start-work](skills/start-work.md) | A `/prep` command: a ready workspace + agreed plan, no code written yet. |
| [capture-repro](skills/capture-repro.md) | A `/capture-repro` command: a failing test or captured measurement that proves a bug before the fix. |
| [run-it](skills/run-it.md) | `/up` / `/up-full` launchers: the app or full stack running as a tracked background task. |
| [invariant-audit](skills/invariant-audit.md) | An `/audit` command: scan the diff against the project's hard rules and block on violations. |
| [commit-gate](skills/commit-gate.md) | A `/commit` command: a verified change committed only on approval. |
| [suspend-unsuspend](skills/suspend-unsuspend.md) | Paired `/suspend` · `/unsuspend` commands: park the branch as a throwaway WIP checkpoint to switch tasks, then unwind it to restore the working tree. |
| [metric-ledger](skills/metric-ledger.md) | A `/log-<metric>` command: record a measurement to a tracked ledger and flag regressions. |
| [session-journal](skills/session-journal.md) | A `/diary` command: append an immutable dated session entry. |
| [task-queue](skills/task-queue.md) | A `/todo` command: maintain the persistent cross-session backlog. |
| [postmortem](skills/postmortem.md) | A `/postmortem` command: durable, honest improvements from a finished session. |
| [open-pr](skills/open-pr.md) | A `/create-pr` command: push the branch and open a PR on sign-off, with merge style / PR conventions / tracker linkage discovered at authoring time. |
| [repo-housekeeping](skills/repo-housekeeping.md) | A `/housekeeping` command: delete content-merged branches, flag stale ones, archive shipped backlog items — VCS detected at authoring time. |
| [adversarial-skeptic](skills/adversarial-skeptic.md) | A `/skeptic` command: independent minimal-context subagents that attack a change *or* a decision and end on the refinements that fix it. Judge-only. |
| [walkthrough](skills/walkthrough.md) | A `/walkthrough` command: explain a change or code in depth — flow, why, before/after, history, trajectory. Explain-only, no verdicts. |

The same skeleton and principles extend to `/review`, `/verify`, `/deploy`, and other commands — only
the steps change.

---

## Notes for the authoring agent

- The **structure and principles are universal; the commands, paths, conventions, constraints, and
  header syntax are not** — re-derive them per project and per agent. Never carry another repo's or
  another agent's specifics across.
- A skill that lies (claims a check ran when it didn't, or hard-codes a command that doesn't exist) is
  worse than no skill. Prefer asking over guessing.
- Keep each skill focused on one job; let the suite compose. Resist a mega-skill — and resist Roo's
  temptation to over-scope a "mode" when a plain command will do.
- Skills are cheap to iterate, especially where they live in local-only dirs — refine wording after the
  first real run.

### Sources (verify; these docs move)

- Claude Code Agent Skills — https://code.claude.com/docs/en/skills
- Cursor Rules & Commands — https://cursor.com/docs/context/rules
- GitHub Copilot custom instructions & prompt files — https://code.visualstudio.com/docs/agent-customization/custom-instructions
- Windsurf Rules & Workflows — https://docs.windsurf.com/windsurf/cascade/workflows
- OpenAI Codex AGENTS.md & prompts — https://developers.openai.com/codex/guides/agents-md , https://developers.openai.com/codex/custom-prompts
- Gemini CLI custom commands — https://geminicli.com/docs/cli/custom-commands/
- Cline rules — https://docs.cline.bot/customization/cline-rules ; Roo Code custom modes — https://roocodeinc.github.io/Roo-Code/features/custom-modes
- AGENTS.md open standard — https://agents.md
