# Meta-skill: behavioral change evaluation

**Archetype for a coordinated `/characterize-change` → `/evaluate-change` → `/behavioral-verdict`
workflow.** Use this to author a skill suite whose deliverables are a reproducible evidence inventory,
independent goal-aware assessments, and a deterministic verdict. The boundary is strict: the
characterizer records behaviour without judging it; evaluators interpret that evidence; only the
verdict step decides the gate.

Read the [README](../README.md) for the skeleton, header-wrapping, and principles. Author this suite
with [authoring-a-skill-suite](authoring-a-skill-suite.md). Use the shared
[project adapter schema](../schemas/behavioral-evaluation-config.schema.json),
[evidence schema](../schemas/behavioral-evidence.schema.json), and
[evaluation schema](../schemas/behavioral-evaluation.schema.json) as the contracts between stages.

**Top guardrail: “Control inputs and observe outputs; do not alter the system under evaluation.”**
Base and changed revisions are immutable specimens. Put harnesses, runtime state, caches, captures,
and reports outside both source trees, and verify specimen integrity before and after the run.

## The three-stage contract

Each stage runs in a fresh agent context. Do not pass the implementation conversation, the
implementer's reasoning, or a success narrative. Pass only the inputs named below. Preserve raw
artifacts so another person can reproduce every claim.

### 1. `/characterize-change` — produce evidence, not a verdict

Start the characterizer with this role statement verbatim:

> Your job is to characterize the externally observable behavioural consequences of the supplied
> diff. You are not evaluating whether the implementation is correct, desirable, complete, or
> aligned with its intended goal. Do not issue a verdict.

Give it the base and changed revision identifiers, the diff, the project adapter, and access to the
two immutable specimens. Do not give it task goals or the implementer's account of the change.

1. **Verify the specimens.** Resolve immutable commit ids; record tree hashes and configured
   integrity checks before execution. Prepare equivalent, isolated runtime state for each revision.
   If a build writes into a checkout, build a disposable copy derived from the recorded revision.
2. **Map candidate effects.** A white-box impact mapper may inspect the diff, callers, consumers,
   state transitions, persistence, errors, authorization, and asynchronous ordering. Its output is a
   hypothesis and probe plan, never behavioural evidence.
3. **Exercise legitimate interfaces.** A constrained evidence runner applies the same trigger and
   conditions to both revisions wherever practical. A changed-only observation normally establishes
   current behaviour, not behaviour caused by the diff; mark the comparison `Indeterminate` unless a
   causal comparison is otherwise demonstrated.
4. **Record one evidence item per candidate consequence.** Use exactly these result classes:
   - **Changed** — the revisions produce different externally observable behaviour under the
     exercised conditions. Also record direction: **Enabled**, **Disabled**, or **Altered**.
   - **Unchanged** — the revisions produce equivalent externally observable behaviour under the
     exercised conditions. This applies only to the exact conditions exercised.
   - **Indeterminate** — a reliable comparison cannot be produced through the permitted interfaces
     and available environment. This is an expected outcome and does not mean no consequence exists.

   Do not create a “not externally observable” class; inability to establish an external consequence
   is `Indeterminate`. Do not replace missing evidence with “likely,” “should,” “appears correct,” or
   other source-level inference. Phrase the candidate consequence neutrally until the observations
   establish a result. If a probe matrix yields different classifications for different conditions,
   split it into separate evidence items so each item has one classification over one coherent set of
   exercised conditions.
5. **Capture the comparison.** Every item records the candidate consequence, trigger and conditions,
   base observation, changed observation, classification, direction when changed, raw evidence
   references, exact reproduction procedure, observation boundary, limitations, and untested
   conditions. Preserve HTTP transcripts, database snapshots or diffs, DOM and accessibility trees,
   screenshots, recordings, network traces, emitted events, filesystem diffs, logs, and timings when
   they are the relevant observable surface.
6. **Verify integrity again.** Run the configured post-checks and include the results. A modified or
   unverifiable specimen makes affected comparisons `Indeterminate`; never repair the specimen and
   continue as though it were unchanged.

The evidence runner must not modify either application revision; add diagnostic endpoints, test-only
branches, flags, logging, or observability; bypass routing, authentication, authorization, validation,
or lifecycle behaviour; call private internals instead of legitimate interfaces; seed impossible
states; replace internal components with mocks; weaken security; use self-added instrumentation as
evidence; or force a conclusion to avoid `Indeterminate`.

