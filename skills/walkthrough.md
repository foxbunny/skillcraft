# Meta-skill: walkthrough

**Archetype for a `/walkthrough` command.** Use this to author a skill whose deliverable is **a
narrative, in-depth explanation of a change or a piece of code — flow, the *why*, before/after
behavior, the history that led here, and the likely direction**. The boundary: it **explains; it
does not review.** No verdicts, no severity-ranked findings, no "fix before merge," and no code
changes. This is the "explain" role — distinct from a review (judgement) or a verify (does it run).

Read the [README](../README.md) for the skeleton, header-wrapping, and principles. Author this skill
with [authoring-a-skill-suite](authoring-a-skill-suite.md).

**Top guardrail: explain, don't judge — and skip the boilerplate, out loud.** Spend the words on the
substance; explicitly say when you're skipping boilerplate (route/socket registration, type-only
additions, test-mock padding, import shuffles, formatting) rather than narrating it. If the user
wants correctness judgement, that's a review skill; if they want to know it runs, that's a verify
skill.

## Generalized steps (the reusable body)

### Dispatch on the argument
| Argument | Mode | Means |
|---|---|---|
| *(none)* | **current branch** | Walk through everything on this branch vs the base — committed **and** uncommitted — as a refresher. Fold any throwaway WIP checkpoint (from [suspend-unsuspend](suspend-unsuspend.md)) into the work rather than describing it as a real commit. |
| a PR ref (number or URL) | **PR** | Walk through that PR's diff; cross-reference its linked ticket first. |
| a filesystem path | **code** | Walk through what that code does and how it evolved — not necessarily a recent change. "Before/after" becomes "what role it plays and how it reached its current shape"; "history" is the path's log. |

If the argument is ambiguous, state your interpretation in one line and proceed — don't stall.

### 1. Gather the material
- Pull the diff (branch-vs-base + uncommitted, or the PR's diff) or, for a path, the code plus its
  change history (`log` of the path).
- **Cross-reference the linked ticket first** for the PR/branch modes: the walkthrough's "why" and
  "before/after" are grounded in what was *asked*, not just inferred from the diff. Note where the
  change is **narrower or broader** than the ticket. A bare one-line ticket is worth flagging — it
  means the intent lives in the code and tests, not the ticket.
- **Build real context, don't guess.** Understand the system the code plugs into well enough to
  explain the *why*: run a read-only search over conventions/callers, read the neighbouring and
  canonical code, and read any relevant design doc. Cite concrete references (`file:line`, commit SHAs,
  PR/ticket numbers) so the walkthrough is verifiable.

### 2. Write the walkthrough
Adapt these sections to the mode; drop any that don't apply; lead with the key point.
1. **The one-line version** — what changed (or what this code *is*), in a sentence; for a PR, tie it
   to the ticket's actual ask.
2. **The system it plugs into** — the minimum context to follow the rest: the data shapes, the
   existing path this sits beside, the invariant it respects. Keep it tight.
3. **The substantive changes / parts** — grouped logically (not file-by-file), each with a focused
   code snippet (the relevant lines, not whole functions), the flow in order, and the **why**. Call
   out deliberate omissions ("notice there's no balance write — that's intentional because…") and
   **explicitly skip** the boilerplate, saying you're skipping it.
4. **Before / after behavior** — a compact contrast of how the relevant part behaved before vs after
   (for a path: current behavior + its role).
5. **History leading up to this** — the chain: prior tickets/PRs/commits that built the surrounding
   machinery, and what this stacks on. From the log + ticket context, not invention.
6. **Likely direction** — where this is heading: the obvious next asks, the follow-on it sets up,
   known issues someone will revisit. Grounded, not generic.
7. **Offer to drill deeper** — name 1–2 specific threads you could expand.

## Facts to discover before emitting

- VCS commands for the branch-vs-base diff, uncommitted diff, and per-path history; how to fetch a
  PR's metadata and diff on the project's host (CLI or API).
- The issue tracker and id format, and how a change links to its ticket (branch name, PR body
  convention) — reuse the ticket-fetch from [start-work](start-work.md).
- Where design docs / architecture notes live, and the project's "boilerplate" categories worth skipping
  (framework boilerplate specific to this stack).
- The agent's read-only explore/fan-out mechanism for building caller/convention context.

## Principles that especially apply

- **Honesty over optimism** — cite real references and ground the "why" in the ticket and code; flag a
  thin ticket rather than inventing intent. Say what you skipped.
- **Validate the work still serves the goal** — the cross-reference to the ticket is what lets the
  walkthrough note where the change drifted from, or exceeded, what was asked.
- **Cross-reference siblings** — point at the review/verify/skeptic commands for the jobs this one
  deliberately doesn't do.

## Notes

- **Explain-only:** never edits code, runs the app, or commits.
- Fills the explain role alongside judgement (`/code-review`, [adversarial-skeptic](adversarial-skeptic.md))
  and verification (a verify command). No built-in command covers in-depth explanation, so this is an
  additive archetype.
- Reuses [start-work](start-work.md)'s ticket fetch for the PR-mode cross-reference; keep the two in
  sync on how tickets are resolved.
