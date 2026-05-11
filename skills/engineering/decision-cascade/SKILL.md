---
name: decision-cascade
description: Map 2nd and 3rd order consequences of a decision before committing. Surface the hidden costs, forced follow-on decisions, and risks that a choice unlocks downstream. Use when evaluating an architectural choice, technology selection, or major process change — especially when the user says "let's go with X", "we've decided on Y", or asks "what are the implications of choosing Z".
---

# Decision Cascade

Every significant decision triggers a chain of consequences. Map the chain before you commit.

## The core insight

Decisions don't happen in isolation. Choosing microservices doesn't just change your deployment model — it forces service discovery, distributed tracing, a service mesh, independent CI pipelines, and eventually a platform engineering team. Choosing a SQL database doesn't just affect queries — it forces a schema migration story, a backup strategy, a connection pooling solution, and a decision about who owns schema changes.

The cascade is where the real cost lives. This skill makes it visible.

## Workflow

### Step 1 — State the decision

Capture the decision precisely:

> "Decision: **[WHAT]** — choosing **[OPTION A]** over **[OPTION B and C]**"

Also capture: who makes this decision, when it must be made, and what it's reversible at (can it be undone? at what cost?).

**Reversibility score**: Rate 1–5 (1 = trivially reversible, 5 = permanent / very expensive to undo).

### Step 2 — Map the cascade

Pull relevant known patterns from [PATTERNS.md](PATTERNS.md). If the decision matches a known pattern, start from that template and adapt.

For each level of the cascade, ask: "Now that we've decided X, what decisions or costs does that force upon us?"

```
Decision: <X>
├── Immediate consequences (within the same sprint)
│   ├── <forced decision or cost>
│   └── <forced decision or cost>
├── 2nd order (within 3 months)
│   ├── <forced decision or cost>
│   └── <forced decision or cost>
└── 3rd order (6–18 months)
    ├── <forced decision or cost>
    └── <forced decision or cost>
```

For each node in the cascade, tag it as:
- **COST** — a real expenditure of time, money, or attention
- **DECISION** — a forced follow-on choice that must now be made
- **RISK** — a new failure mode that is now possible
- **LOCK-IN** — a constraint that will be hard to remove later

### Step 3 — Identify leverage points

A leverage point is a node in the cascade where a small change to the primary decision dramatically reduces cascade depth.

Example: Choosing event-driven async by default (instead of sync HTTP) at the service boundary eliminates 3 downstream cascade nodes around retry storms, timeout tuning, and circuit breakers.

Mark leverage points with `[LEVERAGE]`.

### Step 4 — Compare alternatives

Run the cascade for the top 2–3 alternatives. Summarize the comparison:

| | Option A | Option B | Option C |
|---|---|---|---|
| Cascade depth | | | |
| Immediate costs | | | |
| Largest 3rd-order cost | | | |
| Reversibility | | | |
| Recommended | | | |

### Step 5 — Output

```
DECISION CASCADE ANALYSIS
Decision: <decision>
Reversibility: <score>/5 — <one-line explanation>

CASCADE MAP: [Option A]
<tree as above>

KEY RISKS:
1. <highest-severity risk in the cascade>
2. <second-highest>

LEVERAGE POINT: <the one change that reduces cascade complexity most>

RECOMMENDATION: <option> — <one sentence rationale>
```

## Gotchas

- 3rd order consequences are often dismissed as "we'll deal with it later" — that is when they're cheapest to prevent
- Lock-in nodes deserve extra scrutiny: they limit future options forever
- If an option has a shorter cascade but higher reversibility, prefer it even if the immediate cost looks higher
- Don't analyze the cascade of a decision that hasn't been made yet — anchor on real options under consideration
- Organizational cascades (team structure changes, ownership changes) are as real as technical ones
