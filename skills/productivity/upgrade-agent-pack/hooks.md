# Upgrade Agent Pack — Hook Intent

## Preflight

- Read `Agent-Skill-Prompt-metadata.md` to load the current canonical schemas for all four platforms before touching any file.
- Confirm the target scope: single file, single skill folder, or full recursive scan.
- Detect the platform for each target by inspecting its folder path and file extension.
- Check whether `prompt.md`, `instructions.md`, and `hooks.md` already exist in each skill folder before planning generation.
- Validate that the working directory is a recognized agent-pack repository (look for `.agents/`, `.github/agents/`, or `.claude/agents/`).
- Abort with a clear error if `Agent-Skill-Prompt-metadata.md` is missing or unreadable.

## Completion

- Emit a per-file diff summary listing every added, changed, and removed frontmatter field plus every new file created.
- Emit a final summary line: `Upgrade complete: <N> files upgraded, <M> files created, <K> files skipped, <E> errors.`
- Flag any file that could not be auto-upgraded (e.g., ambiguous platform, conflicting fields, unreadable content) as a manual review item.
- Recommend running `node scripts/pipeline/lint-prompts.mjs` after upgrades to catch stale counts, broken links, and shallow prompts.
- Recommend running `node scripts/pipeline/render-platform-assets.mjs` after upgrading canonical `.agents/` sources to sync platform mirrors.
- Do NOT push, commit, or deploy — leave all file changes as local edits for human review.
