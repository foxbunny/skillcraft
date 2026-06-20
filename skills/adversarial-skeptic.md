# Meta-skill: adversarial skeptic

**Archetype for a `/skeptic` command.** Use this to author a skill whose deliverable is **an
adversarial pressure-test of either a change or a decision, ending on the refinements that would fix
what it found**. The boundary: it **judges; it does not act** — no edits, no commits, and it does not
make the decision for the user. It is the red-team complement to a balanced review, not a replacement
for one.

Read the [README](../README.md) for the skeleton, header-wrapping, and principles. Author this skill
with [authoring-a-skill-suite](authoring-a-skill-suite.md).

**Top guardrail: the subagents run on a minimal, self-contained brief — never feed them our
reasoning.** The whole value is independence: a skeptic that inherits our transcript just agrees with
us. Give it the facts and the goal, deliberately exclude the chain of reasoning and what we already
ruled out, and let it re-derive its position from scratch.

## The defining idea

Adversarial review is run by **independent subagents on thin briefs**, not by the agent talking to
the user. One reviewer who shares your context shares your blind spots; a fresh agent told only the
facts and charged to *break* the thing finds what confirmation bias hid. The skill is adversarial in
**both** modes — it attacks the prevailing view, it does not balance or advocate — but always ends on
**refinements** (the smallest change that neutralises each flaw), because the point is a sharper
artifact or a better-made decision, not a body count.

It has two modes, dispatched by what it is pointed at:

| Mode | Target | The subagent's job |
|---|---|---|
| **Break it** | code — a diff, a path, a PR, the change under discussion | Assume the code is wrong / fails its goal and **prove it** with a concrete reproduction. |
| **Tear it down** | one or more decisions/options being weighed | **One skeptic per option**, each assuming its option is the wrong call; refine every option to its strongest form, then break any tie with an impartial evaluator. |

The tell for *tear it down* is that the conversation is **weighing alternatives**, not checking
whether something works. If genuinely ambiguous, state your one-line read of the mode and proceed.

## Generalized steps (the reusable body)

### Break it (code)
1. **Resolve the target and the goal.** Target: dispatch on the argument — none → the change under
   discussion (branch-vs-base diff + uncommitted); a path → that code; a PR ref → its diff; a quoted
   focus → that slice. Goal (the yardstick): recover it in order — what the user stated as
   acceptance criteria, then the linked ticket, then the intent visible in code/commits/tests. The
   strongest finding is often "the ticket asked X; this does Y." If unrecoverable, state a one-line
   assumption and proceed — a wrong yardstick beats none.
2. **Build the minimal brief.** Self-contained, no transcript: the goal, the code with real anchors
   (`file:line`), and the **minimum surrounding contract** it depends on but doesn't show (the
   invariant, the input shape, the caller's expectation — one or two lines each). That contract is
   the one place to spend words; without it the skeptic flags things already gated upstream. Name any
   repo rules so it judges against the project's conventions. **Exclude** our reasoning and what we
   ruled out.
3. **Spawn the skeptic(s).** Default to one focused pass; for a broad or high-stakes change fan out
   2–4 in parallel, each a **distinct lens** (correctness/logic, goal-met?, invariants/contracts,
   failure modes) so they don't all find the same thing. Prefer the repo's own adversarial agents
   where it has them. Charge each: *assume this code is wrong and prove it; every claim needs a
   `file:line`, the exact triggering input/sequence, and the wrong outcome — a reproduction, not a
   worry. Tier findings* **PROVEN / LIKELY / QUESTION**, *add a one-line fix direction to each, and
   if you can't break it say so and name the strongest thing you couldn't rule out.* When you spawn
   these as defined subagents, **pin each one's model in its definition** so dispatch can't silently
   downgrade to a cheaper default — an underpowered skeptic misses the subtle breaks that justify the
   pass.
4. **Verify, then report.** The brief was thin, so **you** are the validation layer: check each
   surviving finding against the real code and upstream contract and give it a tagged verdict with a
   one-line citation of the rule or code that settles it; kill the ones already gated (mark them false
   positives — **expect a high rate, commonly 30–50%**). Process every candidate to a verdict — "the
   rest look minor" is a process miss, not a judgement — and never fold a real hole into a blanket
   "minor" dismissal. Forward only survivors. Report: **Verdict**
   (holds up / holds up with caveats / does not meet the goal), **Confirmed holes** (ordered by
   severity, each with anchor, trigger, wrong outcome, tier, fix direction), **Dismissed** (and why),
   and the **strongest unrefuted doubt** if nothing was proven. "I tried to break it and couldn't" is
   a valid result.

