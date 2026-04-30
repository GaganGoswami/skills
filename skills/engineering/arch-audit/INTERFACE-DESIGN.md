# Interface Design

This document describes how to design interfaces deliberately. It is based on the "Design It Twice" principle from John Ousterhout's _A Philosophy of Software Design_. Vocabulary is from [LANGUAGE.md](LANGUAGE.md).

## The process

### Step 1: Frame the problem space

Before proposing any interface, establish:

- **Constraints**: What must this module accept, produce, or guarantee?
- **Dependency category**: From [DEEPENING.md](DEEPENING.md) — what kind of dependency is involved?
- **Illustrative sketch**: A rough usage example showing how a caller might use this module

Show this to the user and immediately proceed to Step 2. Don't wait.

### Step 2: Spawn multiple interface candidates in parallel

Generate at least three radically different interface designs. Assign each to a sub-agent with a different brief. Each brief should include both the [LANGUAGE.md](../arch-audit/LANGUAGE.md) vocabulary and the project's CONTEXT.md vocabulary so the output uses the right terms.

Suggested briefs:

- **Agent A — Minimize interface**: 1–3 entry points. Callers provide as little as possible. What can the module infer, default, or decide internally?
- **Agent B — Maximize flexibility**: Every possible variation is exposable. Caller has full control. What would a power user want?
- **Agent C — Optimize for the most common caller**: Design around the 90% case. Make that case trivially easy; accept that edge cases are harder.
- **Agent D — Ports and adapters first**: Design around the seam. Lead with the port; derive the interface from what adapters need to satisfy.

Each agent outputs:

1. **Interface** — the public surface (type signatures, function names, parameters)
2. **Usage example** — a realistic caller snippet
3. **What the implementation hides** — the complexity invisible to callers
4. **Dependency strategy** — which adapters are needed and why
5. **Trade-offs** — what this design makes easy vs. what it makes hard

### Step 3: Present, compare, and recommend

Contrast the candidates by:

- **Depth**: Which interface hides the most implementation complexity?
- **Locality**: Which concentrates change, bugs, and knowledge in one place?
- **Seam placement**: Where does each design locate the substitution point?

Then give a concrete recommendation. Be opinionated — don't just present options, say which one you'd use and why.
