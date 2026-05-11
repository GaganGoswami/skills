# TIL Card Format

Standard output format for a completed knowledge-spike. Copy and fill for every spike.

---

```
TIL: <Technology / RFC / Pattern name>
Date: <YYYY-MM-DD>
Decision enabled: <the decision this spike was run for>
Stack-fit rating: Strong / Conditional / Weak
```

---

## What it is

_One paragraph. What problem does X solve? Who built it and why?_

## Core concepts (the 3–5 things everything else builds on)

1. **<Concept>** — <one sentence explanation>
2. **<Concept>** — <one sentence explanation>
3. **<Concept>** — <one sentence explanation>
_(add up to 5)_

## What it is NOT

_The anti-use-cases. What does X explicitly not solve, and what do people mistakenly try to use it for?_

## Stack-fit analysis

| Dimension | Assessment |
|---|---|
| Language/runtime fit | |
| Operational complexity | |
| Team ramp-up | |
| Migration cost | |
| Lock-in | |

**Summary**: <one sentence verdict for this specific stack>

## Top 3 production gotchas

1. **<Gotcha>**: <what happens, why, how to prevent or detect it>
2. **<Gotcha>**: <what happens, why, how to prevent or detect it>
3. **<Gotcha>**: <what happens, why, how to prevent or detect it>

## Strongest alternatives

| Alternative | When it wins over X |
|---|---|
| <Alt 1> | <condition> |
| <Alt 2> | <condition> |

## 3 things to watch

Things to monitor, re-evaluate, or follow up on as X evolves or as usage grows:

1. <thing to watch — e.g., "Project maturity: currently v0.9, watch for API stability in v1.0">
2. <thing to watch — e.g., "Ecosystem adoption: check in 6 months if managed hosting options have improved">
3. <thing to watch — e.g., "Org-fit: revisit if team grows beyond 10 engineers">

## Primary sources

- Docs: <URL>
- Repo: <URL>
- Best incident/post-mortem reference: <URL or "not found">