### Tear it down (a decision)
1. **Resolve the options and the frame.** Options: the named one if the user named one, else every
   option on the table (the default) — resolve each to verbatim text. Frame: the decision criteria
   shared across options plus the hard constraints that bound the choice. "Wrong call" means *worse
   than an available alternative on the stated criteria*, not "imperfect in a vacuum."
2. **Build one minimal brief per option.** Each contains: this option (verbatim, the subject), the
   others (verbatim, briefly — so "beats it" is judgeable), the criteria, and the hard constraints.
   Pull the option *text* from the conversation but **exclude our leaning** — each skeptic judges its
   own option on the merits, not told which way we tilt.
3. **Fan out — one skeptic per option, in parallel.** Each attacks only its own option (it sees the
   others only as the bar to clear). Charge each: *assume this option is the wrong call and prove it
   — the scenario that breaks it, the cost the discussion isn't pricing in, the load-bearing
   assumption that sinks it if false, and the alternative that beats it on which criterion. Tier each
   objection, add the* **refinement** *that would neutralise it (or "fatal — no cheap fix").*
4. **Refine every option, validate, compare.** Drop objections built on false premises or conditions
   that don't hold here. Apply each option's cheap refinements to produce its **strongest form**, and
   carry forward only the objections that survive refinement. Compare refined-vs-refined — every
   option got attacked, so the question is which survives best, not which got hit.
5. **Break a tie if there is one.** If one refined option clearly survives best, skip ahead. If two
   or more are close, spawn **one impartial tie-breaker** with a *balanced* brief (the tied refined
   options, their residual drawbacks, the criteria and constraints — **not** our leaning, **not** the
   raw objection dumps). It weighs pros and cons even-handedly, picks one, and names the priority that
   would flip the call. It advises; you own the synthesis.
6. **Report.** Lead with the recommendation (the option to back, in refined form), then the rationale,
   the **drawbacks of the pick** that survived refinement (eyes open, not hidden), the other options
   in their strongest form with their key residual drawback, and the dismissed objections. Don't stop
   at "they all have problems" — land on the best-refined option with its trade-offs in plain view.

## Facts to discover before emitting

- How to get the change under review: the VCS diff commands (branch-vs-base and uncommitted) and how
  to fetch a PR's diff (`gh`/`glab`/host CLI or API), normalised to the project's host.
- The **yardstick source**: the issue tracker and id format used to recover a change's intended goal
  (cross-reference [start-work](start-work.md)'s ticket fetch), and the fallback when there's no
  ticket.
- Whether the repo ships its **own adversarial agents or review-checklist rules** worth preferring
  over a generic skeptic — and the standing rules a skeptic should judge code against.
- The agent's subagent/parallel-dispatch mechanism (how this agent spawns independent reviewers).

## Principles that especially apply

- **Honesty over optimism** — don't manufacture a finding to pad the list, and don't soften a real
  one; a strawman costs the skeptic its credibility, and "couldn't break it" is a valid result.
- **Reproduce, don't reason-only** — every code finding needs a concrete trigger and wrong outcome,
  not a worry.
- **Confirm before irreversible / outward actions** — not applicable as a gate here because the skill
  *never acts*; state that boundary plainly instead.
- **Validate the work still serves the goal** — the most valuable break is "this doesn't do what was
  asked," so always recover and attack against the real goal.

## Notes

- **Judge-only:** never edits code, runs nothing destructive, never commits, never makes the call —
  the fix direction points the way; applying it is a follow-up.
- Pairs with a balanced review (`/code-review` / the built-in review skills) and with
  [walkthrough](walkthrough.md) (explain, don't judge). The skeptic is the one that *tries to make it
  fail* — whether "it" is code or a decision. Its decision-mode has no analog in a standard diff
  review; that mode is the part worth keeping even where a project already has a code-review command.
- The parent agent is the validation layer by design — thin briefs trade a false-positive rate for
  independence. Don't forward unverified skeptic output.
