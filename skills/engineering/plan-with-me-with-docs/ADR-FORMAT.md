# ADR Format

ADRs (Architecture Decision Records) live in `docs/adr/`, numbered sequentially: `0001-short-slug.md`.

## Template

```markdown
# {Short title}

{1–3 sentences: what the context was, what was decided, and why.}
```

Optional sections — add only when they add value:

**`status:`** frontmatter (e.g. `status: accepted`) — useful when a decision may be superseded or is still proposed.

**Considered Options** — only when the rejected alternatives are worth remembering. If there was only one realistic choice, skip this section.

**Consequences** — only when the trade-offs are non-obvious. If they're self-evident from the decision, skip this section.

## When to offer an ADR

Only offer to write an ADR when **all three** of the following are true:

1. **Hard to reverse** — changing your mind later has a real cost
2. **Surprising without context** — a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off** — there were genuine alternatives and you chose one for specific reasons

If any one of the three is missing, skip the ADR.

## What qualifies

- Architectural shape choices (event-sourced vs CRUD, monolith vs services)
- Integration patterns (webhook vs polling, sync vs async)
- Technology choices with meaningful lock-in
- Scope and boundary decisions ("the billing context owns payment state")
- Deliberate deviations from the obvious approach
- Constraints that are invisible in the code
- Rejected alternatives with non-obvious reasons

## What doesn't qualify

- Anything reversible in an afternoon
- Standard patterns the team uses everywhere
- Decisions where there was only one realistic choice
- Implementation details that belong in code comments
