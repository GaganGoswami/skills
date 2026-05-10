---
name: prompt-coach
description: Score prompt quality on clarity, specificity, actionability, and scope. Surface targeted improvements before low-quality prompts cause clarification round-trips. Use when the user asks "is my prompt good?", "how can I improve this?", or auto-trigger when a prompt scores below 6/10 and is likely to cause agent confusion.
---

# Prompt Coach

Score prompts and return targeted improvements before they waste tokens on clarification loops.

## Scoring dimensions (each 0–10)

| Dimension | What it measures |
|---|---|
| Clarity | Is the request unambiguous? One interpretation only. |
| Specificity | File paths, error messages, line numbers present? |
| Actionability | Can the agent act immediately without asking questions? |
| Scope | Appropriately sized for one session? |

**Trigger threshold**: overall average < 6 → surface improvements before proceeding.

## Scoring rubric

**Clarity** — 10: one interpretation; 5: two plausible reads; 0: completely vague ("make it better")

**Specificity** — 10: file + line + error + expected vs actual; 5: file named, no line/error; 0: "the login thing is broken"

**Actionability** — 10: agent has everything to start; 5: one missing piece; 0: agent must ask 3+ questions

**Scope** — 10: one focused task; 5: two related tasks; 0: "refactor the whole auth system"

## Improvement template

```
Prompt scored {N}/10.
- Add: {what's missing}
- Specify: {what's ambiguous}
- Stronger version: {rewritten prompt}
```

Always provide the rewritten example — abstract advice without a model is useless.

## Exceptions (brief prompts that are acceptable)

- `"git commit"` — agent has environment context
- `"run tests"` — agent knows the test command
- `"fix it"` — immediately after the agent identified the issue itself
- `"now do X"` — follows a just-completed task in the same session

## Gotchas

- Don't penalize scope when the user owns a known large refactor session — context matters
- Coaching should take < 5 lines; don't pad with warnings the user already knows
- If the prompt is ambiguous but the agent can infer the correct interpretation from file context, proceed and note the inference — don't block on coaching
