---
name: architecture-lineage
description: Reconstruct why the system evolved the way it did by parsing ADRs, PR history, migration logs, and incident records. Use when asking "why does X exist?", "what broke last migration?", "what is risky to change?", or "how did the architecture get here?".
---

# Architecture Lineage

Recover the reasoning behind architectural decisions so agents don't repeat past mistakes or re-litigate settled choices.

## Quick start

```bash
# List ADRs
ls docs/adr/ 2>/dev/null || ls decisions/ 2>/dev/null || echo "No ADR directory found"

# Recent structural changes (new files added)
git log --oneline --diff-filter=A --name-only -- "*.md" "*.yaml" "*.json" | head -40

# Migration history (ordered)
find . -path "*/migrations/*" | sort | tail -20
```

## Workflow

1. **Parse ADRs** — extract decision, status, and `superseded-by` chain
2. **Parse PR history** — `git log --oneline` filtered for architecture keywords (introduce, migrate, replace, deprecate, move)
3. **Parse migration history** — ordered list with rollback notes
4. **Parse incident records** — post-mortems in `docs/incidents/` or linked issues
5. **Build evolution timeline** — chronological decisions with the trigger for each
6. **Flag active risks** — decisions that introduced known debt or caused past incidents

## Lineage query table

| Question | Source |
|---|---|
| Why does this service exist? | ADR + first PR |
| Why was X technology chosen? | ADR with status=accepted |
| What broke last migration? | Incident log + git blame |
| What is risky to modify? | Drift analysis + incident count |
| What changed in the last sprint? | `git log --since="2 weeks ago"` |

## ADR status chain

Follow the `superseded-by` links — a decision may have been overturned. Always report the _current_ accepted state, not the original.

## Drift detection

```bash
# High-churn files are high-risk files
git log --oneline -- "src/<module>/**" | wc -l
```

Flag any file with > 50 commits in the last 6 months as a high-risk touch point.

## Gotchas

- Absence of an ADR does not mean no decision — check PR titles and commit messages
- Superseded ADRs still explain why the current design looks the way it does — read them
- Incident lineage beats PR history for "what is risky" queries
- Technical debt comments in code (`// TODO`, `// HACK`, `// FIXME`) are lineage signals too
