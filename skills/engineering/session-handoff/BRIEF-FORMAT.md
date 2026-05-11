# Handoff Brief Format

Standard template for a session handoff. Fill every section — blank = explicit signal.

---

```
HANDOFF BRIEF
Session: <YYYY-MM-DD> — <3-word slug>
Agent: <model that ran the session, if known>
Status: In Progress / Blocked / Ready to Continue / Complete
```

---

## Goal

_The original intent. One sentence. What were we trying to accomplish?_

## What happened

_Chronological summary of work done. Bullets. Be specific about what succeeded and what failed._

- Did: <action>
- Tried: <action> → <outcome>
- Found: <discovery>

## Files changed

| File | Change |
|---|---|
| `<path>` | <what changed — created / modified / deleted + one-line description> |

## Decisions made

_Every significant choice. Must include reasoning._

| Decision | Chosen | Alternatives considered | Reasoning |
|---|---|---|---|
| <topic> | <choice> | <other options> | <why this one> |

## Discoveries

_Surprises, gotchas, constraints found, things that didn't work as expected._

1. <discovery>
2. <discovery>

## Open questions

_Specific, unanswered questions that block or inform next steps._

1. **<Question>** — Context: <why this matters, what we know so far>
2. **<Question>** — Context: <why this matters, what we know so far>

## Blocker (if any)

_If the session ended blocked, describe exactly:_

- **What we were trying to do**: <action>
- **What went wrong**: <error / obstacle>
- **What we tried**: <attempts made>
- **What is needed to unblock**: <specific requirement or decision>

## Next actions

_Ordered list. Each action must be executable by a cold-start agent with no additional context._

1. [ ] <verb + specific action + file or resource> — e.g., "Add rate limiting to `src/api/auth.ts` using the `express-rate-limit` library. See the open question about threshold values above."
2. [ ] <next action>
3. [ ] <next action>

---

**To resume**: "Continue the session from `.agents/handoffs/<filename>.md`. Start from the NEXT ACTIONS section."
