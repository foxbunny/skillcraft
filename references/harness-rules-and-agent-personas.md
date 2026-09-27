# Harness rules and agent personas

Use this reference while applying
[authoring-rules-and-agent-personas](../skills/authoring-rules-and-agent-personas.md). It records how
the supported harnesses discover standing instructions and specialist agents. **Verify the target's
installed version and current documentation before emitting files**: these surfaces evolve quickly.

Last verified: 2026-09-27.

## Keep three concepts separate

- A **behavioral rule** is prompt context: a convention, invariant, preference, or architectural fact
  that the model should follow. It can be always-on or conditionally loaded.
- An **execution policy** is an enforced control: tool permission, sandbox boundary, command allowlist,
  hook, or approval requirement. Prompt text does not replace it.
- An **agent persona** is a named specialist with its own role and, where supported, its own context,
  tools, model, and runtime settings. It may be selected directly or delegated to by a parent agent.

Do not call all three "rules." In particular, Codex `.rules` files are command-execution policy,
whereas `AGENTS.md` carries behavioral project guidance.

## Harness map

| Harness | Behavioral rules | Agent personas and delegation | Inheritance or verification trap |
|---|---|---|---|
| **Claude Code** | `CLAUDE.md` or `AGENTS.md`; modular project rules in `.claude/rules/*.md`, optionally scoped with `paths` frontmatter. | Project personas in `.claude/agents/*.md`; YAML frontmatter plus a Markdown system prompt. `description` drives delegation; tools, model, permission mode, skills, hooks, memory, and worktree isolation are configurable. | Custom subagents normally load `CLAUDE.md`; built-in Explore and Plan do not. `omitClaudeMd` can disable inheritance. A persona prompt is not a permission boundary. |
| **Cursor** | `.cursor/rules/` supports Always, intelligent/model-decided, file-pattern, and manual activation. Root `AGENTS.md` and `CLAUDE.md` are also read automatically. | Project personas live in `.cursor/agents/*.md`; `.claude/agents/` and `.codex/agents/` are compatibility inputs. Agent may delegate automatically from `description`, or the user can request a persona. | Test the actual delegation. Project definitions outrank user definitions; `.cursor/agents/` outranks compatibility directories. Hooks and tool policy can still block delegation or tools. |
| **GitHub Copilot** | `.github/copilot-instructions.md`, path-scoped `.github/instructions/*.instructions.md`, and supported `AGENTS.md`/`CLAUDE.md` inputs are merged where the client supports them. | Repository personas are `.github/agents/<name>.md` agent profiles with YAML frontmatter and a Markdown prompt. They can be selected as the session agent or run as isolated subagents; `infer` controls automatic delegation in Copilot CLI. | A custom agent run as a Copilot CLI subagent does **not** receive repository instructions by default. Set `include-custom-instructions: true` when it must inherit them. Client support differs, so verify the intended IDE/CLI/GitHub surface. |
| **Windsurf / Devin Desktop** | Preferred workspace rules are `.devin/rules/*.md`; legacy `.windsurf/rules/*.md` remains a fallback. Rules support `always_on`, `model_decision`, `glob`, and `manual`; `AGENTS.md` is interpreted by the same rule engine. | The reviewed customization surface provides rules, workflows, skills, and built-in agents, but no repository custom-persona file equivalent was established. | Do not invent a persona format. Express task procedure as a skill/workflow and stable guidance as rules, or document that a separate agent runtime is required. Confirm whether the installed product has since added custom agents. |
| **Gemini CLI** | `GEMINI.md` files are concatenated through the context hierarchy; `context.fileName` can add names such as `AGENTS.md`. | Project personas live in `.gemini/agents/*.md`; YAML frontmatter defines `name`, `description`, tools and optional runtime settings, and the body is the system prompt. The main agent delegates automatically or via `@name`. | Omitted tools inherit the parent tool set. Enforced access belongs in Policy Engine TOML, including subagent-specific rules; prose is not enforcement. Custom subagents currently have an evolving/preview surface. |
| **OpenAI Codex** | `AGENTS.md` is loaded hierarchically from user scope and project root toward the working directory; closer project files appear later. | Project personas live in `.codex/agents/*.toml`; required fields are `name`, `description`, and `developer_instructions`. Omitted model/runtime settings inherit. Codex can delegate when explicitly asked or when `AGENTS.md`/skill instructions direct it. | `.codex/rules/*.rules` governs command execution, not behavioral context. Parent sandbox and approval policy remain authoritative; a persona cannot widen them. Verify the effective agent and instructions in a fresh run. |
| **Cline** | Workspace rules live in `.clinerules/` or `.cline/rules/`; no frontmatter means always active and `paths` frontmatter makes a rule conditional. Workspace rules take precedence over global rules. | The reviewed Cline customization documentation does not establish a repository custom-persona/subagent definition surface. | Do not encode a supposed persona in an undocumented file. Use a workflow for an action and a rule for standing guidance, or state that the target needs a harness with native personas. |
| **Roo Code** | Workspace-wide rules live in `.roo/rules/`; mode-specific rules in `.roo/rules-<slug>/`. Legacy single-file fallbacks remain available. | Project personas are custom modes in `.roomodes`. A mode defines `slug`, `name`, `description`, `roleDefinition`, `whenToUse`, `groups` (tool/file access), and optional `customInstructions`; Orchestrator can delegate with `new_task`. | A mode changes the active role and tools; it is not automatically an independent fresh context. Use delegated tasks when context isolation is required, and test the mode/tool restrictions in the target version. |

## Recipe-level invariants

1. Put a fact in one authoritative home. Personas refer to shared rules; they do not fork copies of
   architectural or security invariants.
2. Specify whether the persona must receive project rules, and configure that using the harness's
   real inheritance mechanism.
3. Treat a persona's tool list as least-privilege configuration only where the harness enforces it.
   Put non-negotiable controls in permissions, policy, hooks, sandboxing, or external authorization.
4. Prefer a skill for a bounded procedure. Create a persona only when separate context, a stable role,
   a distinct tool surface, or an independent handoff materially changes the work.
5. Verify discovery with a fresh session and verify delegation with a neutral trigger prompt. Inspect
   the effective rule/persona inventory when the harness exposes one.

## Primary sources

- Claude Code: https://code.claude.com/docs/en/memory and
  https://code.claude.com/docs/en/sub-agents
- Cursor: https://prod.cursor.com/help/customization/rules and
  https://prod.cursor.com/docs/subagents
- GitHub Copilot: https://docs.github.com/en/copilot/reference/customization-cheat-sheet and
  https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference
- Windsurf / Devin Desktop: https://docs.devin.ai/desktop/cascade/memories and
  https://docs.devin.ai/desktop/cascade/workflows
- Gemini CLI: https://geminicli.com/docs/cli/gemini-md/ and
  https://geminicli.com/docs/core/subagents/
- OpenAI Codex: https://learn.chatgpt.com/docs/agent-configuration/agents-md,
  https://learn.chatgpt.com/docs/agent-configuration/subagents, and
  https://learn.chatgpt.com/docs/agent-configuration/rules
- Cline: https://docs.cline.bot/customization/cline-rules
- Roo Code: https://roocodeinc.github.io/Roo-Code/features/custom-instructions/ and
  https://roocodeinc.github.io/Roo-Code/features/custom-modes/
