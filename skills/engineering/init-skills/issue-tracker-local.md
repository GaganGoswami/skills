# Issue Tracker: Local

Issues live as markdown files in `.scratch/`. No CLI tool required — the agent reads and writes files directly.

## File layout

```
.scratch/
  <feature-slug>/
    PRD.md
    issues/
      01-short-slug.md
      02-another-slug.md
```

- One directory per feature, kebab-case slug
- PRD (if any) at `.scratch/<feature-slug>/PRD.md`
- Issues numbered from `01`, kebab-case slug: `01-short-slug.md`

## Issue file format

```markdown
# Title

Status: needs-triage

Body text here.

## Acceptance criteria

- [ ] Criterion 1

## Comments

---
**Agent** — YYYY-MM-DD

Comment text.
```

- `Status:` line near the top — update it in place when the state changes
- Comments append under `## Comments`, separated by `---`

## Conventions

- "Publish to tracker" = create the markdown file
- "Fetch relevant ticket" = read the file (and any linked files)
- "Add a comment" = append under `## Comments`
- "Change label/state" = update the `Status:` line
