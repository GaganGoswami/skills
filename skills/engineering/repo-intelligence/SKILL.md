---
name: repo-intelligence
description: Build executable repository cognition: service graphs, API detection, event flow analysis, dependency mapping, and architecture summaries. Use when analyzing architecture, planning cross-service changes, tracing dependencies, generating PR context, or debugging incidents across services.
---

# Repo Intelligence

Build a living map of how the repository works — services, APIs, events, dependencies, and ownership — so agents can reason about cross-cutting changes without human scaffolding.

## Quick start

```bash
# Detect service entry points
rg "@RestController|router\.|FastAPI|@app\.route|@Controller" . -l

# Detect event flows
rg "Kafka|@KafkaListener|EventEmitter|\.emit\(|\.subscribe\(" . -l

# Detect DB usage
rg "JpaRepository|MongoRepository|prisma\.|SELECT |createTable" . -l
```

## Workflow

1. **Map services** — find entry points (HTTP, gRPC, CLI, workers)
2. **Detect APIs** — REST routes, GraphQL schemas, gRPC protos
3. **Detect event flows** — message queues, pub/sub, webhooks
4. **Detect DB usage** — repos, queries, schema migrations
5. **Build dependency graph** — what calls what, what owns what
6. **Identify ownership** — CODEOWNERS, team tags, module boundaries
7. **Generate summary** — architecture map in plain English

## Output checklist

- [ ] Service list with entry point types
- [ ] API inventory (method + path or equivalent)
- [ ] Event flow diagram (producer → topic → consumer)
- [ ] DB ownership map (service → schemas/tables)
- [ ] Dependency adjacency list
- [ ] Orphan services flagged
- [ ] Circular dependencies flagged

## Validation

- **Orphan** = service with no inbound edges and no outbound API
- **Circular** = A → B → C → A in the call graph
- **Missing owner** = module with no CODEOWNERS or team tag

## Search patterns by stack

| Stack | API pattern | Event pattern |
|---|---|---|
| Spring | `@RestController`, `@RequestMapping` | `@KafkaListener`, `ApplicationEvent` |
| Express | `router.get\|post\|put` | `EventEmitter`, `amqplib` |
| FastAPI | `@app.get\|post\|put` | `aiokafka`, `celery` |
| NestJS | `@Controller`, `@Get\|Post` | `@EventPattern`, `ClientKafka` |

## Gotchas

- Don't confuse test doubles and mocks as real service dependencies
- Generated files (protos, OpenAPI specs) reveal contracts — don't skip them
- CODEOWNERS absence doesn't mean no owner — check git blame on module roots
