# Issue Tracker: GitLab

Issues live in GitLab Issues. Use the `glab` CLI for all operations. Infer the project from the git remote.

## Commands

**Create an issue:**
```bash
glab issue create --title "Title" --description "Body"
```

**Read an issue (with comments):**
```bash
glab issue view <number> --comments
```

Machine-readable:
```bash
glab issue view <number> -F json
```

**List issues:**
```bash
glab issue list --state opened
```

Note: GitLab uses `opened`, not `open`.

**Add a comment (note):**
```bash
glab issue note <number> --message "Comment text"
```

**Add a label:**
```bash
glab issue update <number> --label "label-name"
```

**Remove a label:**
```bash
glab issue update <number> --unlabel "label-name"
```

**Close an issue** — add a note first, then close:
```bash
glab issue note <number> --message "Closing because..."
glab issue close <number>
```

## Merge requests

GitLab calls pull requests "merge requests". Use `glab mr` for all MR operations.

## Conventions

- "Publish to tracker" = create a GitLab issue
- "Fetch relevant ticket" = `glab issue view <number> --comments`
- Labels are strings; match what the project actually uses
