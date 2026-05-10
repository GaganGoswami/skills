---
name: skill-factory
description: Analyze a session for repeated patterns, frequent corrections, and re-explained context. Synthesize reusable SKILL.md files that permanently encode the pattern. Use when the user says "save this pattern", "we keep doing this", "turn this into a skill", or at the end of a session with notable repeated workflows or corrections.
---

# Skill Factory

Turn tribal knowledge and session patterns into version-controlled agent skills that prevent the same friction from recurring.

## Pattern detection

Review the current session for:

1. **Rephrasings** — prompts the user had to restate because the agent misunderstood
2. **Injected context** — background the user provided that isn't in any existing skill or AGENTS.md
3. **Corrections** — agent outputs the user had to override or fix
4. **Orchestrated workflows** — multi-step sequences the user assembled manually that could run automatically

## Skill synthesis

For each detected pattern:

1. **Name it** — short verb-noun (`lint-staged-check`, `migration-rollback`)
2. **Write the description** — what it does + "Use when [specific trigger]"
3. **Encode the corrective behavior** — not the happy path, the thing that kept going wrong
4. **Add a Gotchas section** — failure modes to avoid (highest signal content)
5. Keep SKILL.md under 100 lines; split to REFERENCE.md if needed

## Output protocol

1. Present proposed skills to the user for review
2. Do NOT write files until the user approves
3. After approval, write to `skills/engineering/<skill-name>/SKILL.md`
4. Update AGENTS.md skill table with the new entry

## Qualification threshold

A pattern qualifies as a skill if:
- It occurred ≥ 2 times in the session, OR
- It caused a correction that took > 3 turns to resolve, OR
- The user explicitly flagged it as recurring

A single one-off command does not qualify — it belongs in a script or alias.

## Gotchas

- The `description` field is what the agent reads to decide whether to load the skill — make it specific, not generic
- Corrections are higher signal than rephrasings — they reveal actual agent failure modes
- Don't encode workarounds for bugs that should be fixed upstream
- If the pattern is a single shell command, it's a script — not a skill
