# AGENTS.md

Guidance for AI agents working in this repository.

## Agent skills

This repo ships 26 agent skills in two categories. Install via:

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
| `plan-and-build-with-me` | `skills/engineering/plan-and-build-with-me/` | Step-by-step guided build-and-learn sessions |
| `repo-intelligence` | `skills/engineering/repo-intelligence/` | Build service graphs, API maps, and dependency analysis |
| `semantic-memory` | `skills/engineering/semantic-memory/` | Compress repos into layered summaries for agent retrieval |
| `architecture-lineage` | `skills/engineering/architecture-lineage/` | Reconstruct why the system evolved — ADRs, PR history, incidents |
| `skill-factory` | `skills/engineering/skill-factory/` | Capture session patterns as permanent reusable skills |
| `prompt-coach` | `skills/engineering/prompt-coach/` | Score and improve prompts before they cause clarification loops |
| `multi-agent-orchestrator` | `skills/engineering/multi-agent-orchestrator/` | Parallel subagent tasks in isolated worktrees with merge validation |
| `ai-architecture` | `skills/engineering/ai-architecture/` | Design AI-native systems: patterns, models, memory, evaluation, security |
| `assumption-hunter` | `skills/engineering/assumption-hunter/` | Surface hidden assumptions in plans, designs, and code before they cause rework |
| `first-principles` | `skills/engineering/first-principles/` | Deconstruct any problem to irreducible truths and rebuild from scratch |
| `decision-cascade` | `skills/engineering/decision-cascade/` | Map 2nd and 3rd order consequences of a decision before committing |
| `knowledge-spike` | `skills/engineering/knowledge-spike/` | Structured 30-minute learning sprint with reusable TIL card output |
| `session-handoff` | `skills/engineering/session-handoff/` | Package session state as a structured brief for zero-warmup resumption |

### Productivity skills

| Skill | Path | Purpose |
|---|---|---|
| `token-saver` | `skills/productivity/token-saver/` | Ultra-compressed communication mode |
| `plan-with-me` | `skills/productivity/plan-with-me/` | Relentless interview to stress-test a plan |
| `forge-skill` | `skills/productivity/forge-skill/` | Create new agent skills |
| `idea-accelerator` | `skills/productivity/idea-accelerator/` | SCAMPER + inversion diverge→converge loop to generate and stress-test 10 idea variants |

### Issue tracker

Issues live as local markdown files under `.scratch/<feature-slug>/`. See `docs/agents/issue-tracker.md`.

### Triage labels

Default label vocabulary (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context layout — one `CONTEXT.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.
