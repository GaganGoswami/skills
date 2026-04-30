# Deep Modules

From _A Philosophy of Software Design_ by John Ousterhout.

A **deep module** provides a large behavior behind a small interface. The implementation does a lot; the interface exposes little.

```
┌─────────────────────────────────┐
│  Interface (small)              │  ← what callers see
│  • 2–3 methods                  │
│  • minimal parameters           │
├─────────────────────────────────┤
│                                 │
│  Implementation (large)         │  ← what callers don't see
│                                 │
│  • handles edge cases           │
│  • owns the complexity          │
│  • encapsulates state changes   │
│                                 │
└─────────────────────────────────┘
```

A **shallow module** has an interface nearly as complex as its implementation. Adding it to the codebase adds cognitive load without adding leverage.

```
┌─────────────────────────────────┐
│  Interface (large)              │  ← callers must know everything
│  • many methods                 │
│  • many parameters              │
├─────────────────────────────────┤
│  Implementation (small)         │  ← barely hiding anything
└─────────────────────────────────┘
```

## Interface design questions

When reviewing or designing a module's interface, ask:

- Can I reduce the number of methods?
- Can I simplify the parameters (fewer, or smarter defaults)?
- Can I hide more complexity inside the implementation?
- If a caller has to call 3 methods in a specific order — can the module handle that sequence internally?

## Why it matters for TDD

Deep modules are easier to test:

- Fewer entry points = fewer test cases to write for the interface
- Complex behavior is concentrated = complex behavior is testable in one place
- Callers don't care about internals = tests don't break on refactor

Shallow modules spread complexity to their callers. When you test a shallow module, you end up testing the caller logic too — which means you're not testing in the right place.
