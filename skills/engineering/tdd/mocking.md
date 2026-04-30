# Mocking

Mock at system boundaries only. Don't mock things you control.

## Mock these

- **External APIs** — Stripe, Twilio, third-party services you don't own
- **Databases** — when a real test DB isn't available or practical
- **Time and randomness** — `Date.now()`, `Math.random()`, UUID generators
- **Filesystem** — when a real temp directory isn't practical

## Don't mock these

- Your own classes and modules
- Internal collaborators
- Anything you control and could use directly

Mocking your own code tests that you wired things up, not that the wiring does anything useful. When a test passes because `myService.process` was called — not because the output is correct — it's a false positive waiting to happen.

## Designing for mockability

### Dependency injection

Pass dependencies in rather than creating them inside.

```typescript
// Hard to mock — creates its own dependency
class NotificationService {
  async notify(userId: string) {
    const client = new TwilioClient(process.env.TWILIO_KEY)
    await client.messages.create(...)
  }
}

// Easy to mock — accepts dependency
class NotificationService {
  constructor(private sms: SmsClient) {}

  async notify(userId: string) {
    await this.sms.send(...)
  }
}
```

### Prefer SDK-style interfaces over generic fetchers

Design mock boundaries around specific operations, not generic request/response wrappers.

**Avoid** (generic fetcher — conditional mock logic required):
```typescript
interface HttpClient {
  get(url: string): Promise<unknown>
  post(url: string, body: unknown): Promise<unknown>
}
```

**Prefer** (operation-specific — each independently mockable):
```typescript
interface PaymentClient {
  createCharge(amount: number, currency: string): Promise<Charge>
  refund(chargeId: string): Promise<Refund>
  getCharge(chargeId: string): Promise<Charge>
}
```

Each operation is independently mockable. No conditional logic in mock setup. Type safety per operation. Tests read as specifications.
