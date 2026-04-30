# Refactoring

Candidates to look for after all tests pass — never while RED.

## Common candidates

**Duplication** — extract a function or class when the same logic appears in two or more places. Name it after what it does, not where it came from.

**Long methods** — break into private helpers. Keep tests on the public interface; don't test the private helpers directly. If a private helper is worth testing, it may want to be a separate module.

**Shallow modules** — if two modules each hide very little complexity, consider whether they'd be better combined or whether one should absorb the other's logic. A module that just delegates to another is probably not earning its interface.

**Feature envy** — if a method spends most of its time operating on another module's data, the logic probably belongs on that other module.

**Primitive obsession** — if you're passing raw strings, numbers, or booleans that carry domain meaning (email address, currency amount, on/off flag), consider a value object or named type.

**Code the new code reveals** — sometimes writing one feature exposes that adjacent existing code is more tangled than it seemed. Note it; refactor it if it's within scope.

## Rules

- Run tests after every refactor step — one change at a time
- A refactor should leave behaviour identical; if tests change, it's not a refactor
- Don't refactor speculatively — only what the current code is asking for
- If a refactor would take longer than the feature itself, note it and move on
