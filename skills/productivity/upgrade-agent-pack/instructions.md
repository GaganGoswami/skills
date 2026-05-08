# Upgrade Agent Pack — Operating Instructions

## General Rules

- Treat `Agent-Skill-Prompt-metadata.md` as the single source of truth for all frontmatter schemas.
- Apply the minimum diff that fixes a compliance issue; do not rewrite content that is not broken.
- Never add fields that are not in the canonical schema for the detected platform.
- Preserve all existing body content; reorganize into modules only if the body exceeds 80 lines.
- Use only fields officially documented for the target platform — do not add Copilot fields to a Codex `SKILL.md`.
- When generating a missing module, extract and rewrite existing content; do not invent new guidance.

## Frontmatter Patch Rules

### All platforms
- `name` must exactly match the filename stem (e.g., `reviewer.agent.md` → `name: reviewer`).
- `description` must be ≤ 1024 characters, third-person, and include `"Use when: ..."` trigger language.
- Do not use vague words in `description`: `powerful`, `smart`, `advanced`, `various`, `multiple`.

### GitHub Copilot agents (`.agent.md`)
- Always include `user-invocable` and `disable-model-invocation`.
- `model` must be an array if specifying multiple models.
- `handoffs` items require `label`; `agent`, `prompt`, `send`, `model` are optional.
- Remove deprecated `infer` field without replacement.
- `target` is optional; omit unless targeting a specific runtime (`vscode` or `cloud`).
- `hooks` defaults to `{}`; do not add hook bodies unless the platform runtime supports them.

### GitHub Copilot skills (`SKILL.md`)
- Always include `user-invocable` and `disable-model-invocation`.
- `context` is experimental; set only if the skill requires fork-level access.
- `allowed-tools` must be a platform-recognized value; `shell` is the only currently documented value.
- Do not add `relatedSkills` for rendered Copilot output (only used in `.agents/` canonical sources).

### Claude Code agents
- `tools` and `disallowedTools` are mutually exclusive sets; do not list a tool in both.
- `model` must be one of `sonnet`, `opus`, `haiku`, or a versioned variant.
- `permissionMode` defaults to `default`; only set `full` if explicitly authorized.
- `maxTurns` should be ≤ 20 for skills; ≤ 50 for full-lifecycle orchestrators.
- `isolation` defaults to `workspace`; use `repo` only for read-only analysis agents.
- `background: true` should only be set for agents that run asynchronously as monitors.

### Codex skills (`SKILL.md`)
- Strip all frontmatter fields except `name` and `description`.
- Move any extra guidance from frontmatter into the Markdown body.
- Keep the body structured with clear `# When to use` and `# Instructions` sections.

### Kiro IDE agents
- `tools` must be an array of string tool names; quote each element.
- `includeMcpJson: true` should be added when the agent needs access to workspace MCP tools.
- `includePowers: false` is the safe default unless the agent needs elevated access.
- Do not add Copilot-specific fields (`user-invocable`, `allowed-tools`, etc.).

### Kiro CLI agents (`.json`)
- `prompt` must be a `file://` URI pointing to an adjacent `prompt.md`.
- `allowedTools` is a subset of `tools`; do not list tools in `allowedTools` that are not in `tools`.
- `toolAliases` and `toolsSettings` may be empty objects.
- `resources` should list only files that must be in context at startup.

## Module Generation Rules

### `prompt.md`
- First heading: `# <Skill Name> — Core Tasking Prompt`
- One paragraph mission statement.
- Numbered workflow steps.
- Output format specification.
- Do NOT include policy rules or constraints — those go in `instructions.md`.

### `instructions.md`
- First heading: `# <Skill Name> — Operating Instructions`
- Group rules into named sections (General, Frontmatter Patch Rules, Module Generation, etc.).
- Each rule is one line, starting with an imperative verb.
- Include anti-patterns as a named section at the end.
- Keep platform-neutral; no platform-specific syntax.

### `hooks.md`
- Two sections only: `## Preflight` and `## Completion`.
- Preflight: context loading, scope validation, prerequisite checks.
- Completion: output formatting, summary structure, next-action options.
- Keep each section to ≤ 10 bullet points.
- Do NOT include implementation code — this is a human-readable intent document.

### `examples/`
- `sample-input.md` — a realistic before-state showing a stale/incomplete file.
- `sample-output.md` — the upgraded after-state with all changes applied.
- `edge-cases.md` — at least three edge cases: empty body, multi-platform, conflicting fields.

## Anti-Patterns

- Do not copy a Copilot frontmatter schema into a Codex `SKILL.md`.
- Do not add `disallowedTools: [Write]` to a Claude agent that needs to create files.
- Do not set `background: true` for interactive agents.
- Do not truncate body content to fit it into frontmatter fields.
- Do not generate module files that are already present and valid.
- Do not rename files as part of an upgrade — only patch content.
- Do not add `relatedSkills` to platform-specific renders (only canonical `.agents/` sources use this field).
