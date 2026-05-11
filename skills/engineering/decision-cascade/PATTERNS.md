# Known Decision Cascade Patterns

Common high-stakes decisions and their documented downstream effects. Use as a starting template — adapt to your context.

---

## Monolith → Microservices

**Decision**: Split a monolith into independently deployable services.

```
Monolith → Microservices
├── Immediate
│   ├── [DECISION] Define service boundaries and ownership
│   ├── [DECISION] Choose inter-service communication (HTTP vs events)
│   └── [COST] Rewrite module interfaces as network contracts
├── 2nd order
│   ├── [DECISION] Choose service discovery mechanism (Consul, k8s DNS, etc.)
│   ├── [COST] Distributed tracing setup (Jaeger, OTEL)
│   ├── [RISK] Distributed transactions — no ACID across services
│   ├── [COST] Per-service CI/CD pipelines
│   └── [DECISION] API versioning strategy
└── 3rd order
    ├── [COST] Platform engineering team or equivalent ownership
    ├── [RISK] Cascading failures — service mesh or circuit breakers required
    ├── [LOCK-IN] Team topology now coupled to service topology
    └── [DECISION] Data consistency model (eventual vs strong consistency)
```

**Leverage point**: Define clear domain boundaries first. Wrong boundaries create worse coupling than the monolith.

---

## Synchronous → Asynchronous (event-driven)

**Decision**: Replace direct service calls with message queues / event streams.

```
Sync → Async
├── Immediate
│   ├── [DECISION] Choose message broker (Kafka, SQS, RabbitMQ)
│   ├── [COST] Rewrite call sites as producers; add consumers
│   └── [DECISION] Define event schema and versioning strategy
├── 2nd order
│   ├── [COST] Dead-letter queue and replay infrastructure
│   ├── [RISK] Eventual consistency — UI must handle "pending" states
│   ├── [DECISION] Idempotency strategy for consumers
│   └── [COST] Observability for async flows (correlation IDs, tracing)
└── 3rd order
    ├── [LOCK-IN] Event schema becomes a public contract — breaking changes are expensive
    ├── [COST] Schema registry and compatibility tooling
    └── [RISK] Consumer lag under load — requires monitoring and alerting
```

**Leverage point**: Define the event schema contract early and enforce compatibility from day one.

---

## SQL → NoSQL

**Decision**: Replace a relational database with a document or key-value store.

```
SQL → NoSQL
├── Immediate
│   ├── [DECISION] Choose NoSQL type (document, key-value, wide-column, graph)
│   ├── [COST] Denormalize schema — design for query patterns, not relations
│   └── [COST] Data migration plan
├── 2nd order
│   ├── [RISK] No joins — complex queries must be handled in application code
│   ├── [DECISION] Consistency model per operation (eventual vs strong)
│   ├── [COST] ORM / query layer replacement
│   └── [RISK] Schema validation moves to application layer — drift risk
└── 3rd order
    ├── [LOCK-IN] Query patterns baked into data layout — expensive to change
    ├── [COST] Analytics and reporting now require ETL or a separate OLAP store
    └── [DECISION] Multi-region strategy (replication topology)
```

**Leverage point**: Audit query patterns before choosing the NoSQL type — wrong type creates a harder migration than SQL.

---

## Self-hosted → Managed Cloud Service

**Decision**: Replace self-managed infrastructure with a vendor-managed PaaS/SaaS.

```
Self-hosted → Managed
├── Immediate
│   ├── [COST] Migration and data transfer
│   ├── [DECISION] Pricing model fit (per-request vs per-hour vs per-seat)
│   └── [COST] Auth/RBAC reconfiguration
├── 2nd order
│   ├── [LOCK-IN] Vendor API surface now a dependency
│   ├── [RISK] Feature availability tied to vendor roadmap
│   └── [COST] Egress costs for data-heavy workloads
└── 3rd order
    ├── [LOCK-IN] Proprietary features accelerate lock-in over time
    ├── [RISK] Price changes — vendor economics can shift dramatically
    └── [DECISION] Exit strategy: can you migrate away if needed?
```

**Leverage point**: Use vendor-agnostic abstractions (e.g., OTEL, S3-compatible APIs) from day one.

---

## Manual Process → Automated Pipeline

**Decision**: Automate a previously human-managed workflow.

```
Manual → Automated
├── Immediate
│   ├── [DECISION] Define the automation boundary — what stays human?
│   ├── [COST] Build the pipeline + test coverage for edge cases
│   └── [RISK] Hidden logic in human judgment not yet captured
├── 2nd order
│   ├── [COST] Monitoring and alerting for the automated path
│   ├── [DECISION] Failure handling — fallback to manual or fail loudly?
│   └── [RISK] Automation error propagates faster than human error
└── 3rd order
    ├── [LOCK-IN] Team loses institutional knowledge of the manual process
    ├── [COST] Ongoing maintenance as upstream inputs change
    └── [RISK] Edge cases that were handled gracefully by humans become incidents
```

**Leverage point**: Keep a manual override path — automate the 80% case, preserve human control for the long tail.
