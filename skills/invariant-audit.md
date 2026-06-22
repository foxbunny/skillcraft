# Meta-skill: "audit" / invariant check

**Archetype for an `/audit` command** (e.g. `/audit-realtime`, `/audit-logs`, `/audit-a11y`). Use this
to author a skill whose deliverable is **a clean/violations verdict on the changed code, measured
against the project's hard rules** — with violations that block the change until fixed.

**Skill vs. rule boundary (read first):** the *invariants themselves* ("no heap allocation on the
audio thread", "no PII in logs", "no DB access outside the repository layer") are **rules** that live
in standing context (`CLAUDE.md` / `AGENTS.md`). This skill does **not** re-author them — it *references*
them and performs the **action** of checking the diff against them. Keep the rules in one place; let the
audit point at them.

Read the [README](../README.md) for the skeleton, header-wrapping, and principles. Author this skill
with [authoring-a-skill-suite](authoring-a-skill-suite.md).

**Top guardrail: judge by context, not just tokens.** A flagged construct may be fine *where it runs*
(setup/teardown) and forbidden elsewhere (the hot path). Audit by *location and effect*, not by string
match alone — and a violation blocks the change even when no single token is "forbidden" (e.g. a
correct-looking but wrongly-ordered concurrency handoff).

## Generalized steps (the reusable body)

1. **Identify the changed surface** that the invariant governs — the files/functions on the audited
   path (the realtime callback, the logging sites, the data layer, the render path).
2. **Scan for the forbidden patterns** with a concrete, copy-pasteable grep, then **read** each hit in
   context. Derive the grep patterns *from* the standing-context rule and point back to it — list them
   for greppability, not as a second canonical copy of the rule that will drift from it.
3. **For each hit on the governed path, report `file:line` + the lighter-weight alternative** the
   project prefers (pre-allocated pool instead of `new`, the repository API instead of a raw query,
   the structured logger instead of string interpolation).
4. **Check the subtler correctness class**, not just banned tokens — the violations that pass a naive
   scan (a wrong memory order, an unescaped value, a missing tenant filter). Spell out what "correct"
   looks like so the auditor verifies ordering/shape, not just absence.
5. **Summarize: clean, or a list of violations.** Violations block the change until fixed.

## Facts to discover before emitting

- The project's hard invariants and where they're documented (instruction files, `docs/ARCHITECTURE.md`,
  existing rules) — so the audit *references* them.
- The exact forbidden constructs and their preferred alternatives, per invariant.
- Which paths/files the invariant governs vs. where the same construct is allowed.
- A real prior incident, if one exists — naming the class that slipped through a green audit makes the
  skill concrete and credible.

## Principles that especially apply

- **Gate-and-stop discipline** — violations block; don't paper over them.
- **Blast-radius thinking** — audit every governed site the change touches, not just the obvious one.
- **Honesty over optimism** — report "clean" only when you actually traced each hit, including the
  subtle-correctness class.
- **Respect standing project constraints** — the audit enforces rules; it doesn't redefine them.

## Notes

- Cross-reference siblings: run after implementation and before [commit-gate](commit-gate.md); the
  commit gate should refuse if a required audit hasn't passed.
- One audit skill per distinct invariant domain. Resist an oversized audit that checks unrelated rules.
- The invariants live in standing context — when they change, update the rule, and the audit stays thin.
