# Meta-skill: authoring rules and agent personas

**Archetype for adding companion rules and personas to a project-specific skill suite.** Its
deliverable is the smallest set of harness-native standing instructions and specialist agent
definitions that make the suite reliable. It may produce no persona when a skill plus shared rules
is sufficient.

Read the [README](../README.md) for the three primitives and
[harness-rules-and-agent-personas](../references/harness-rules-and-agent-personas.md) for current
harness semantics. Use this recipe from
[authoring-a-skill-suite](authoring-a-skill-suite.md), after the target harness is known.

**Top guardrail: prompt text is guidance, not enforcement.** Never put a permission, sandbox,
approval, or security boundary only in a rule or persona and claim it is enforced. Configure the
harness's real policy surface, or report that enforcement is unavailable.

## 1. Classify the requested customization

Run the **action / standard / persona** test:

- A repeatable multi-step action is a **skill or workflow**.
- A stable fact, convention, invariant, or preference is a **rule**.
- A specialist worker that benefits from an independent context, distinct tool surface, stable role,
  or explicit handoff is a **persona**.

Split mixed requests. Keep the action in the skill, the invariant in one shared rule, and only the
role-specific contract in the persona. Do not create a persona merely to hold a long procedure.

## 2. Discover the harness contract

Inspect existing instruction, rule, skill, agent, mode, settings, permission, and hook files before
choosing paths. From the harness documentation and installed version, establish:

- rule scopes, activation modes, load order, precedence, size limits, and import behavior;
- persona locations, schema, selection/delegation triggers, context isolation, and reload behavior;
- which project instructions each persona inherits, skips, or must explicitly opt into;
- which tool, model, sandbox, permission, hook, and worktree fields are actually enforced;
- whether the surface is stable, preview, client-specific, or unsupported.

Use the reference map as a starting point, not as proof. If the harness has no documented persona
surface, do not invent one; emit only supported artifacts and record the gap.

## 3. Design the rule set

Inventory candidate guidance and give each item one authoritative home. For every rule record:

- concern and authoritative source;
- exact instruction, with a concrete example or repository reference where useful;
- scope: organization, user, repository, subtree, file pattern, or mode/persona;
- activation: always, path/glob, model-decided, or manual;
- conflict and precedence behavior;
- whether it is behavioral guidance or an enforced control.

Keep always-loaded rules short. Move procedures into skills, detailed background into linked docs,
and narrow guidance into path-scoped rules. Do not treat the absence of a rule as permission.

## 4. Design each persona as a contract

Create a persona only for a distinct responsibility. Define:

- **identity and trigger:** stable name plus a description stating when the parent should delegate;
- **job and boundary:** one outcome, explicit non-goals, and whether it may modify state;
- **inputs and return:** the minimum brief it receives and a structured handoff the caller can use;
- **context:** shared rules it must inherit, source material it must retrieve afresh, and conversation
  history it must not receive;
- **capabilities:** least-privilege tools, integrations, file access, and optional model/reasoning choice;
- **runtime:** foreground/background, parallelism, isolation/worktree needs, limits, and failure behavior.

Do not duplicate hard invariants in the persona body. Configure inheritance or explicitly point the
persona at their authoritative rule files. A read-only sentence is not a read-only runtime: use real
tool/policy restrictions where supported.

## 5. Wire skills, rules, and personas together

State in each calling skill:

1. when to delegate;
2. the persona name and minimum self-contained brief;
3. which shared rules must be present;
4. the expected return schema;
5. who validates the result and owns side effects.

Do not assume a child receives the parent's transcript or repository instructions. Use the harness's
documented inheritance switch, include the necessary facts in the brief, or fail clearly when neither
is possible. Avoid circular delegation and keep independent evaluators free of the implementer's
success narrative.

## 6. Emit harness-native artifacts

Write the smallest supported set of files. Preserve existing layout, names, ordering, frontmatter,
and local-vs-shared conventions. Keep descriptions concise because many harnesses expose them to the
parent continuously and use them for routing. Put deterministic enforcement in policies, hooks, or
scripts rather than prose.

For every emitted artifact, record whether it is version-controlled, its scope, activation, and its
authoritative source. Flag experimental or client-specific fields.

## 7. Validate from a fresh session

- Run the harness's parser, validator, doctor, or inventory command when one exists.
- Prove the intended rule loads under one matching condition and does not load under one nonmatching
  condition; check precedence with a harmless sentinel when layering is material.
- Trigger each persona without naming it when model-decided routing is intended, then invoke it
  explicitly as a control.
- Have the persona report the rules and tools it actually received; compare that with the contract.
- Exercise one forbidden capability through a harmless probe to verify the policy layer—not merely
  the persona's willingness to comply.
- Confirm a fresh-context persona did not receive excluded implementation narrative.

If the runtime is unavailable, validate syntax and paths and report live discovery, inheritance, and
delegation as unverified. Do not infer success from valid Markdown or YAML alone.

## Facts to discover before emitting

- Target harness, client/surface, installed version, and official documentation version.
- Existing rule hierarchy, imports, precedence, naming, and local-vs-shared conventions.
- Existing personas/modes, delegation mechanism, context inheritance, and reload behavior.
- Real permission, policy, sandbox, hook, and tool-control surfaces.
- Which skills need a specialist and why a separate context or capability boundary helps.
- The authoritative sources for every invariant and preference.
- Available validation and fresh-session test commands.

## Notes

- A persona is not a stronger rule and a rule is not a permission boundary.
- Prefer a few narrow personas with distinct triggers over a catalog of generic helpers.
- Keep shared truths in rules; keep role-specific judgment and handoff contracts in personas.
- Re-run the harness survey when upgrading the target client. These formats and inheritance semantics
  are moving targets.
