# AGENTS.md

Guidance for AI agents working in this repository.

## Agent skills

This repo ships 13 agent skills in two categories. Install via:

```bash
npx skills@latest add gagangoswami/skills
```

### Engineering skills

| Skill | Path | Purpose |
|---|---|---|
| `debug` | `skills/engineering/debug/` | Disciplined bug diagnosis loop |
| `plan-with-me-with-docs` | `skills/engineering/plan-with-me-with-docs/` | Structured planning that writes CONTEXT.md and ADRs |
| `arch-audit` | `skills/engineering/arch-audit/` | Architecture audit with deepening opportunities |
| `init-skills` | `skills/engineering/init-skills/` | Bootstrap domain docs and issue tracker for a new repo |
| `tdd` | `skills/engineering/tdd/` | Red-green-refactor TDD loop |
| `to-tasks` | `skills/engineering/to-tasks/` | Break a plan into independently-grabbable issues |
| `to-prd` | `skills/engineering/to-prd/` | Turn conversation context into a PRD |
| `triage` | `skills/engineering/triage/` | Triage issues through a state machine |
| `big-picture` | `skills/engineering/big-picture/` | Zoom out to see system-level structure |
| `plan-and-build-with-me` | `skills/engineering/plan-and-build-with-me/` | tep-by-step guided build-and-learn sessions |

### Productivity skills

| Skill | Path | Purpose |
|---|---|---|
| `token-saver` | `skills/productivity/token-saver/` | Ultra-compressed communication mode |
| `plan-with-me` | `skills/productivity/plan-with-me/` | Relentless interview to stress-test a plan |
| `forge-skill` | `skills/productivity/forge-skill/` | Create new agent skills |

### Issue tracker

Issues live as local markdown files under `.scratch/<feature-slug>/`. See `docs/agents/issue-tracker.md`.

### Triage labels

Default label vocabulary (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context layout — one `CONTEXT.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.
