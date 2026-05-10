# Phase 5: Findings Report

## Output Format

Produce a structured markdown report. For tooling integration, also emit SARIF.

---

## Security Audit Report

**Repository**: `[repo-name]`  
**Scan date**: `[YYYY-MM-DD]`  
**Scanner**: vuln-scanner (Mythos-inspired)  
**Tools run**: Semgrep `[version]` · CodeQL `[version]` · Manual reasoning  

---

### Executive Summary

| Severity | Count |
|---|---|
| 🔴 CRITICAL | N |
| 🟠 HIGH | N |
| 🟡 MEDIUM | N |
| 🔵 LOW | N |
| **Total** | **N** |

**Key findings**: [1-3 sentence summary of the most important risks]

---

### Findings

#### [FINDING-001] [Vulnerability Name]

| Field | Value |
|---|---|
| **Severity** | CRITICAL / HIGH / MEDIUM / LOW |
| **CWE** | CWE-XXX — [CWE Name] |
| **CVSS Score** | X.X (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H) |
| **File** | `path/to/file.ext:line` |
| **Status** | Open / Confirmed / Needs Review |

**Description**:  
[2-3 sentences explaining what the vulnerability is and why it matters]

**Evidence**:
```language
// vulnerable code snippet with line numbers
```

**Exploit path**:  
[Step-by-step how an attacker reaches this code]

**Remediation**:
```language
// fixed code
```

**References**: [CWE link] · [OWASP link] · [CVE if applicable]

---

*(repeat FINDING-NNN block for each finding)*

---

### Variant Families

List vulnerability families discovered in Phase 3.

| Family | Original | Variants | Locations |
|---|---|---|---|
| [CWE-XXX] [Name] | `file:line` | N | [file list] |

---

### Attack Surface Map

*(From Phase 1 — paste the threat matrix here)*

---

### Remediation Roadmap

Prioritized fix list, ordered by severity then effort:

| Priority | Finding | Fix effort | Owner (git blame) |
|---|---|---|---|
| 1 | [FINDING-001] | Small / Medium / Large | `@username` |
| 2 | [FINDING-002] | Small / Medium / Large | `@username` |

---

### SARIF Export

For IDE / PR integration, emit findings as SARIF:

```bash
# Merge all SARIF files from Phases 2 and 3
jq -s '{
  "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Documents/CommitteeSpecifications/2.1.0/sarif-schema-2.1.0.json",
  "version": "2.1.0",
  "runs": map(.runs[]) | [{
    "tool": {"driver": {"name": "vuln-scanner", "rules": []}},
    "results": .
  }]
}' findings.sarif variants.sarif > final-report.sarif
```

Upload to GitHub code scanning:

```bash
gh api \
  --method POST \
  -H "Accept: application/vnd.github+json" \
  /repos/{owner}/{repo}/code-scanning/sarifs \
  -f commit_sha="$(git rev-parse HEAD)" \
  -f ref="refs/heads/main" \
  -f sarif="$(gzip -c final-report.sarif | base64)"
```

---

### Report Checklist

- [ ] All CRITICAL and HIGH findings have confirmed exploit paths (Phase 4 PoC)
- [ ] All findings have file:line citations
- [ ] All findings have concrete remediation guidance
- [ ] Variant families documented
- [ ] SARIF exported for CI/CD integration
- [ ] Remediation roadmap prioritized
