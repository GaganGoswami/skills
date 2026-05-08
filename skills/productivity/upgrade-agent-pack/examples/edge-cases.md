# Edge Cases — Upgrade Agent Pack

---

## Edge Case 1 — Kiro IDE vs Kiro CLI (two separate files)

**Problem**: A single canonical `.agents/agents/planner.md` needs to render both a Kiro IDE subagent (`.kiro/agents/planner.md`) and a Kiro CLI agent (`.kiro/agents/planner.json`). These are structurally different formats.

**Incorrect approach** — overwriting the IDE file with JSON:
```
# DO NOT write JSON to planner.md
.kiro/agents/planner.md → ❌ written as JSON
```

**Correct approach** — produce two separate files:

`.kiro/agents/planner.md` (Kiro IDE YAML frontmatter):
```markdown
---
name: planner
description: "Generate a phased implementation plan from a product brief. Use when: planning a sprint, breaking down an epic, or preparing a handoff document."
tools: ["read", "shell"]
model: claude-sonnet-4
includeMcpJson: true
includePowers: false
---
```

`.kiro/agents/planner.json` (Kiro CLI JSON):
```json
{
  "name": "planner",
  "description": "Generate a phased implementation plan from a product brief.",
  "prompt": "file://./../prompts/planner-prompt.md",
  "tools": ["read", "shell"],
  "allowedTools": ["read"],
  "model": "claude-sonnet-4",
  "includeMcpJson": true,
  "welcomeMessage": "Ready to plan. Provide your brief.",
  "mcpServers": {},
  "toolAliases": {},
  "toolsSettings": {},
  "resources": [],
  "hooks": {}
}
```

**Rule**: Always create both files for Kiro platform targets. Never merge them.

---

## Edge Case 2 — Claude `disallowedTools` conflict

**Problem**: An agent needs `Write` for creating reports but also appeared in `disallowedTools` from a previous copy-paste error.

**Before (conflicting):**
```yaml
tools: [Read, Glob, Grep, Write, Bash]
disallowedTools: [Write, Bash]
```

**Detection**: `Write` appears in both lists.

**Resolution policy**:
- If the agent body says "generate files", "write reports", or "create" → keep in `tools`, remove from `disallowedTools`
- If the agent body says "read-only", "no file creation", or "audit" → keep in `disallowedTools`, remove from `tools`
- If ambiguous → flag for manual review; do not auto-resolve

**After (resolved for a write-capable agent):**
```yaml
tools: [Read, Glob, Grep, Write, Bash]
disallowedTools: []
```

---

## Edge Case 3 — Codex field stripping breaks the skill body

**Problem**: A skill has critical guidance encoded inside frontmatter fields (e.g., a list of rules in a custom `allowed-tools` value). When stripping to Codex minimum, content would be lost.

**Before:**
```yaml
---
name: api-reviewer
description: Reviews API contracts.
allowed-tools: |
  openapi-lint
  schema-compare
  diff-highlighter
---
```

**Correct resolution**: Move the content into the Markdown body before stripping frontmatter:

**After:**
```yaml
---
name: api-reviewer
description: "Review OpenAPI contract changes for breaking changes and schema drift. Use when: comparing two versions of an OpenAPI spec, reviewing API PRs, or auditing schema consistency."
---

## Tools Used

The following tools may be invoked during API review:
- `openapi-lint` — validate spec structure
- `schema-compare` — detect breaking changes
- `diff-highlighter` — format diff output
```

**Rule**: Never drop field content without checking whether it contains guidance that belongs in the body.

---

## Edge Case 4 — Empty body after frontmatter migration

**Problem**: The original file had only frontmatter and a one-line description. After stripping extra fields, the body is empty.

**Before:**
```yaml
---
name: linter
description: Lints code.
user-invocable: true
allowed-tools: shell
hint: Run ESLint, Prettier, and custom rules.
---
```

**After incorrect stripping (body empty):**
```yaml
---
name: linter
description: Lints code.
user-invocable: true
disable-model-invocation: false
---
```

**Correct resolution**: Lift the `hint` value into a body stub:

```yaml
---
name: linter
description: "Run ESLint, Prettier, and project-specific lint rules on the target files. Use when: running pre-commit checks, reviewing a PR for style issues, or validating a fresh scaffold."
user-invocable: true
disable-model-invocation: false
---

Run ESLint, Prettier, and custom rules on the provided file or directory.
Report all violations grouped by rule, with file + line references.
```

**Rule**: A `SKILL.md` must have at least a one-paragraph body after frontmatter. Generate a stub from `hint`, `argument-hint`, or the description if the body is missing.

---

## Edge Case 5 — `description` exceeds 1024 characters

**Problem**: A description was copy-pasted from a README and is several paragraphs long.

**Detection**: Count characters in the `description` value; flag if `len(description) > 1024`.

**Resolution**:
1. Move the expanded description into the Markdown body as a `## Overview` section.
2. Write a new short `description` following the template: `<Verb> <domain noun>. Use when: <trigger-1>, <trigger-2>.`

**Before (truncated example):**
```yaml
description: "This skill provides comprehensive support for reviewing Java Spring Boot
  applications, including REST endpoint analysis, JPA entity validation, security
  configuration audit, Maven dependency review, test coverage assessment, and
  integration with SonarQube. It is designed for teams that need deep, multi-layer
  code review across large enterprise codebases with hundreds of controllers and
  service beans. [... continues for 400 more characters]"
```

**After:**
```yaml
description: "Review Java Spring Boot applications for REST correctness, JPA safety, security configuration, and Maven dependency health. Use when: auditing a Spring Boot service, reviewing a major refactor, or running a pre-release quality gate."
```

Body gets new section:
```markdown
## Overview

This skill provides comprehensive support for reviewing Java Spring Boot applications,
including REST endpoint analysis, JPA entity validation, security configuration audit,
Maven dependency review, and test coverage assessment.
```

---

## Edge Case 6 — Deprecated `infer` field on Copilot agents

**Problem**: Older Copilot agent files use `infer: true` to control model invocation. This field is deprecated.

| Old field | Replacement |
|---|---|
| `infer: true` | `disable-model-invocation: false` |
| `infer: false` | `disable-model-invocation: true` |

**Resolution**: Replace automatically with the mapped value. Do not leave `infer` in the output.

---

## Edge Case 7 — Multi-platform canonical source with platform-specific overrides

**Problem**: `.agents/skills/db-schema-review/SKILL.md` is the canonical source. It needs to render correctly for both Copilot (needs `user-invocable`) and Codex (must not have `user-invocable`).

**Rule**: The canonical `.agents/` source may include all supported fields from any platform. The `render-platform-assets.mjs` script strips platform-incompatible fields when generating mirrors. Do NOT manually pre-strip fields from canonical sources.

**Correct canonical source** (includes all fields; the render script handles stripping per platform):
```yaml
---
name: db-schema-review
description: "Review database schema changes for correctness, migration safety, and index efficiency. Use when: reviewing Flyway migrations, JPA entity changes, or schema PRs."
user-invocable: true
disable-model-invocation: false
relatedSkills: [java-spring-boot, performance-optimization]
---
```
