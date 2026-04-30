# Out of Scope

The `.out-of-scope/` directory stores records of deliberately rejected feature concepts. It prevents the same request from being relitigated every time a new issue arrives.

## File layout

```
.out-of-scope/
  auto-truncation.md
  dark-mode.md
  plugin-system.md
```

One file per **concept**, not per issue. Kebab-case name matching the concept.

## File format

```markdown
# Concept Name

Explanation of why this is out of scope. Should be substantive:
- A scope or philosophy reason ("This tool is intentionally read-only")
- A technical constraint ("Requires a daemon process; we ship a CLI")
- A strategic decision ("Deferred until v2 is stable")

NOT: "Too busy right now" or "Not a priority" — these invite revisiting.

## Prior requests

- #12 — Auto-truncate skill descriptions over the limit
- #34 — Silently clamp long inputs instead of erroring
```

## When to check

During triage Step 1, before categorizing a new issue: search `.out-of-scope/` for files whose name or content matches the concept. If a match is found, the issue is a duplicate of a wontfix decision.

## When to create

Only when an enhancement is rejected as `wontfix`. Don't create preemptively.

## When to update

Append to `## Prior requests` when a new issue matches an existing concept.

## When to delete

When the maintainer reverses the decision — delete the file so future requests aren't incorrectly blocked.

## Flow

```
New enhancement issue
       ↓
Check .out-of-scope/ for concept match
       ↓
  Match found?
  YES → append to Prior requests → post comment explaining decision → close with wontfix
  NO  → continue normal triage
       ↓
  Issue ultimately rejected as wontfix?
  YES → create .out-of-scope/<concept>.md (or append if concept file exists)
  NO  → no .out-of-scope/ action needed
```
