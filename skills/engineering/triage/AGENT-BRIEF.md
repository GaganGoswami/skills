# Agent Brief

An agent brief is a comment posted to a `ready-for-agent` issue. It gives an AFK agent everything it needs to implement correctly — without becoming outdated the moment the code changes.

## Principles

**Durability over precision.** Describe interfaces, types, behavioral contracts, and module responsibilities. Avoid file paths, line numbers, and internal function names — these change. An agent can find a file; it cannot infer a contract that was never written down.

**Behavioral, not procedural.** Describe WHAT the implementation should do, not HOW to do it. An agent picking up this issue should make its own implementation decisions.

**Complete acceptance criteria.** Each criterion should be concrete, independently testable, and verifiable without ambiguity. "Works correctly" is not a criterion. "Returns 422 when the email field is missing" is.

**Explicit scope boundaries.** State what is out of scope. Prevents agents from doing more (or less) than intended.

## Template

```markdown
## Agent Brief

**Category:** bug | enhancement

**Summary:** One sentence describing what this issue asks for.

**Current behavior:** What happens now (bugs only).

**Desired behavior:** What should happen after this issue is resolved.

**Key interfaces:**
- `TypeName` — description of role
- `functionName(param: Type): ReturnType` — description
- Config shape: `{ field: Type }` — description

**Acceptance criteria:**
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

**Out of scope:**
- Thing A is not required
- Thing B will be handled in a separate issue
```

## Example

**Bad brief** (file path + procedural instruction):
> Update line 247 of `src/skills/registry.ts` to truncate descriptions longer than 1024 characters before calling `buildSystemPrompt`.

**Good brief** (behavioral + durable):

```markdown
## Agent Brief

**Category:** bug

**Summary:** Skill descriptions longer than 1024 characters cause silent truncation in the system prompt, making skill selection unreliable.

**Current behavior:** The registry accepts descriptions of any length. Descriptions exceeding 1024 characters are silently truncated during system prompt assembly, cutting off the "Use when" trigger clause.

**Desired behavior:** The registry rejects descriptions longer than 1024 characters at registration time with a clear error. Existing skills with over-length descriptions should be flagged during the next load.

**Key interfaces:**
- `SkillRegistry.register(skill: Skill): void` — should throw `SkillValidationError` when `skill.description.length > 1024`
- `SkillValidationError` — new error type, message should include the skill name and actual length

**Acceptance criteria:**
- [ ] Registering a skill with a description > 1024 chars throws `SkillValidationError`
- [ ] Error message includes the skill name and character count
- [ ] Skills with descriptions ≤ 1024 chars register without error
- [ ] Existing tests still pass

**Out of scope:**
- Auto-truncation is not acceptable — the description must be fixed at the source
- Updating existing over-length skill descriptions is a separate issue
```
