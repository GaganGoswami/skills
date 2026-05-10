# Multi-Agent Orchestrator — Reference

## DAG scheduling

Build the task dependency graph before dispatching any agent.

```
DB schema migration
       ↓
Backend API (depends on schema)
       ↓
Frontend UI (depends on API contract)

Test setup ← runs in parallel with DB migration
Security audit ← runs in parallel, read-only
```

**Scheduling rules**:
1. Nodes with no inbound edges run immediately (parallel wave 1)
2. A node becomes runnable once all its dependencies complete
3. Wave N+1 starts only when all runnable wave-N tasks finish or are recovered

## Shared memory bus

All agents read from and write to `.agents/memory/` during the run.

| File | Owner | Access |
|---|---|---|
| `task-state.json` | Orchestrator | Write; agents read-only |
| `architecture.md` | Pre-populated | All read-only during run |
| `service-graph.json` | Pre-populated | All read-only during run |
| `<task-N>-output.md` | Task-N agent | Its own writes; others read after task completes |

**Rule**: no agent writes shared memory while another agent depends on it. Orchestrator gates access.

## Conflict resolution engine

Step-by-step for any file appearing in 2+ worktrees:

1. **Ownership check** — does CODEOWNERS assign the file to one team?
   - Yes → that team's agent owns the canonical version; other changes are patches
2. **Semantic diff** — are the changes logically compatible (different functions/blocks)?
   - Yes → merge automatically using 3-way merge
3. **Incompatible changes** — same lines, different semantics
   - Escalate to human review; block PR until resolved
   - Attach both versions with a diff summary to the PR

## Recovery engine

```
Task N fails
    ↓
Is it a leaf node (no dependents)?
    Yes → skip, flag in PR description, continue merge
    No  → spawn recovery agent with 50% scope (smallest reproducible subtask)
           if recovery succeeds → re-enter DAG at Task N
           if recovery fails    → mark subtree blocked; report in PR
```

Max 1 recovery attempt per task. Never retry indefinitely — it burns tokens and masks root causes.

## Runtime monitoring checklist

Orchestrator tracks per task:
- [ ] Started / in-progress / complete / failed / recovered
- [ ] Token count (soft warn at 80k, hard abort at 200k)
- [ ] Wall-clock time (warn at 8 min, abort at 10 min)
- [ ] CRITICAL findings (security scan, compliance rule) → abort all immediately

## Evaluation layer

Before opening the PR, run:

1. **Test suite** — full affected-module tests + integration tests on merged branch
2. **Architecture alignment** — does the merged diff contradict any active ADR?
3. **Coverage delta** — did any agent reduce coverage below the baseline?
4. **Policy scan** — re-run security agent on the merged diff (not per-worktree)

Gate the PR on: tests green + no ADR contradiction + coverage maintained.

## PR generation

One PR per orchestration run. Contents:

```markdown
## Summary
{one-paragraph description of what the swarm built}

## Tasks completed
- Task 1: {description} ✅
- Task 2: {description} ✅
- Task 3: {description} ⚠️ partial (recovery applied)

## Blocked / skipped
- Task 4: {reason} — manual review needed

## Architecture decisions made
- {any new patterns introduced, linked to relevant ADRs}

## Test results
- {suite}: {pass/fail}, coverage: {N}%
```
