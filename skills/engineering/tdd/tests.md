# Tests

What good tests look like — and what bad tests look like.

## Good tests: behavior through public interfaces

A good test describes a behavior a caller cares about, using the module's public API. It survives internal refactors because it doesn't know or care how the implementation works.

```typescript
test("user can checkout with a valid cart", async () => {
  const cart = Cart.create()
  cart.add(product("shirt", 29_00))
  cart.add(product("jeans", 59_00))

  const order = await checkout(cart, paymentMethod("visa-ending-4242"))

  expect(order.status).toBe("confirmed")
  expect(order.total).toBe(88_00)
})
```

Characteristics:
- Tests behavior callers care about
- Uses the public API only — no internals touched
- Survives any internal refactor that preserves the behavior
- Describes WHAT, not HOW
- One logical assertion (the order was confirmed at the right total)

## Bad tests: implementation details

A bad test couples to internals. It breaks when you refactor even though behavior hasn't changed.

```typescript
test("checkout calls paymentService.process", async () => {
  const paymentService = { process: jest.fn() }
  const cart = new Cart(paymentService)

  await cart.checkout()

  expect(paymentService.process).toHaveBeenCalledWith({ amount: 88_00 })
})
```

Red flags:
- Mocks an internal collaborator
- Asserts that a method was called (not what the outcome was)
- Breaks if you rename `paymentService.process` to `paymentService.charge`
- Name describes HOW, not WHAT

## Good vs bad: createUser

**Bad** — asserts on a mocked internal:
```typescript
test("createUser hashes password", async () => {
  const hasher = { hash: jest.fn().mockResolvedValue("hashed") }
  await createUser("alice", "secret", hasher)
  expect(hasher.hash).toHaveBeenCalledWith("secret")
})
```

**Good** — asserts on observable behavior:
```typescript
test("created user can authenticate with their password", async () => {
  await createUser("alice", "secret")
  const result = await authenticate("alice", "secret")
  expect(result.success).toBe(true)
})
```

The good test doesn't care whether you use bcrypt, argon2, or something else. It cares that authentication works.
