---
name: upgrade-agent-pack
description: "Upgrade agents, skills, prompts, instructions, and hooks to match latest cross-platform frontmatter schemas and best practices. Use when: migrating existing agent/skill files to current spec, fixing stale frontmatter fields, adding missing prompt.md / instructions.md / hooks.md modules, auditing cross-platform portability (GitHub Copilot, Claude Code, Codex, Kiro), or aligning file layout with the canonical agent-pack structure."
user-invocable: true
disable-model-invocation: false
relatedSkills: [forge-skill, agent-customization, validation-and-qa]
---

# Upgrade Agent Pack Skill

## When to Use

- An agent or skill was authored before the cross-platform spec in `Agent-Skill-Prompt-metadata.md`
- Frontmatter fields are missing, misspelled, or from a deprecated schema
- `prompt.md`, `instructions.md`, or `hooks.md` modules are absent from a skill folder
- A skill or agent needs to run on a new platform (e.g., adding Kiro IDE or Codex support)
- The `Agent-Skill-Prompt-metadata.md` spec was updated and existing files need to be synchronized
- Audit is needed to check portability across GitHub Copilot, Claude Code, Codex, and Kiro

---

## Platform Frontmatter Schemas

Read `Agent-Skill-Prompt-metadata.md` as the authoritative source. The tables below are the validated minimums per platform.

### GitHub Copilot — `.agent.md`

```yaml
# Required
name: <string>
description: <string>           # one sentence, specific trigger language

# Common optional
argument-hint: <string>
tools: [<string>, ...]          # e.g. "search/codebase", "web/fetch"
agents: [<string>, ...]
model: [<string>, ...]          # e.g. "Claude Opus 4.5", "GPT-5.2"
user-invocable: true | false
disable-model-invocation: true | false
target: vscode | cloud
mcp-servers: []
handoffs:
  - label: <string>
    agent: <string>
    prompt: <string>
    send: true | false
    model: <string>
hooks: {}
```

### GitHub Copilot — `SKILL.md`

```yaml
# Required
name: <string>
description: <string>

# Optional
argument-hint: <string>
user-invocable: true | false
disable-model-invocation: true | false
context: fork | workspace
license: MIT | Apache-2.0 | ...
allowed-tools: shell | ...
```

### Claude Code — agent `.md`

```yaml
# Required
name: <string>
description: <string>

# Optional
tools: [Read, Glob, Grep, Bash, Write, ...]
disallowedTools: [Write, ...]
model: sonnet | opus | haiku
prompt: <relative-path-to-prompt.md>
permissionMode: default | restricted | full
mcpServers: []
hooks: {}
maxTurns: <int>
skills: []
initialPrompt: ""
memory: true | false
effort: low | medium | high
background: true | false
isolation: workspace | repo
color: blue | green | red | ...
```

### Codex — `SKILL.md`

```yaml
# Required only
name: <string>
description: <string>
# No other frontmatter fields are officially documented — keep minimal
```

### Kiro IDE — agent `.md`

```yaml
# Required
name: <string>

# Optional
description: <string>
tools: ["read", "shell", "@context7", ...]
model: claude-sonnet-4 | ...
includeMcpJson: true | false
includePowers: true | false
```

### Kiro CLI — `agent.json`

```json
{
  "name": "<string>",
  "description": "<string>",
  "prompt": "file://./../prompts/<name>-prompt.md",
  "mcpServers": {},
  "tools": ["read", "shell"],
  "toolAliases": {},
  "allowedTools": ["read"],
  "toolsSettings": {},
  "resources": ["file://README.md"],
  "hooks": {},
  "includeMcpJson": true,
  "model": "claude-sonnet-4",
  "keyboardShortcut": "",
  "welcomeMessage": "<string>"
}
```

---

## Canonical Skill Folder Layout

Every skill in `.agents/skills/<skill-name>/` should contain:

```text
<skill-name>/
├── SKILL.md          # Frontmatter entry point + concise body
├── prompt.md         # Core tasking prompt (platform-neutral)
├── instructions.md   # Stable rules, standards, conventions
├── hooks.md          # Preflight / completion hook intent
└── examples/
    ├── sample-input.md
    ├── sample-output.md
    └── edge-cases.md
```

`SKILL.md` is **required**. `prompt.md`, `instructions.md`, and `hooks.md` are **strongly recommended** for any skill whose body exceeds 80 lines or that will be ported to multiple platforms.

---

## Canonical Agent Folder Layout

Platform-specific agent files in `.github/agents/`, `.claude/agents/`, `.kiro/agents/`:

```text
# GitHub Copilot
.github/agents/<name>.agent.md

# Claude Code
.claude/agents/<name>.md

# Kiro IDE
.kiro/agents/<name>.md
.kiro/agents/<name>.json   # CLI config — separate from IDE subagent

# Codex (no dedicated agent format; uses SKILL.md convention)
codex/skills/<name>/SKILL.md
```

---

## Upgrade Workflow

### Step 1 — Inventory existing files

