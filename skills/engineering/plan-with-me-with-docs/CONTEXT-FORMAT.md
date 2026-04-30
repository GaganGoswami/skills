# Context Format

A `CONTEXT.md` file is the project's domain glossary — the shared vocabulary between engineers and domain experts. It keeps the codebase and the conversations around it speaking the same language.

## File structure

```markdown
# {Context Name}

{One sentence describing what this context covers.}

## Language

**{Term}**: {Definition in one sentence.}  
_Avoid_: {aliases to retire}

**{Term}**: {Definition in one sentence.}

## Relationships

**{Term A}** has many **{Term B}s** ...

## Example dialogue

{A short exchange between a developer and domain expert that demonstrates the vocabulary in natural use.}

## Flagged ambiguities

- {A term or concept that is still fuzzy or contested.}
```

## Rules

**Be opinionated.** Pick one term for each concept and retire the aliases. The point is to eliminate ambiguity, not document it.

**Flag conflicts explicitly.** If a term means different things in different contexts, say so under "Flagged ambiguities" — don't silently pick one.

**Tight definitions.** One sentence per term. If you need more, the definition is doing too much.

**Show relationships.** The "Relationships" section is where cardinality and ownership live — it's not optional.

**Project-specific only.** Don't document general programming terms. Only include concepts that are specific to this project's domain and would require explanation to a new team member.

**Group under subheadings** when the glossary grows large enough that terms naturally cluster.

## Single vs multi-context repos

**Single-context**: one `CONTEXT.md` at the repo root, `docs/adr/` alongside it. Most repos are this.

**Multi-context**: `CONTEXT-MAP.md` at the root describes the contexts and how they relate. Each context gets its own `CONTEXT.md` and `docs/adr/` (e.g. `src/ordering/CONTEXT.md`).

Create files lazily — only when you have something to write. If no `CONTEXT.md` exists, create one when the first term resolves. If no `docs/adr/` directory exists, create it when the first ADR is needed.
