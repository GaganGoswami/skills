# Language

Precise vocabulary for talking about module design. Use these terms exactly — they carry specific meaning that generic alternatives blur.

## Terms

**Module** — any unit with an interface and an implementation: a function, class, package, or slice. The size doesn't matter; the boundary does.  
_Avoid_: unit, component, service (these carry other connotations)

**Interface** — the full contract at a module's boundary: type signatures, invariants, ordering constraints, error modes, configuration surface, performance expectations.  
_Avoid_: API, signature (these are subsets, not the whole contract)

**Implementation** — the code inside the module, invisible to callers. Callers must not depend on it.

**Depth** — the ratio of leverage to interface complexity. A deep module provides a lot of behavior behind a small interface. A shallow module's interface is nearly as complex as its implementation.  
Depth is a property of the interface, not the implementation. You can have a large implementation that is still shallow if the interface is equally large.

**Seam** — the location where an interface lives and where one adapter could be replaced by another.  
_Avoid_: boundary (too vague)

**Adapter** — a concrete thing that satisfies an interface at a seam. The word describes the _role_ (satisfying the interface), not the substance.

**Leverage** — what callers gain from depth: they invoke a small interface and get a large behavior.

**Locality** — what maintainers gain from depth: changes, bugs, and knowledge are concentrated in one place instead of spread across callers.

## Principles

- **Depth is a property of the interface, not the implementation.** A 10,000-line module with a 10-function public API may be deep. A 50-line wrapper with a 50-function pass-through API is shallow.
- **The deletion test**: if you deleted this module, how much caller code would break? High breakage = high leverage = deep. Low breakage = shallow.
- **The interface is the test surface.** Tests should couple to the interface, not the implementation.
- **One adapter = hypothetical seam.** Two adapters = real seam. Don't claim you have a real seam until you've had to satisfy the interface twice.

## Relationships

```
Module
├── Interface  →  produces Leverage (for callers)
│                 produces Locality (for maintainers)
└── Implementation (hidden)

Seam hosts Adapter(s)
```

## Rejected framings

These terms are imprecise in this context — don't use them when the terms above apply:

| Avoid | Use instead |
|---|---|
| "Service" | Module (unless it's genuinely a separate service) |
| "API" | Interface (when referring to the full contract) |
| "Boundary" | Seam (when referring to a substitution point) |
| "Unit" | Module |
| "Component" | Module |
