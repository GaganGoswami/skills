---
name: knowledge-spike
description: Run a structured 30-minute learning sprint on any technology, RFC, pattern, or concept. Produces a reusable TIL card with key concepts, stack-fit analysis, gotchas, and 3 things to watch. Use when the user says "explain X to me", "I need to understand Y", "what is Z and should I use it", "spike on this", or needs to evaluate a technology for a real decision — not just general curiosity.
---

# Knowledge Spike

Learn precisely what you need to make a decision. No more, no less. Output is a reusable artefact, not a conversation.

## What this is not

- Not a tutorial — tutorials teach breadth; this targets decision-relevant depth
- Not a summary — summaries flatten tradeoffs; this sharpens them
- Not a recommendation without context — the output is stack-fit analysis, not a universal verdict

## Workflow

### Step 1 — Anchor the learning goal

Before exploring, ask: **"What decision will this knowledge enable?"**

| Decision type | Learning focus |
|---|---|
| Should we adopt X? | Tradeoffs, maturity, lock-in, alternatives |
| How do we implement X? | Core concepts, APIs, failure modes |
| Why is X behaving this way? | Internals, edge cases, known bugs |
| Is X right for our scale? | Performance characteristics, limits |

If the user hasn't stated the decision, infer it from context. State it explicitly before proceeding.

### Step 2 — Explore (fetch + reason)

For technologies and RFCs: fetch official docs, the GitHub repo README, and one credible comparison article. For patterns: reason from first principles using established CS/architecture knowledge.

Focus only on:
1. What problem does X solve, and what problem does it NOT solve?
2. What are the core 3–5 concepts that everything else builds on?
3. What does X assume about your environment (runtime, scale, team size, data shape)?
4. What are the top 3 failure modes users encounter in production?
5. What are the strongest alternatives and when do they win?

### Step 3 — Stack-fit analysis

Evaluate X against the user's current stack (infer from codebase context if not stated):

| Dimension | Assessment |
|---|---|
| **Language/runtime fit** | Native support? Idiomatic? Or bolted-on? |
| **Operational complexity** | What new infra or tooling does this require? |
| **Team ramp-up** | Days, weeks, or months to productive? |
| **Migration cost** | What would it replace? What does migration look like? |
| **Lock-in** | How hard is it to move away from X later? |

Rate overall fit: **Strong / Conditional / Weak**. One sentence explaining the rating.

### Step 4 — Produce the TIL card

See [TIL-FORMAT.md](TIL-FORMAT.md) for the exact output format. Fill all sections.

## Gotchas

- Don't let "understanding X" become a research rabbit hole — time-box to what the decision needs
- Vendor docs are optimistic; prioritize community posts, GitHub issues, and incident post-mortems for failure modes
- A "Weak" stack-fit rating is a useful output — it saves days of implementation before discovering the mismatch
- If the user is asking about a technology they've already chosen, focus the spike on failure modes and gotchas, not evaluation
- "I don't know enough about X to spike on it" is not a valid blocker — that's exactly when this skill applies
