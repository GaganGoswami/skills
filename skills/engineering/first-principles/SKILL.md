---
name: first-principles
description: Deconstruct any problem, design, or plan to its irreducible truths, then rebuild the solution from scratch. Prevents anchoring bias and inherited constraints. Use when the user says "we've always done it this way", "why does X have to be like this", "is there a fundamentally better way", "challenge my assumptions", "first principles", or when a plan feels like it's optimizing around an avoidable constraint.
---

# First Principles

Stop optimizing a bad foundation. Tear the problem down to bedrock, then rebuild.

## When to invoke

- A plan is adding complexity to work around a constraint that was never questioned
- The current solution is a layered accumulation of workarounds
- The user is debating *how* to do X instead of questioning *whether* X is the right goal
- A technology or pattern was chosen years ago and the original reason may no longer apply

## Workflow

### Step 1 — State the problem without the solution

Restate the problem the user is actually trying to solve, stripped of any reference to their current approach.

> Wrong: "How do we make our monolith scale better?"
> Right: "How do we serve 10× current load with acceptable latency and cost?"

If the user's problem statement contains a solution embedded in it, surface that tension explicitly before continuing.

### Step 2 — List all inherited constraints

Ask: what rules, structures, or decisions are we taking as given that we've never verified?

Scan for:
- **Technology constraints** — "we use X because we've always used X"
- **Organizational constraints** — "team A owns this, so we can't touch it"
- **Process constraints** — "this requires a human in the loop" (does it?)
- **Data constraints** — "we need to keep this for 7 years" (says who?)
- **Cost constraints** — "we can't afford Y" (at what scale? have we checked recently?)

List each constraint. Mark each as: **verified** (checked, still true) / **unverified** (assumed) / **outdated** (was true, may no longer be).

### Step 3 — Identify the irreducible truths

What is actually, physically, or logically true regardless of what we decide?

Examples:
- "Data must be stored somewhere before it can be queried" (physical truth)
- "A user cannot authenticate before they exist in a system" (logical truth)
- "Network calls have latency" (physical truth)

Irreducible truths are the only constraints you cannot discard. Everything else is negotiable.

### Step 4 — Rebuild from scratch

Starting only from the irreducible truths, generate the simplest possible design that solves the problem from Step 1.

Rules:
- Do NOT reference the existing solution
- Do NOT import inherited constraints that were marked unverified or outdated
- Do NOT optimize for current team structure — optimize for the problem

Present this as: **The clean-slate design**.

### Step 5 — Gap analysis

Compare the clean-slate design to the current solution:

| Dimension | Current approach | Clean-slate | Delta |
|---|---|---|---|
| Complexity | | | |
| Cost | | | |
| Performance | | | |
| Maintainability | | | |
| Migration cost | | | |

Produce a **migration verdict**:
- **Migrate now** — delta is large, migration cost is low
- **Migrate incrementally** — delta is large, migration cost is high (define the seam to start from)
- **Stay** — delta is small or migration cost exceeds benefit

## Gotchas

- First principles doesn't mean "rewrite everything" — it means "verify your constraints"
- Organizational constraints are real costs — a clean-slate design that requires restructuring two teams is not free
- The goal is the migration verdict, not the clean-slate design — the design is only a reasoning tool
- If the current solution survives the analysis, that's a valid and valuable outcome — don't force migration
- Don't conflate "simple" with "familiar" — a simpler design may look strange because it's unfamiliar
