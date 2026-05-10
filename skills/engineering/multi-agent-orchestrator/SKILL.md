---
name: multi-agent-orchestrator
description: Decompose large cross-cutting changes into a DAG of parallel subagent tasks in isolated git worktrees with conflict resolution, recovery, and merge validation. Use when a change spans 3+ bounded contexts, touches 10+ files, requires an agent swarm, or sequential execution is too slow.
---

# Multi-Agent Orchestrator

Coordinate autonomous agent swarms: decompose → build DAG → dispatch in parallel → resolve conflicts → recover failures → merge → PR.

## When to invoke

- Change spans ≥ 3 bounded contexts, OR
- Plan has ≥ 10 files to modify, OR
- Tasks are clearly independent (no shared file edits)

## Workflow

### 1. Agent registry

Declare specialised agents for the run:

```yaml
agents:
  backend:  { context: src/api/, tools: [bash, test] }
  frontend: { context: src/ui/, tools: [bash, test] }
  db:       { context: src/db/, tools: [bash, migrate] }
  test:     { context: tests/, tools: [bash] }
  security: { context: "*", tools: [read], readonly: true }
```

### 2. Decompose into DAG

Read the plan. Build a dependency graph — tasks sharing no edited files run in parallel; dependent tasks run sequentially within a lane.

**Conflict check**: list every file each task will touch. Any file appearing in 2+ lanes must be moved into a sequential merge task.

### 3. Worktree setup

```bash
for N in 1 2 3; do
  git worktree add .worktrees/task-$N -b task/ticket-$N
done
```

### 4. Dispatch and monitor

Each subagent receives only its task slice and bounded context files. Orchestrator monitors:
- task completion / timeout
- token consumption
- CRITICAL compliance findings (abort all on detection)

### 5. Conflict resolution

Before merge, run semantic diff across worktrees. For any overlapping change:
1. Prefer the task with file ownership per CODEOWNERS
2. If no owner, escalate to human review before merging

### 6. Recovery

On subagent failure: spawn a recovery agent with reduced scope for that task only. Max 1 retry. If retry fails, report and skip — do not block the rest of the merge.

### 7. Merge, evaluate, PR

```bash
# Merge all lanes into integration branch
# Run full test suite
# If green → open one PR with consolidated changelog
# If red → report failing task; do not merge
```

## Guardrails

- Max 8 parallel subagents; 10-minute timeout per task
- Abort all if any agent hits a CRITICAL security or compliance finding
- One PR per orchestration run
- Never merge directly to main — always use an integration branch

## Gotchas

- Use `git worktree remove`, never `rm -rf .worktrees/`
- Run affected-module tests per lane before the full suite
- Shared memory (`.agents/memory/`) is read-only during parallel execution; writes happen only after merge

## Advanced

See [REFERENCE.md](REFERENCE.md) for DAG scheduling, shared memory bus, evaluation engine, and PR generation patterns.
