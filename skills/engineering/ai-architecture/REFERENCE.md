# AI Architecture — Reference

## Memory strategy

| Type | Storage | When to use |
|---|---|---|
| Working memory | In-context (messages array) | Current task state, tool call history |
| Episodic memory | Vector DB (session-scoped) | Recall what happened in prior sessions |
| Semantic memory | Vector DB (persistent) | Domain facts, summarised repo knowledge |
| Organisational memory | Knowledge graph or vector DB | Cross-user shared institutional knowledge |

Rule of thumb: start with in-context → add episodic → add semantic → add organisational only when multi-user knowledge sharing is required.

## Evaluation architecture

### Metrics by pattern

| Pattern | Key metrics |
|---|---|
| RAG | Faithfulness, answer relevancy, context precision/recall |
| Agent | Task completion rate, tool call accuracy, retry rate |
| Multi-agent | Coordination overhead, conflict rate, end-to-end latency |
| Fine-tuned | BLEU/ROUGE, domain benchmark, regression vs base model |

### Evaluation pipeline

1. **Unit eval** — run each LLM call against a labelled dataset (≥ 50 examples)
2. **Integration eval** — run full agent flow end-to-end against golden traces
3. **Regression eval** — run on every PR that touches prompts or model config
4. **Shadow eval** — run new model/prompt in parallel with production; diff outputs

## Security layer

- **Prompt injection defence**: classify every user input before routing to tools; block `ignore previous instructions` patterns
- **PII masking**: detect and redact PII before it enters the LLM context; restore in the final response if needed
- **RBAC**: scope tool permissions to the authenticated user's role; never pass admin credentials to an agent
- **Audit trail**: log every LLM call with: timestamp, model, token count, user ID, tool calls made
- **Human approval gates**: required before any action that is destructive, touches production data, or involves regulated data

## Agent orchestration patterns

### Single agent
```
User → Agent → Tools → Response
```
Best for: tasks that fit in one context window with < 5 tool calls.

### Planner + executor
```
User → Planner → Task list → Executor(s) → Merge → Response
```
Best for: complex tasks that need decomposition before execution.

### Hierarchical swarm
```
Orchestrator → Specialised Orchestrators → Worker Agents
```
Best for: enterprise-scale workflows with domain-specialised subagents (backend, frontend, security, test agents).

## Model routing rules

```
if task == "classification" or "routing":   use small/cheap model
if task == "generation" or "summarisation": use mid-tier model
if task == "reasoning" or "planning":       use reasoning model
if task == "embedding":                     use embedding model
if cost_budget == "critical":               use local model
```

Always define a fallback model for each tier in case of rate-limiting or outage.
