# skills

A collection of agent skills for GitHub Copilot and compatible AI agents.

## Install

```bash
npx skills@latest add gagangoswami/skills
```

This installs all 12 skills into your agent's skill directory (e.g. `.agents/skills/`).

To install a single skill:

```bash
npx skills@latest add gagangoswami/skills/skills/engineering/debug
```

## Skills

### Engineering

| Skill | What it does |
|---|---|
| `debug` | Disciplined bug diagnosis — reproduce, minimise, hypothesise, instrument, fix, regression-test |
| `plan-with-me-with-docs` | Structured planning session that produces a `CONTEXT.md` and ADR records |
| `arch-audit` | Audit a codebase for deepening opportunities — coupling, testability, module depth |
| `init-skills` | Bootstrap a new repo: domain docs, issue tracker config, triage labels |
| `tdd` | Red-green-refactor TDD loop with guidance on interfaces, mocking, and tests |
| `to-tasks` | Break a plan or PRD into independently-grabbable vertical slice issues |
| `to-prd` | Turn the current conversation context into a publishable PRD |
| `triage` | Triage incoming issues through a state machine with agent briefs |
| `big-picture` | Zoom out to understand system structure before diving into a feature |

### Productivity

| Skill | What it does |
|---|---|
| `token-saver` | Ultra-compressed communication — drops filler while keeping full technical accuracy |
| `plan-with-me` | Relentless interview to stress-test a plan or design |
| `forge-skill` | Create new agent skills with proper structure and bundled resources |

## Customise

After installing, edit any skill file in `.agents/skills/<name>/SKILL.md` to adjust the description or add project-specific context.

To override companion docs (e.g. `CONTEXT-FORMAT.md`, `ADR-FORMAT.md`), copy the file into the skill directory and edit it — the local copy takes precedence.

## Structure

```
skills/
  engineering/
    debug/
    plan-with-me-with-docs/
    arch-audit/
    init-skills/
    tdd/
    to-tasks/
    to-prd/
    triage/
    big-picture/
  productivity/
    token-saver/
    plan-with-me/
    forge-skill/
```

Each skill directory contains a `SKILL.md` and any companion resource files referenced by the skill.
