---
name: semantic-memory
description: Generate and retrieve compressed, layered semantic summaries of a codebase so agents get task-relevant context without loading the full repo. Use when compressing a large codebase for agent consumption, retrieving relevant service context for a task, or building persistent memory across sessions.
---

# Semantic Memory

Compress repository knowledge into layered summaries so agents receive precise, task-relevant context — not a raw firehose of files.

## Compression pipeline

```
Raw Files → AST Summary → Service Summary → Domain Summary → Architecture Summary → Task Context
```

Each layer is ~10× smaller than the one above. Agents receive only the layer appropriate to their task.

## Quick start

```bash
# Largest modules (highest compression value)
find . -name "*.ts" -o -name "*.py" -o -name "*.java" | xargs wc -l 2>/dev/null | sort -rn | head -20

# Public interface surface
rg "^export (default |const |function |class )" . --type ts -l
```

## Workflow

1. **Chunk semantically** — by module/service, not by file size
2. **Summarize each chunk** — purpose, public interface, key dependencies
3. **Build service digests** — one structured block per service
4. **Build domain summary** — cross-service view in domain language
5. **Cache summaries** — store in `.agents/memory/` tracked by git
6. **Retrieve on demand** — pull only digests for services the task touches

## Service digest format

```
Service: <name>
Purpose: <one sentence>
Exposes: <APIs / events / CLI commands>
Depends on: <other services>
DB: <schemas / tables owned>
Key files: <3–5 most important paths>
```

## Retrieval strategy

- Start with the domain summary (always)
- Pull service digests for services the task directly touches
- Pull file-level detail only for files being modified
- Never load the full codebase into context

## Gotchas

- Stale summaries are worse than no summaries — regenerate after significant merges
- Don't summarize generated files (migrations, protos, lock files)
- Keep domain summary under 500 tokens; expand per-service digest as needed
- Index services by their public interface, not their internal class names
