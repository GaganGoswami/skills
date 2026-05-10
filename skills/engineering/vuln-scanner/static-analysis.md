# Phase 2: Static Analysis

## Tool Selection

Run both tools when possible. Semgrep requires no build; CodeQL provides deeper
semantic analysis but needs a compilable project.

### Semgrep (preferred — no build required)

```bash
# Install if not present
pip install semgrep

# Run OWASP Top 10 + secrets detection
semgrep scan \
  --config=p/owasp-top-ten \
  --config=p/secrets \
  --config=p/javascript \
  --config=p/python \
  --sarif --output=findings.sarif .

# Parse and triage results
cat findings.sarif | jq '
  .runs[].results[] |
  {
    rule: .ruleId,
    file: .locations[0].physicalLocation.artifactLocation.uri,
    line: .locations[0].physicalLocation.region.startLine,
    severity: .properties.severity,
    message: .message.text
  }
'
```

**Language-specific packs** (add as needed based on Phase 1 detection):

| Language / Framework | Config flag |
|---|---|
| JavaScript / TypeScript | `--config=p/javascript` |
| Python | `--config=p/python` |
| Java | `--config=p/java` |
| Go | `--config=p/golang` |
| Ruby | `--config=p/ruby` |
| React | `--config=p/react` |
| Django | `--config=p/django` |
| Express | `--config=p/express` |

### CodeQL (deep semantic — requires build)

```bash
# Create database
codeql database create codeql-db --language=javascript
# or: --language=python | java | cpp | csharp | go | ruby

# Run security queries
codeql analyze codeql-db \
  javascript-security-extended.qls \
  --format=sarif-latest \
  --output=codeql-findings.sarif

# Merge with Semgrep results
cat findings.sarif codeql-findings.sarif | \
  jq -s 'reduce .[] as $r ({"runs":[]}; .runs += $r.runs)'
```

## Severity Triage

| Level | Criteria |
|---|---|
| **CRITICAL** | RCE, auth bypass, SQLi with confirmed data sink |
| **HIGH** | XSS, SSRF, path traversal with user-controlled input |
| **MEDIUM** | Insecure crypto, hardcoded secrets, missing auth checks |
| **LOW** | Information disclosure, verbose error messages |

## False Positive Filter

Before reporting any finding, verify:

1. **Trace the input source** — is it actually user-controlled, or a developer-defined constant?
2. **Check for sanitization** — does any sanitizer/validator exist between the source and sink?
3. **Confirm reachability** — is the code path reachable from a real entry point (not dead code)?

Discard findings that fail any of the three checks. Mark uncertain ones as `NEEDS-MANUAL-REVIEW`.

## Checklist

- [ ] Semgrep run with OWASP + secrets + language packs
- [ ] CodeQL run (if buildable)
- [ ] Results merged and deduplicated
- [ ] False positive filter applied
- [ ] Findings triaged by severity
- [ ] CRITICAL / HIGH findings ready for Phase 3 (variant analysis) and Phase 4 (PoC)
