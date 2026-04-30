# Interface Design for Testability

Three principles that make interfaces easy to test.

## 1. Accept dependencies, don't create them

Inject dependencies rather than instantiating them inside the module. Callers control what gets wired up; tests inject test doubles.

**Hard to test** (creates its own dependency):
```typescript
class OrderService {
  private mailer = new EmailService() // can't substitute in tests

  async confirmOrder(orderId: string) {
    await this.mailer.send(...)
  }
}
```

**Easy to test** (accepts dependency):
```typescript
class OrderService {
  constructor(private mailer: Mailer) {} // inject in tests

  async confirmOrder(orderId: string) {
    await this.mailer.send(...)
  }
}
```

## 2. Return results, don't only produce side effects

Pure functions are trivially testable. Side-effect-only methods require you to verify via observation (querying a DB, checking a flag), which couples tests to implementation.

**Hard to test** (void, side-effect only):
```typescript
function processCart(cart: Cart): void {
  cart.items.forEach(item => {
    inventory.decrement(item.id, item.quantity) // have to check inventory state
  })
}
```

**Easy to test** (returns result):
```typescript
function processCart(cart: Cart): InventoryUpdate[] {
  return cart.items.map(item => ({
    id: item.id,
    delta: -item.quantity,
  }))
  // test asserts on the returned value — no side-effect observation needed
}
```

## 3. Small surface area

Fewer methods and parameters means simpler test setup. Every parameter you add to a function signature is another thing tests must provide.

If your test setup is more complex than the assertion, the interface is probably too large. That's a signal to push complexity inside the module.
