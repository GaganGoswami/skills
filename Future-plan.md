# How to Build Complex Skills for Coding Agents

A complex skill is not:

```text id="7y6fkg"
"one big prompt"
```

A real enterprise-grade skill is:

```text id="y3s7n0"
Goal
 + Context Intelligence
 + Memory
 + Tools
 + Policies
 + Workflows
 + Validation
 + Recovery
 + Observability
 + Runtime Adaptation
```

---

# 1. Universal Skill Architecture

Every advanced skill should follow this structure.

```yaml id="i7ehjt"
skill:
  metadata:
  objectives:
  triggers:
  inputs:
  outputs:

  context_layer:
  memory_layer:
  reasoning_layer:
  planning_layer:
  execution_layer:
  validation_layer:
  recovery_layer:
  observability_layer:
  governance_layer:
```

---

# 2. Core Concepts Before Building Skills

---

# A. Skills Are Runtime Systems

NOT:

```text id="0a7pjq"
static prompts
```

BUT:

```text id="shpsph"
adaptive execution systems
```

---

# B. Skills Need State

Need:

* working memory
* execution memory
* repo memory
* organizational memory

---

# C. Skills Need Tooling

Example tools:

* terminal
* docker
* kubectl
* git
* AST parser
* vector DB
* repo graph
* deployment APIs

---

# D. Skills Need Evaluation

Without evaluation:

```text id="ylpnw3"
agents hallucinate silently
```

---

# E. Skills Need Recovery

Without recovery:

```text id="ol4b4k"
complex workflows fail constantly
```

---



# 4. Deep Dive — AI Architecture Skill

This is MUCH more advanced.

---

# Goal

Design AI-native systems automatically.

---

# Responsibilities

Skill should:

* understand business problem
* determine AI patterns
* choose architecture
* select models
* define memory strategy
* define orchestration strategy
* define evaluation strategy

---

# STEP 1 — Business Understanding Layer

Input:

```text id="d0j4y4"
"Build KYC compliance co-pilot"
```

Skill extracts:

* domain
* workflows
* users
* regulations
* latency needs
* data sensitivity

---

# STEP 2 — AI Pattern Selection

Skill decides:

```text id="7nkmrl"
RAG?
Agents?
Workflow AI?
Multi-agent?
Realtime?
Fine-tuning?
Reasoning models?
Hybrid retrieval?
```

---

# STEP 3 — Architecture Planning

Generates:

```text id="bblc4n"
Frontend
Backend
LLM Layer
RAG Layer
Memory Layer
Orchestration Layer
Evaluation Layer
Observability Layer
Security Layer
```

---

# STEP 4 — Model Routing Decisions

Skill determines:

* GPT-5.5?
* local models?
* Claude?
* embedding models?
* reasoning models?

---

# STEP 5 — Memory Strategy

Chooses:

* vector memory
* episodic memory
* semantic memory
* organizational memory

---

# STEP 6 — Agent Architecture Planning

Determines:

* single agent?
* planner/executor?
* swarm?
* hierarchical orchestration?

---

# STEP 7 — Evaluation Architecture

Defines:

* hallucination checks
* benchmark datasets
* regression evaluation
* trace analysis

---

# FINAL AI Architecture Skill

```text id="f1jjlwm"
AI Architecture Skill
    ├── Business Understanding
    ├── AI Pattern Selector
    ├── Model Router
    ├── RAG Planner
    ├── Agent Planner
    ├── Memory Planner
    ├── Evaluation Planner
    ├── Security Planner
    └── Deployment Planner
```

---

# 5. Deep Dive — Multi-Agent Orchestration Skill

This is one of the hardest possible skills.

---

# Goal

Coordinate autonomous engineering swarms.

---

# Responsibilities

Skill must:

* spawn agents
* coordinate execution
* manage dependencies
* merge outputs
* resolve conflicts
* optimize token usage
* recover failures

---

# STEP 1 — Dynamic Agent Registry

Skill maintains registry:

```yaml id="c4z8i7"
agents:
  backend_agent:
  frontend_agent:
  db_agent:
  test_agent:
  security_agent:
```

---

# STEP 2 — Task Decomposition Engine

Input:

```text id="8fjlwm"
Implement customer onboarding feature
```

Planner decomposes:

```text id="qdxlgq"
- schema work
- API work
- frontend work
- tests
- deployment
```

---

# STEP 3 — Dependency Graph Generation

```text id="zdjlwm"
DB schema
   ->
Backend API
   ->
Frontend UI
```

---

# STEP 4 — Parallel Execution Planning

Detects independent tasks.

Example:

```text id="aex0tm"
Frontend
and
Test setup
can run simultaneously
```

---

# STEP 5 — Shared Memory Bus

All agents write to:

* task memory
* repo memory
* architecture memory
* execution memory

---

# STEP 6 — Conflict Resolution Engine

Critical problem.

Example:

```text id="jlwm4u"
2 agents edit same file
```

Need:

* merge strategy
* locking
* ownership
* semantic merge

---

# STEP 7 — Runtime Coordination

Orchestrator monitors:

* failures
* token consumption
* deadlocks
* retries
* agent health

---

# STEP 8 — Recovery Mechanisms

Example:

```text id="q8l3t6"
Frontend agent fails
    ->
spawn recovery agent
    ->
retry with smaller scope
```

---

# STEP 9 — Evaluation Layer

Evaluate:

* correctness
* consistency
* architecture alignment
* test coverage
* policy compliance

---

# STEP 10 — PR Generation

Final orchestration:

* consolidate changes
* generate changelog
* summarize reasoning
* create PR

---

# FINAL Multi-Agent Skill Architecture

```text id="7fjlwm"
Multi-Agent Skill
   ├── Agent Registry
   ├── Planner
   ├── DAG Generator
   ├── Scheduler
   ├── Memory Bus
   ├── Coordination Engine
   ├── Merge Engine
   ├── Recovery Engine
   ├── Evaluation Engine
   └── PR Engine
```

---

# 6. Critical Engineering Patterns

---

# A. DAG-Based Execution

Avoid:

```text id="prmjlwm"
linear workflows
```

Use:

```text id="8wz2ps"
dependency graphs
```

---

# B. Runtime Adaptation

Skill changes behavior based on:

* repo size
* complexity
* failures
* token budget
* latency

---

# C. Hierarchical Orchestration

```text id="mjlwm7"
Orchestrator
   ->
specialized orchestrators
   ->
worker agents
```

---

# D. Human Approval Gates

Required for:

* deployments
* destructive actions
* schema changes
* production updates

---

# 7. Suggested Tech Stack

---

Complex skills are the foundational building blocks of:

* autonomous SDLC
* enterprise AI engineering
* self-healing software systems
* AI-native engineering organizations
* next-generation coding agents beyond Copilot/Codex/Claude Code.
