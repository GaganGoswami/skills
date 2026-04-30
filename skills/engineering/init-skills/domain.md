# Domain Docs

Engineering skills consume two types of domain documentation: a domain glossary and architecture decision records.

## Where to look

**Single-context repo**: `CONTEXT.md` at the repo root. ADRs in `docs/adr/`.

**Multi-context repo**: `CONTEXT-MAP.md` at the root lists all contexts and how they relate. Each context has its own `CONTEXT.md` and `docs/adr/` directory (e.g. `src/ordering/CONTEXT.md`, `src/ordering/docs/adr/`).

If neither file exists, proceed silently. Don't block on missing docs.

## How to use the glossary

Before exploring unfamiliar code, read the glossary. Then:

- Use glossary vocabulary in all output: issue titles, ADR text, code comments, test names, inline responses
- If you encounter a concept that has no glossary entry, that's a signal: either it's invented language (worth questioning) or a real gap (note it for `/plan-with-me-with-docs`)
- Flag conflicts between what the code does and what the glossary says — code may have drifted

## How to use ADRs

Read `docs/adr/` before making architectural recommendations in an unfamiliar area. Then:

- Respect decisions that are still active
- Flag conflicts explicitly: "This approach contradicts ADR-0007 — but worth reopening because…"
- Don't silently work around an ADR without surfacing it

## File structure reference

Single-context:
```
CONTEXT.md
docs/
  adr/
    0001-initial-shape.md
    0002-auth-strategy.md
```

Multi-context:
```
CONTEXT-MAP.md
src/
  ordering/
    CONTEXT.md
    docs/adr/
  billing/
    CONTEXT.md
    docs/adr/
```
