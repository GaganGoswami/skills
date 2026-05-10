# Phase 3: Variant Analysis

## The Core Principle

After finding one vulnerability, search for all structural siblings in the codebase.
One confirmed bug is a pattern. This is the core of Anthropic's Mythos methodology —
one XSS often means twenty more written by the same developer using the same pattern.

## Process

1. **Extract the vulnerable pattern** — identify the structural fingerprint:
   - What function / method is called?
   - Is user input passed directly without sanitization?
   - What is the dangerous sink?

2. **Write a custom Semgrep rule** matching the structural pattern:

```yaml
rules:
  - id: variant-of-found-vuln
    patterns:
      - pattern: $FUNC($USER_INPUT, ...)
      - pattern-not: $FUNC(sanitize($USER_INPUT), ...)
    message: "Potential variant of confirmed $VULN_TYPE at $ORIGINAL_FILE:$LINE"
    languages: [javascript, python, java]
    severity: WARNING
    metadata:
      cwe: CWE-XXX
      original-finding: "$ORIGINAL_FILE:$LINE"
```

3. **Run the custom rule across the full codebase**:

```bash
semgrep scan --config=variant-rule.yaml --sarif --output=variants.sarif .
```

4. **Group variants by**:
   - Same CWE category
   - Same author (`git blame` the lines)
   - Same module or service boundary

5. **Bulk-report as a vulnerability family** — not individual tickets. One finding
   entry with a list of all affected locations.

## Variant Categories — Always Check These

| Original finding | Where to look for variants |
|---|---|
| Auth bypass in one route | All auth middleware chains; every route that skips middleware |
| SQLi in one query | All ORM `raw()`, `execute()`, `query()` calls with string concat |
| SSRF in one `fetch` | All outbound HTTP calls — `axios`, `got`, `requests`, `http.get` |
| Hardcoded secret in one file | All config, env, and `*.json` / `*.yaml` / `*.toml` files |
| XSS in one render | All `innerHTML`, `dangerouslySetInnerHTML`, `document.write` usages |
| Path traversal in one handler | All `path.join`, `fs.readFile`, `open()` with user input |
| Insecure deserialization | All `pickle.loads`, `JSON.parse` on untrusted input, `ObjectInputStream` |
| Prototype pollution | All `Object.assign`, lodash `merge`, `_.extend` with user objects |

## Semantic Variant Search (When Semgrep Misses Patterns)

For patterns that require understanding semantics (not just syntax), use the agent's
code reasoning to:

1. Search for all call sites of the same API (`grep_search` / `semantic_search`)
2. Read each call site and determine if input sanitization is present
3. Flag any site where the same class of input flows to the same class of sink

## Output Format

```
## Vulnerability Family: [CWE-XXX] [Name]

**Original finding**: `file:line` — [brief description]
**Variant count**: N additional locations

### Affected locations
- `file2:line` — [why this is a variant]
- `file3:line` — [why this is a variant]
- `file4:line` — [why this is a variant]

**Common root cause**: [shared developer pattern or missing abstraction]
**Recommended fix**: [single systemic fix — e.g., add sanitization to shared utility]
```
