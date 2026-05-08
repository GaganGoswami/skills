# Sample Input — Stale Agent-Pack Files (Before Upgrade)

These files represent a realistic before-state. Each has one or more compliance issues.

---

## File 1: `.github/agents/code-reviewer.agent.md`

```markdown
---
name: code-reviewer
description: Reviews code.
infer: true
model: "Claude Opus 4.5"
---

You are a code reviewer. Review the provided diff or PR for issues and suggest fixes.
Always check for security vulnerabilities, missing tests, and style violations.
```

**Issues to fix:**
- `description` is too short and lacks `"Use when: ..."` trigger language
- Deprecated `infer: true` field must be removed
- `model` must be an array: `["Claude Opus 4.5"]`
- Missing: `user-invocable`, `disable-model-invocation`, `argument-hint`

---

## File 2: `.github/skills/summarize-diff/SKILL.md`

```markdown
---
name: summarize-diff
description: Summarizes diffs.
context: fork
allowed-tools: shell
---

## Instructions

Given a unified diff, write a concise summary of what changed, grouped by component.
Format output as a bullet list with a one-sentence headline followed by changed files.
Flag any deleted public API surface.
```

**Issues to fix:**
- `description` lacks trigger language
- Missing: `user-invocable`, `disable-model-invocation`
- `context: fork` is experimental; keep only if fork access is genuinely required
- Missing: `prompt.md`, `instructions.md`, `hooks.md` — all absent from folder

---

## File 3: `codex/skills/summarize-diff/SKILL.md`

```markdown
---
name: summarize-diff
description: Summarizes diffs.
user-invocable: true
disable-model-invocation: false
context: fork
---

Summarize the provided diff into a clear bullet list grouped by component.
```

**Issues to fix:**
- `user-invocable`, `disable-model-invocation`, `context` are not valid Codex frontmatter fields — strip them
- `description` lacks trigger language

---

## File 4: `.claude/agents/code-reviewer.md`

```markdown
---
name: code-reviewer
description: Reviews code.
tools: [Read, Grep, Write, Bash]
disallowedTools: [Write]
---

Review the provided diff for bugs, security issues, and missing test coverage.
Produce a structured report with sections: Summary, Issues, Recommendations.
```

**Issues to fix:**
- `Write` appears in both `tools` and `disallowedTools` — remove from `disallowedTools` (or `tools`)
- Missing: `model`, `permissionMode`, `maxTurns`, `isolation`
- `description` lacks trigger language

---

## File 5: `.kiro/agents/code-reviewer.md`

```markdown
---
name: code-reviewer
description: Reviews code.
user-invocable: false
allowed-tools: shell
---

Review code changes for correctness and security.
```

**Issues to fix:**
- `user-invocable` and `allowed-tools` are Copilot-specific fields — remove them
- Add Kiro-appropriate fields: `tools`, `model`, `includeMcpJson`
- `description` lacks trigger language
