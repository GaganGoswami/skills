# Deepening Opportunities

This document defines how to identify and execute module-deepening opportunities. Vocabulary is from [LANGUAGE.md](LANGUAGE.md).

## Dependency categories

Before deciding how to deepen a module, classify its dependencies. The classification determines the deepening strategy.

### 1. In-process (pure computation, no I/O)

Algorithms, transformations, validation logic, formatting. No external calls.

**Strategy**: Always deepenable. Extract into a module with a clean interface, test it directly. No adapters needed.

### 2. Local-substitutable (a real alternative exists)

PGLite instead of Postgres. In-memory filesystem instead of the real one.

**Strategy**: Deepenable if a stand-in exists. Prefer the stand-in in your test suite over mocking. This keeps tests honest — you're running real logic, not a mock.

### 3. Remote but owned (ports & adapters)

Your own database, your own internal service, a queue you control.

**Strategy**:

1. Define a **port** at the seam (an interface in your language's type system)
2. The deep module owns the logic; transport is injected as an **adapter**
3. Tests use an in-memory adapter — no network, no teardown, fast

The port describes _what_ is needed. The adapter describes _how_ it's satisfied.

### 4. True external / mock

Stripe, Twilio, third-party APIs you don't control.

**Strategy**: The deepened module takes the dependency as an injected port. Tests provide a mock adapter. The mock adapter should be typed against the port — if the port changes, the mock breaks before production does.

## Seam discipline

- **One adapter** = hypothetical seam. You _could_ substitute, but you haven't had to yet. Worth tracking.
- **Two adapters** = real seam. You've proven the port is useful and stable. This is a genuine interface.

Don't elevate a hypothetical seam to a "real" design decision until you have the second adapter.

## Testing strategy: replace, don't layer

When you deepen a module, the old tests often become redundant. Don't keep the old unit tests on the shallow module AND add new tests on the deep module — that's layering. Instead:

1. Write new tests at the deepened module's interface
2. Delete tests that were testing implementation details of the old shallow module
3. Tests describe behaviour, not implementation

The question to ask: _"Does this test care how the module works, or just what it does?"_ If the former, delete it.
