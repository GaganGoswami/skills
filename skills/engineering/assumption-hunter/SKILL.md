---
name: assumption-hunter
description: Surface hidden assumptions in plans, designs, specs, and code before they become bugs, rework, or production incidents. Use when reviewing a plan, before starting implementation, when something "obviously works" but hasn't been verified, when the user says "we assumed", "of course X is true", or asks "what am I missing".
---

# Assumption Hunter

Make the invisible visible. Every plan runs on assumptions. Surface them before they surface you.

## Trigger

Auto-run at the start of any plan review or architecture discussion. Also invoke explicitly when:

- A plan says "assuming X, we will..." and X was never verified
- A design was made with data that's now > 6 months old
- An implementation is about to start on a spec that hasn't been pressure-tested
- Post-mortem analysis ("we assumed the retry would succeed")

## Workflow

### Step 1 — Ingest the artifact

Read the plan, spec, design doc, or code region the user provides. If none is provided, ask for the single most important artifact to analyze.

### Step 2 — Hunt by category

Scan across all four assumption categories from [CATEGORIES.md](CATEGORIES.md). For each category, list every assumption found — both explicit ("we assume X") and implicit (buried in the design without being stated).

Format each finding:

```
[CATEGORY] Assumption: <the belief>
Evidence: <what evidence exists that this is true, if any>
Risk if wrong: <what breaks, and how badly>
Verification: <cheapest way to confirm this is actually true>
```

### Step 3 — Prioritize by blast radius

Rank all assumptions by: **Risk if wrong** × **Evidence quality**

| Priority | Criteria |
|---|---|
| **Critical** | High risk if wrong + no evidence |
| **High** | High risk if wrong + weak evidence |
| **Medium** | Medium risk + no evidence |
| **Low** | Low risk, or strong evidence already |

Surface all Critical and High assumptions to the user before any implementation starts.

### Step 4 — Propose assumption tests

For each Critical/High assumption, propose the **cheapest falsifiable test**:

- User behavior → 5-question interview, A/B test, or clickable prototype
- Technical → spike (< 4 hours), benchmarking script, or POC
- Business → market research, competitive survey, or a single sales call
- Temporal → check if the data/rule/constraint is still current

### Step 5 — Output

```
ASSUMPTION AUDIT — <artifact name>

CRITICAL (verify before proceeding):
1. [TECHNICAL] We assumed Redis can sustain X ops/sec at our volume.
   Evidence: None. Risk: Cache stampede under load.
   Test: Load test with k6 against staging — 2 hours.

HIGH (verify before committing to architecture):
2. [USER] We assumed users will check notifications daily.
   Evidence: Weak — one user interview 8 months ago.
   Test: Survey 10 current users — 1 day.

MEDIUM (verify before launch):
...

SAFE TO PROCEED:
...
```

## Gotchas

- Absence of evidence is not evidence of absence — "no one has complained" is not validation
- Technical assumptions about 3rd-party services are often the most dangerous: SLAs change, APIs deprecate
- Temporal assumptions decay fastest — anything older than 6 months needs re-verification
- Don't assume the team's consensus means the assumption is correct — groupthink is an assumption failure mode
- If the plan has zero explicit assumptions stated, that's a red flag — not a sign the plan is solid
