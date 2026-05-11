---
name: session-handoff
description: Package the current session state as a structured handoff brief — decisions made with reasoning, files touched, open questions, blockers, and concrete next steps. Use at the end of a work session, before switching context, when handing off to another agent or teammate, or when the user says "wrap up", "summarize what we did", "create a handoff", "I need to stop here", or "pick this up later".
---

# Session Handoff

Package everything the next person (or agent) needs to pick this up cold. Zero warm-up required.

## The problem this solves

Context loss between sessions is the #1 compounding cost in AI-assisted development. Re-establishing "where were we?" takes 10–20 minutes per session and forces the same reasoning to be redone. This skill captures the reasoning once, so it's never lost.

## Workflow

### Step 1 — Reconstruct the session

Review the conversation history. Extract:

1. **What was the goal?** — The original intent the user arrived with
2. **What did we actually do?** — The work that happened, in order
3. **What changed?** — Files created, modified, or deleted
4. **What decisions were made?** — Every significant choice and the reasoning behind it
5. **What was discovered?** — Surprises, constraints found, gotchas hit
6. **What is unfinished?** — Work started but not completed
7. **What is open?** — Questions not yet answered, decisions not yet made
8. **What is next?** — The next concrete action, ready to execute

### Step 2 — Write the brief

Use the format from [BRIEF-FORMAT.md](BRIEF-FORMAT.md) exactly. Fill all sections — a blank section is a signal, not an omission.

### Step 3 — Save the brief

Save to `.agents/handoffs/<YYYY-MM-DD>-<slug>.md` where slug is a 3-word description of the session (e.g., `2026-05-10-auth-refactor-spike`).

If `.agents/handoffs/` does not exist, create it.

### Step 4 — State the precise resume command

Close the brief with a single line the next agent can paste verbatim to resume:

> **To resume**: "Continue the session from `.agents/handoffs/<filename>.md`. Start from the NEXT ACTIONS section."

## What makes a good handoff brief

- **Decisions include reasoning** — "We chose X" is useless. "We chose X because Y, and considered Z but ruled it out because W" is a handoff.
- **Open questions are specific** — "Figure out auth" is useless. "Decide: do we use refresh tokens or session cookies? The constraint is: must work for both web and mobile clients."
- **Next actions are executable** — Each action starts with a verb and contains enough context for a cold-start agent to execute it without asking questions.
- **Files are linked** — Every changed file is listed with a one-line description of what changed.

## Gotchas

- Don't summarize what you *planned* to do — capture what you *actually* did
- Discoveries are often the highest-value part of the handoff — don't skip them
- If the session ended in a blocker, the handoff should state exactly what the blocker is and what was tried
- A handoff brief should be readable in under 3 minutes — if it's longer, compress decisions into one line each and move detail to sub-sections
- Version the handoff: if you're updating an existing one, append `v2`, don't overwrite (history matters)
