# Issue Tracker: GitHub

Issues live in GitHub Issues. Use the `gh` CLI for all operations. Infer the repo from the git remote.

## Commands

**Create an issue:**
```bash
gh issue create --title "Title" --body "Body"
```

**Read an issue (with comments):**
```bash
gh issue view <number> --comments
```

**List issues (machine-readable):**
```bash
gh issue list --state open --json number,title,labels,state | jq '.[]'
```

Filter by label:
```bash
gh issue list --label needs-triage --json number,title,state | jq '.[]'
```

**Add a comment:**
```bash
gh issue comment <number> --body "Comment text"
```

**Add a label:**
```bash
gh issue edit <number> --add-label "label-name"
```

**Remove a label:**
```bash
gh issue edit <number> --remove-label "label-name"
```

**Close an issue:**
```bash
gh issue close <number>
```

## Conventions

- "Publish to tracker" = create a GitHub issue
- "Fetch relevant ticket" = `gh issue view <number> --comments`
- Labels are strings; match what the repo actually uses
- If the repo has no labels yet, create them with `gh label create`
