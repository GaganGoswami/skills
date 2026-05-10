---
name: ai-architecture
description: Design AI-native system architectures end-to-end: select AI patterns (RAG, agents, multi-agent, fine-tuning), choose models, plan memory strategy, design evaluation pipelines, and produce a complete architecture blueprint. Use when asked to architect an AI system, AI co-pilot, LLM-powered workflow, agent platform, or when choosing between AI patterns for a business problem.
---

# AI Architecture

Translate a business problem into a complete AI system blueprint — patterns, models, memory, orchestration, evaluation, and deployment strategy.

## Quick start

Answer these before generating the architecture:

1. **Domain** — what business process does this automate or augment?
2. **Users** — humans in the loop, autonomous, or both?
3. **Latency** — interactive (<2s), near-real-time (<30s), or batch?
4. **Data sensitivity** — PII, regulated (HIPAA/GDPR), or public?
5. **Scale** — requests/day order of magnitude?

## Workflow

### Step 1 — AI pattern selection

Choose the primary pattern(s):

| Pattern | When to use |
|---|---|
| RAG | Ground responses in private/fresh data |
| Single agent | Autonomous multi-step task with tool use |
| Multi-agent swarm | Parallel specialised tasks |
| Workflow AI | Deterministic graph with AI decision nodes |
| Fine-tuning | Consistent style/format at high volume |
| Reasoning model | Complex planning, math, code generation |
| Hybrid retrieval | Keyword + vector for high-recall domains |

### Step 2 — Architecture layers

Generate a blueprint covering:

- **Frontend** — chat UI, API, or embedded widget
- **LLM layer** — primary model + fallback; routing rules
- **RAG layer** — chunking strategy, vector store, re-ranking
- **Memory layer** — working / episodic / semantic / organisational
- **Orchestration layer** — single agent vs planner+executor vs swarm
- **Evaluation layer** — hallucination checks, benchmarks, regression
- **Observability layer** — traces, latency, cost per query
- **Security layer** — prompt injection defence, PII masking, RBAC

### Step 3 — Model routing

Assign models per task class:

```
Fast/cheap   → small local model or GPT-4o-mini
Reasoning    → o3 or Claude Sonnet
Generation   → Claude Opus or GPT-4.1
Embeddings   → text-embedding-3-large or local
```

### Step 4 — Output

Produce:
- [ ] Architecture diagram (Mermaid)
- [ ] Layer-by-layer decision log
- [ ] Model routing table
- [ ] Memory strategy statement
- [ ] Evaluation plan (metrics + datasets)
- [ ] Human approval gate list (destructive or PII-touching actions)

## Gotchas

- RAG alone is not an agent — if the system needs to act, add tool-calling
- Fine-tuning requires labelled data at scale; default to prompt engineering first
- Multi-agent adds coordination overhead — don't use it for tasks a single agent handles in < 5 steps
- Always include a human approval gate before any action that is irreversible or touches regulated data

## Advanced

See [REFERENCE.md](REFERENCE.md) for memory strategy details, evaluation architecture, and security layer patterns.
