# Phase 1: Threat Modeling

## Workflow

1. **Map the repo structure** — identify entry points:
   - HTTP handlers, REST/GraphQL endpoints
   - CLI arguments and flags
   - File parsers (JSON, XML, YAML, CSV, binary formats)
   - IPC channels, message queues, event streams
   - Environment variables and config files
   - Third-party webhooks and callbacks

2. **Classify trust zones**:
   - External (untrusted) — internet-facing inputs, user-supplied data
   - Internal (semi-trusted) — service-to-service, authenticated clients
   - Privileged — admin interfaces, internal tools, CI/CD pipelines

3. **Trace data flows** from each entry point to sinks:
   - Database queries (raw SQL, ORM calls)
   - Shell execution (`exec`, `spawn`, `subprocess`, `os.system`)
   - File writes and path construction
   - Serialization / deserialization
   - Authentication and authorization checks
   - Outbound HTTP calls (SSRF risk)
   - HTML rendering (XSS risk)

4. **Build a STRIDE threat matrix**:

   | Category | Question to answer |
   |---|---|
   | **S**poofing | Can an attacker impersonate a user or service? |
   | **T**ampering | Can data be modified in transit or at rest? |
   | **R**epudiation | Can actions be denied? Are audit logs tamper-proof? |
   | **I**nfo Disclosure | Are secrets, PII, or internal paths exposed? |
   | **D**enial of Service | Can input cause resource exhaustion or crashes? |
   | **E**levation of Privilege | Can a low-trust caller gain higher permissions? |

5. **Output**: a repo-specific threat matrix that drives Phase 2 scanner config

## Framework Detection

Auto-detect the framework and load the relevant rule packs for Phase 2.

| Framework | Key rule packs to activate |
|---|---|
| Express / Node.js | SSRF, prototype pollution, ReDoS, path traversal |
| Spring Boot / Java | Deserialization, OGNL injection, SSRF, XXE |
| Django / Flask | SSTI, SQLi, CSRF bypass, insecure deserialization |
| React / Next.js | XSS, client-side path traversal, CSP bypass |
| Ruby on Rails | Mass assignment, SQLi, CSRF, insecure redirects |
| Go (net/http) | SSRF, path traversal, integer overflow |

## Attack Surface Checklist

- [ ] All HTTP routes enumerated
- [ ] Auth middleware verified on every route
- [ ] Third-party dependencies inventoried (`npm ls`, `pip list`, `mvn dependency:tree`)
- [ ] Secrets scanning baseline run (no keys committed)
- [ ] All data flows traced to sinks
- [ ] STRIDE matrix populated
- [ ] Framework-specific rules selected for Phase 2