It may use the real UI; existing public or legitimate administrative APIs; existing logs and
telemetry; request/response capture; supported fixtures; durable database state; emitted messages,
traffic, files, browser storage, DOM, accessibility trees, screenshots, recordings, and timing. It
may control connectivity, time, and external responses only at existing environment or integration
boundaries. For every mocked external interaction, capture the application request, mock response,
the basis for treating that response as contract-valid, and the resulting observable behaviour.

### 2. `/evaluate-change` — retrieve goals afresh and assess by concern

Start new evaluator contexts after characterization. Retrieve goal material at this point, driven by
the observed consequences and affected capabilities rather than the implementer's justification.
Retrieve both supporting and conflicting material, preserving source, authority, version or date,
and retrieval time. Distinguish:

- explicit task objective;
- acceptance criteria;
- hard system invariants;
- architectural decisions;
- product or quality goals;
- preferences;
- historical context and known failures.

Absence of a retrieved rule is not permission. If required material cannot be retrieved, record the
gap and let the verdict become insufficient rather than inventing a rule.

Select independent evaluators from the affected concerns: task completion, regression and invariant
preservation, accessibility and usability, data integrity, security and authorization, architecture,
or broader system goals. Each gets only the evidence inventory, the freshly retrieved goal packet,
its concern brief, and the project adapter. Each finding must cite evidence and goal sources,
separate demonstrated observation from interpretation, and classify the relationship as `advances`,
`preserves`, `undermines`, `trade_off`, `unrelated`, or `indeterminate`.

Normalize their outputs into required-criterion and hard-invariant assessments using the
[evaluation schema](../schemas/behavioral-evaluation.schema.json). Keep conflicting assessments; do
not collapse them into a vote.

### 3. `/behavioral-verdict` — apply policy, do not vote

Validate the normalized packet against the evaluation schema, then run
[`scripts/aggregate_behavioral_verdict.py`](../scripts/aggregate_behavioral_verdict.py) over it. The
default policy is deliberately asymmetric:

- any demonstrated hard-invariant violation → `fail`;
- any unmet required acceptance criterion → `fail`;
- any missing or insufficient assessment for a required criterion, or an indeterminate required hard
  invariant → `incomplete`;
- all required criteria demonstrated with every required hard invariant preserved → `pass`;
- nonblocking trade-offs are surfaced separately for human judgment.

One concrete blocking finding wins over any number of favourable opinions. Never use majority voting
to override demonstrated contrary evidence. If a project needs a stricter policy, replace the script
at authoring time and test the policy; do not weaken these defaults silently.

## Facts to discover before emitting

Bake confirmed project facts into the generated suite and its adapter. Do not leave commands as
guesswork. Discover and propose:

- how to determine the base and changed revisions, and how to start each exact revision;
- supported user, client, and legitimate administrative interfaces;
- test identities and documented fixture setup;
- observation surfaces and database snapshot mechanisms;
- external integration boundaries and authoritative sources for valid mock contracts;
- sources for objectives, acceptance criteria, invariants, decisions, goals, preferences, and history;
- how affected concerns select evaluators;
- the hard-invariant set and any stricter verdict rules;
- evidence artifact location, naming, access controls, and retention;
- integrity checks that detect tracked, untracked, ignored, generated, and durable-state changes.

Store these extension points in a project adapter shaped by
[`behavioral-evaluation-config.schema.json`](../schemas/behavioral-evaluation-config.schema.json).
Omit unsupported capabilities instead of inventing them, and make that absence visible to the
characterizer as a possible source of `Indeterminate` results.

## Principles that especially apply

- **Reproduce, don't reason-only** — source inspection proposes probes; only observed comparisons are
  behavioural evidence.
- **Objective measurement over impression** — retain raw, diffable artifacts and exact procedures.
- **Blast-radius thinking** — map callers, consumers, state, failure, authorization, and ordering
  before choosing probes.
- **Honesty over optimism** — `Unchanged` is scoped, `Indeterminate` is valid, and unrun checks stay
  unclaimed.
- **Gate-and-stop discipline** — immutable-specimen failures and invalid evidence contracts stop the
  affected comparison; demonstrated invariant violations stop the final gate.

## Notes

- This workflow complements [capture-repro](capture-repro.md), [invariant-audit](invariant-audit.md),
  and [commit-gate](commit-gate.md). It does not replace implementation tests or a code review.
- Keep mapper and runner as separate agents when the platform supports it. If they must be phases in
  one agent, carry forward only the probe plan, treat all source-derived claims as hypotheses, and
  enforce the same evidence contract.
- The characterizer never calls a result an improvement, regression, fix, defect, success, or
  failure. Those are evaluator interpretations, not evidence classifications.
