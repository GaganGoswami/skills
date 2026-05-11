---
name: idea-accelerator
description: Rapid idea generation engine. Apply SCAMPER, inversion, forced analogy, and random entry in a structured diverge→converge loop. Use when the user has a seed idea and wants to expand it, says "give me variations", "brainstorm", "I need ideas for X", "what else could this be", or is stuck in a local maximum and wants a creative reset.
---

# Idea Accelerator

Break out of local maxima. Generate 10 idea variants in one pass, then converge on the 2 strongest.

## Protocol

### Phase 1 — Anchor (60 seconds)

State the seed idea back as a single sentence:

> "The core idea is: **[X]** — a **[what]** that helps **[who]** do **[outcome]**."

If the user's idea is vague, ask ONE clarifying question — the most load-bearing one only — then proceed.

### Phase 2 — Diverge (main loop)

Apply all 7 lenses from [SCAMPER.md](SCAMPER.md) in sequence. Generate at least one variant per lens. Label each with its lens tag.

Also run two wild-card lenses:

| Lens | Question |
|---|---|
| **Inversion** | What if you built the exact opposite? Who benefits from the problem NOT being solved? |
| **Random entry** | Pick an unrelated domain (nature, cooking, military, architecture). What would that domain do with this problem? |

Target: ≥ 10 variants across all lenses. Compress each to one sentence.

### Phase 3 — Converge

Rank all variants on three axes (score 1–5 each):

| Axis | What it measures |
|---|---|
| **Distinctiveness** | How different is this from the original idea and from each other? |
| **Feasibility** | Can this be prototyped in < 2 weeks? |
| **Leverage** | Does this unlock a bigger opportunity or solve a harder problem? |

Pick the **top 2** by total score. Present them as: `Variant A (score)` and `Variant B (score)`.

### Phase 4 — Stress-test top 2

For each winner, run the 3-question kill test from [STRESS-TEST.md](STRESS-TEST.md):

1. What would have to be true for this to completely fail?
2. Who already does something similar and why haven't they succeeded?
3. What is the riskiest assumption — and can you test it this week?

### Phase 5 — Output

Return a compact card:

```
SEED: <original idea>

TOP 2 VARIANTS:
A. <variant> [score: X/15] — Riskiest assumption: <assumption>
B. <variant> [score: X/15] — Riskiest assumption: <assumption>

WILD CARD (keep for later): <most surprising variant from diverge phase>

NEXT ACTION: <single lowest-cost, highest-information experiment to run first>
```

## Gotchas

- Don't collapse into safe variations of the original — the goal is surface area, not polish
- If all 10 variants cluster around the same theme, force at least one inversion
- Feasibility scores are about the *prototype*, not the full product — don't kill ideas on scale problems before the idea is validated
- The wild card is often the best idea in the room — don't discard it just because it scored lower
- Do NOT generate options for options — each variant must be a complete idea, not a sub-choice

## Trigger phrases

"brainstorm", "give me alternatives", "what else could this be", "I'm stuck", "variants", "10 ideas", "creative reset", "expand this", "ideate"