```
For each target file or folder:
1. Identify platform (Copilot / Claude / Codex / Kiro IDE / Kiro CLI)
2. Read current frontmatter
3. Compare against schema above
4. List: missing fields, deprecated fields, wrong types
```

### Step 2 — Audit supporting modules

```
Check for presence of:
- prompt.md     → if absent, extract task mission from body and generate
- instructions.md → if absent, extract rules/constraints from body and generate
- hooks.md      → if absent, derive from any preflight/completion language in body
- examples/     → if absent, flag as recommended addition
```

### Step 3 — Apply frontmatter patches

Rules per platform:

| Action | Condition |
|--------|-----------|
| Add `name` | Always required; derive from filename if missing |
| Add `description` | Always required; must include trigger language |
| Add `argument-hint` | Copilot agents/skills if user-facing |
| Add `user-invocable: false` | Skills not meant for direct user invocation |
| Add `disable-model-invocation: false` | Copilot/skill default |
| Remove deprecated `infer` field | Copilot — field is deprecated |
| Strip extra fields from Codex `SKILL.md` | Keep only `name` + `description` |
| Add `model` | Claude agent if not set and non-default model needed |
| Add `maxTurns` | Claude agent if unbounded execution is a risk |
| Add `permissionMode: default` | Claude agent if missing |

### Step 4 — Generate missing modules

#### `prompt.md` generation rules

- Extract the core mission statement from the skill/agent body
- Rewrite in imperative, task-focused language
- Remove policy text (that belongs in `instructions.md`)
- Keep under 50 lines; link to `instructions.md` for constraints

#### `instructions.md` generation rules

- Extract: coding standards, testing rules, security checks, repo conventions
- Write as enumerated constraints: one rule per line
- Use present-tense imperatives: "Follow X", "Prefer Y", "Flag Z"
- Must be platform-neutral (no platform-specific syntax)

#### `hooks.md` generation rules

- Write two sections: `## Preflight` and `## Completion`
- Preflight: context loading, scope confirmation, prerequisite checks
- Completion: output format, summary structure, next-action recommendation
- Keep each section under 10 bullet points

### Step 5 — Validate and report

Produce a diff-style summary:

```
UPGRADED: .github/agents/reviewer.agent.md
  + added: argument-hint
  + added: user-invocable: true
  ~ fixed: model → array format ["Claude Opus 4.5"]
  - removed: deprecated field `infer`

CREATED: .github/skills/code-review/prompt.md
CREATED: .github/skills/code-review/instructions.md
CREATED: .github/skills/code-review/hooks.md

SKIPPED: codex/skills/code-review/SKILL.md — already minimal and valid
```

---

## Description Quality Rules

A `description` field must:

1. Open with a plain-English statement of what the skill/agent does
2. Include explicit trigger language: `"Use when: <condition1>, <condition2>, ..."`
3. Stay under 1024 characters
4. Be written in third person
5. Avoid vague words: `powerful`, `smart`, `advanced`, `various`, `multiple`

**Rewrite template:**

```
<Verb> <domain noun> using <method or tool>. Use when: <trigger-1>, <trigger-2>, <trigger-3>.
```

---

## Common Upgrade Patterns

### Pattern A — Copilot skill missing `user-invocable`

```yaml
# Before
---
name: code-review
description: Review code changes.
---

# After
---
name: code-review
description: Review code changes for correctness, security, and maintainability. Use when: reviewing PRs, patches, or risky refactors.
argument-hint: PR number, branch name, or diff summary
user-invocable: true
disable-model-invocation: false
context: workspace
---
```

### Pattern B — Claude agent missing `maxTurns` and `model`

```yaml
# Before
---
name: reviewer
description: Review code.
tools: [Read, Grep]
---

# After
---
name: reviewer
description: Review code changes for correctness, security, and test coverage. Use when: running a structured review on any diff or PR.
tools: [Read, Glob, Grep, Bash]
disallowedTools: [Write]
model: sonnet
permissionMode: default
maxTurns: 12
effort: medium
isolation: workspace
color: blue
---
```

### Pattern C — Kiro IDE agent missing `includeMcpJson`

```yaml
# Before
---
name: reviewer
description: Review changes.
tools: ["read"]
---

# After
---
name: reviewer
description: Review code and infrastructure changes for correctness, security, and blast radius. Use when: auditing PRs, configuration changes, or Terraform plans.
tools: ["read", "shell"]
model: claude-sonnet-4
includeMcpJson: true
includePowers: false
---
```

### Pattern D — Codex skill with extraneous frontmatter

```yaml
# Before
---
name: code-review
description: Review code.
user-invocable: true
context: fork
allowed-tools: shell
---

# After — strip to Codex minimum
---
name: code-review
description: Review code changes for correctness, security, and test coverage. Use when: reviewing PRs, patches, or architectural refactors.
---
```

---

## See Also

- [prompt.md](prompt.md) — core tasking prompt for this skill
- [instructions.md](instructions.md) — stable operating rules
- [hooks.md](hooks.md) — preflight and completion behavior
- [examples/sample-input.md](examples/sample-input.md) — sample before/after upgrade
- `Agent-Skill-Prompt-metadata.md` — authoritative cross-platform spec
