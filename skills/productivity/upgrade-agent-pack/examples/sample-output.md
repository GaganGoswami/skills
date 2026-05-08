# Sample Output — Upgraded Agent-Pack Files (After Upgrade)

---

## File 1: `.github/agents/code-reviewer.agent.md` — UPGRADED

```markdown
---
name: code-reviewer
description: "Review code changes for correctness, security, and test coverage. Use when: reviewing PRs, patches, architectural refactors, or risky bug fixes."
argument-hint: PR number, branch name, or diff summary
tools: ["search/codebase", "web/fetch"]
model: ["Claude Opus 4.5"]
user-invocable: true
disable-model-invocation: false
---

You are a code reviewer. Review the provided diff or PR for issues and suggest fixes.
Always check for security vulnerabilities, missing tests, and style violations.
```

**Upgrade diff:**
```
+ added:   description trigger language ("Use when: ...")
+ added:   argument-hint
+ added:   user-invocable: true
+ added:   disable-model-invocation: false
~ changed: model: "Claude Opus 4.5" → ["Claude Opus 4.5"]
- removed: infer: true (deprecated)
```

---

## File 2: `.github/skills/summarize-diff/SKILL.md` — UPGRADED

```markdown
---
name: summarize-diff
description: "Summarize a unified diff into a structured component-by-component change list. Use when: generating PR descriptions, reviewing what changed in a patch, or auditing deleted public API surface."
argument-hint: Unified diff text or file path
user-invocable: true
disable-model-invocation: false
---

## Instructions

Given a unified diff, write a concise summary of what changed, grouped by component.
Format output as a bullet list with a one-sentence headline followed by changed files.
Flag any deleted public API surface.
```

**Upgrade diff:**
```
+ added:   description trigger language
+ added:   argument-hint
+ added:   user-invocable: true
+ added:   disable-model-invocation: false
- removed: context: fork (not needed; removed experimental field)
- removed: allowed-tools: shell (not needed for this skill)
```

**Created new modules:**

`prompt.md`:
```markdown
# Summarize Diff — Core Tasking Prompt

Produce a concise, component-grouped summary of the provided unified diff.

1. Parse the diff and identify changed files.
2. Group changes by logical component (e.g., "API layer", "tests", "config").
3. For each group, write: one headline sentence + list of changed files.
4. Flag any deleted or renamed public API surface at the top of the report.
5. Keep the total summary under 20 bullet points.
```

`instructions.md`:
```markdown
# Summarize Diff — Operating Instructions

- Accept unified diff text as input, or a file path pointing to a diff file.
- Always group changes by logical component, not by file type.
- Flag public API deletions in a dedicated "Breaking Changes" section.
- Keep each component group to one headline + file list; do not repeat diff content.
- Output in Markdown; use ## headings for each component group.
```

`hooks.md`:
```markdown
# Summarize Diff — Hook Intent

## Preflight
- Confirm the input is a unified diff (contains `---`, `+++`, `@@` markers).
- Check input length; warn if diff exceeds 2000 lines (large diffs may truncate summaries).

## Completion
- Confirm every changed file appears in at least one component group.
- Output the summary followed by: "Total: X files changed across Y components."
```

---

## File 3: `codex/skills/summarize-diff/SKILL.md` — UPGRADED

```markdown
---
name: summarize-diff
description: "Summarize a unified diff into a structured component-by-component change list. Use when: generating PR descriptions, reviewing what changed in a patch, or auditing deleted API surface."
---

Summarize the provided diff into a clear bullet list grouped by component.
```

**Upgrade diff:**
```
+ added:   description trigger language
- removed: user-invocable: true (Codex: not a valid field)
- removed: disable-model-invocation: false (Codex: not a valid field)
- removed: context: fork (Codex: not a valid field)
```

---

## File 4: `.claude/agents/code-reviewer.md` — UPGRADED

```markdown
---
name: code-reviewer
description: "Review code changes for correctness, security, and test coverage. Use when: reviewing PRs, patches, or any diff that will be merged into main."
tools: [Read, Glob, Grep, Bash]
disallowedTools: []
model: sonnet
permissionMode: default
maxTurns: 15
isolation: workspace
color: blue
---

Review the provided diff for bugs, security issues, and missing test coverage.
Produce a structured report with sections: Summary, Issues, Recommendations.
```

**Upgrade diff:**
```
+ added:   description trigger language
+ added:   model: sonnet
+ added:   permissionMode: default
+ added:   maxTurns: 15
+ added:   isolation: workspace
+ added:   color: blue
- removed: Write from tools[] (conflicts with disallowedTools)
- removed: Write from disallowedTools[] (Write removed from tools, so disallowedTools entry is now empty)
```

---

## File 5: `.kiro/agents/code-reviewer.md` — UPGRADED

```markdown
---
name: code-reviewer
description: "Review code changes for correctness, security, and test coverage. Use when: reviewing PRs, patches, Terraform plans, or any change going to a protected branch."
tools: ["read", "shell"]
model: claude-sonnet-4
includeMcpJson: true
includePowers: false
---

Review code changes for correctness and security.
```

**Upgrade diff:**
```
+ added:   description trigger language
+ added:   tools: ["read", "shell"]
+ added:   model: claude-sonnet-4
+ added:   includeMcpJson: true
+ added:   includePowers: false
- removed: user-invocable: false (Copilot field — not valid for Kiro)
- removed: allowed-tools: shell (Copilot field — not valid for Kiro)
```

---

## Upgrade Summary Report

```
UPGRADED: .github/agents/code-reviewer.agent.md
  + added:   description trigger language
  + added:   argument-hint
  + added:   user-invocable: true
  + added:   disable-model-invocation: false
  ~ changed: model → array format
  - removed: infer (deprecated)

UPGRADED: .github/skills/summarize-diff/SKILL.md
  + added:   description trigger language
  + added:   argument-hint
  + added:   user-invocable: true
  + added:   disable-model-invocation: false
  - removed: context: fork
  - removed: allowed-tools: shell

CREATED: .github/skills/summarize-diff/prompt.md
CREATED: .github/skills/summarize-diff/instructions.md
CREATED: .github/skills/summarize-diff/hooks.md

UPGRADED: codex/skills/summarize-diff/SKILL.md
  + added:   description trigger language
  - removed: user-invocable, disable-model-invocation, context (invalid Codex fields)

UPGRADED: .claude/agents/code-reviewer.md
  + added:   description trigger language, model, permissionMode, maxTurns, isolation, color
  - removed: Write from both tools[] and disallowedTools[] (conflict resolved)

UPGRADED: .kiro/agents/code-reviewer.md
  + added:   description trigger language, tools, model, includeMcpJson, includePowers
  - removed: user-invocable, allowed-tools (Copilot-specific fields)

Upgrade complete: 5 files upgraded, 3 files created, 0 files skipped, 0 errors.

Next steps:
  - Run: node scripts/pipeline/lint-prompts.mjs
  - Run: node scripts/pipeline/render-platform-assets.mjs  (if any .agents/ sources were changed)
```
