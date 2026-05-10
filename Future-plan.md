This is a rich design challenge. Here's a comprehensive, deeply thought-out skill architecture for a **Mythos-style vulnerability scanner** that works across Claude Code, GitHub Copilot (GHCP), and OpenAI Codex.

***

# Vulnerability Scanner Skill: Design Blueprint

The **Agent Skills open standard** is now adopted by Claude Code, GitHub Copilot, Codex CLI, Cursor, and Gemini CLI — meaning a single `SKILL.md` file you author works across all of them without modification. This is your primary deployment vehicle. [dev](https://dev.to/maximsaplin/ai-agents-vs-code-vulnerabilities-was-anthropic-mythos-a-big-deal-or-fear-mongering-8ci)

***

## Skill Architecture Overview

The skill should be a **Capability Uplift** skill — it gives agents abilities they don't have out of the box (running real static analysis, exploit modeling, threat classification) rather than just describing vulnerabilities. The structure is: [firecrawl](https://www.firecrawl.dev/blog/best-claude-code-skills)

```
.claude/skills/
└── vuln-scanner/
    ├── SKILL.md              ← Frontmatter + routing logic
    ├── threat-model.md       ← Repo-specific threat modeling
    ├── static-analysis.md    ← CodeQL / Semgrep execution
    ├── variant-analysis.md   ← Cross-codebase pattern matching
    ├── exploit-poc.md        ← PoC generation workflow
    └── report-template.md    ← Structured findings output
```

Claude loads only the `SKILL.md` name/description (~100 tokens) at startup, then pulls in sub-files on demand — keeping context efficient. [claude](https://claude.com/blog/how-to-create-skills-key-steps-limitations-and-examples)

***

## The SKILL.md File

This is the complete, production-ready skill definition:

```markdown
---
name: vuln-scanner
description: >
  Autonomous vulnerability scanning skill inspired by Anthropic Mythos methodology.
  Activates when the user asks to: scan for security vulnerabilities, audit the repo
  for CVEs, find exploitable code paths, perform threat modeling, run static analysis,
  detect OWASP Top 10 issues, check for injection/auth/crypto flaws, or generate
  proof-of-concept exploits for found vulnerabilities. NOT for general code review
  or linting. Use for security-specific analysis workflows on any language or framework.
license: MIT
---

# Vulnerability Scanner — Mythos-Inspired Security Skill

## Overview
This skill runs a structured, multi-phase vulnerability audit against the current
repository, using a methodology modeled after Anthropic's Mythos security research.
It combines static analysis tooling, semantic code reasoning, and variant analysis
to find real, exploitable vulnerabilities — not just theoretical checklist items.

## Phase 1: Repo Threat Modeling
Read [threat-model.md](threat-model.md) first. Build a project-specific attack surface
map before scanning. Identify: trust boundaries, external inputs, authentication paths,
crypto usage, and data sinks. This prevents generic false positives.

## Phase 2: Static Analysis
Read [static-analysis.md](static-analysis.md). Execute CodeQL and/or Semgrep
against the repository. Map results to CWE categories. Prioritize by exploitability.

## Phase 3: Variant Analysis
Read [variant-analysis.md](variant-analysis.md). After finding one vulnerability,
search for structural variants across the entire codebase. One XSS often means
twenty more in the same pattern.

## Phase 4: Exploit PoC Generation
Read [exploit-poc.md](exploit-poc.md). For high-confidence findings, generate a
minimal proof-of-concept. A working PoC transforms a low-priority ticket into
an immediate action item.

## Phase 5: Report
Read [report-template.md](report-template.md). Output a structured findings report
in SARIF-compatible format with file:line citations, CVSS scores, and remediation
guidance.

## Routing Decision Tree
- User says "scan" or "audit" → Run all 5 phases
- User says "find variants of [vuln]" → Phase 3 only
- User says "threat model" → Phase 1 only
- User says "generate PoC" → Phase 4 only
- User says "fix vuln at [file:line]" → Phase 5 remediation path
```

***

## Phase Sub-Files (Key Design Details)

### `threat-model.md` — Phase 1
```markdown
## Threat Modeling Workflow

1. Map the repo structure: identify entry points (HTTP handlers, CLI args, file parsers,
   IPC channels, env vars)
2. Classify trust zones: external (untrusted), internal (semi-trusted), privileged
3. Trace data flows from each entry point to sinks (DB queries, shell exec, file writes,
   serialization, auth checks)
4. Build a STRIDE threat model: Spoofing, Tampering, Repudiation, Info Disclosure,
   DoS, Elevation of Privilege
5. Output: a repo-specific threat matrix that drives Phase 2 scanner config

## Framework Detection
Auto-detect framework and load relevant rule packs:
- Express/Node → inject SSRF, prototype pollution, ReDoS rules
- Spring Boot/Java → inject deserialization, OGNL injection, SSRF rules
- Django/Flask → inject SSTI, SQLi, CSRF bypass rules
- React/Next.js → inject XSS, client-side path traversal, CSP bypass rules
```

***

### `static-analysis.md` — Phase 2

```markdown
## Static Analysis Execution

### Semgrep (preferred — no build required)
```bash
# Install if not present
pip install semgrep

# Run OWASP Top 10 + secrets detection
semgrep scan --config=p/owasp-top-ten \
             --config=p/secrets \
             --config=p/javascript \
             --config=p/python \
             --sarif --output=findings.sarif .

# Parse and triage
cat findings.sarif | jq '.runs[].results[] | {rule: .ruleId, file: .locations.physicalLocation.artifactLocation.uri, line: .locations.physicalLocation.region.startLine, severity: .properties.severity}'
```

### CodeQL (deep semantic — requires build)
```bash
codeql database create codeql-db --language=javascript
codeql analyze codeql-db javascript-security-extended.qls \
  --format=sarif-latest --output=codeql-findings.sarif
```

## Triage Rules
- CRITICAL: RCE, auth bypass, SQLi with confirmed data sink
- HIGH: XSS, SSRF, path traversal with user-controlled input
- MEDIUM: Insecure crypto, hardcoded secrets, missing auth checks
- LOW: Information disclosure, verbose error messages

## False Positive Filter
Before reporting, verify each finding by:
1. Tracing the input source — is it actually user-controlled?
2. Checking if sanitization exists between source and sink
3. Confirming the code path is reachable from a real entry point
```

***

### `variant-analysis.md` — Phase 3 (The Mythos Method)

This is the most powerful phase — it's what separates Mythos-class scanning from ordinary checkers: [dev](https://dev.to/maximsaplin/ai-agents-vs-code-vulnerabilities-was-anthropic-mythos-a-big-deal-or-fear-mongering-8ci)

```markdown
## Variant Analysis: Find the Vulnerability Family

After finding one vulnerability, search for all structural siblings in the codebase.
This is the core of Anthropic's Mythos methodology — one confirmed bug is a pattern.

### Process
1. Extract the vulnerable code pattern (AST fingerprint or grep pattern)
2. Use Semgrep to write a custom rule matching the same structural pattern:

```yaml
rules:
  - id: variant-of-found-vuln
    patterns:
      - pattern: $FUNC($USER_INPUT, ...)  # generalize the finding
      - pattern-not: $FUNC(sanitize($USER_INPUT), ...)
    message: Potential variant of confirmed $VULN_TYPE
    languages: [javascript, python, java]
    severity: WARNING
```

3. Run cross-repo scan with the custom rule
4. Group variants by: same CWE, same developer (git blame), same module
5. Bulk-report as a vulnerability family — not individual tickets

### Variant Categories to Always Check
- Auth bypass → check all auth middleware chains
- SQLi in one query → check all ORM raw() or execute() calls
- SSRF in one fetch → check all outbound HTTP calls
- Hardcoded secret in one file → scan all config/env files
- XSS in one render → check all innerHTML / dangerouslySetInnerHTML usages
```

***

### `exploit-poc.md` — Phase 4

```markdown
## Proof-of-Concept Generation

For CRITICAL and HIGH findings with confirmed reachable paths, generate a minimal PoC.

### PoC Template Structure
```
## Vulnerability: [CWE-XXX] [Name] at [file:line]

**Attack Vector**: [describe the exact input path]
**Preconditions**: [what attacker needs — unauthenticated? specific role?]

**PoC Payload**:
[minimal payload — curl command, HTTP request, code snippet]

**Expected Result**: [what happens when exploit succeeds]
**Impact**: CVSS [score] — [brief impact statement]

**Recommended Fix**: [concrete code change with before/after]
```

### Safety Guardrails
- Generate PoCs only for code in the current repo
- Do NOT generate PoCs for third-party infrastructure beyond the repo's scope
- Omit weaponized payloads for vulnerabilities in production systems
  unless explicitly requested by repo owner
- Flag any finding that could be a supply-chain attack vector for immediate escalation
```

***

## Cross-Agent Compatibility

Since the Agent Skills spec is an open standard, this skill installs identically on all three platforms: [firecrawl](https://www.firecrawl.dev/blog/best-claude-code-skills)

| Platform | Install Location | Activation |
|---|---|---|
| **Claude Code** | `.claude/skills/vuln-scanner/` | Automatic on security keywords |
| **GitHub Copilot** | `.github/agents/vuln-scanner.md` (flatten to single file)  [techcommunity.microsoft](https://techcommunity.microsoft.com/blog/azureinfrastructureblog/vs-code-custom-agents-ai-powered-terraform-security-scanning-in-the-ide/4507903) | `@vuln-scanner` in chat |
| **OpenAI Codex CLI** | `.codex/skills/vuln-scanner/` | Automatic + `/vuln-scan` command |

For GHCP specifically, you may need to flatten the multi-file structure into a single `.github/agents/vuln-scanner.md` with a security gate: a grep check for `CRITICAL VULNERABILITY FOUND` that fails the PR check if triggered. [eliostruyf](https://www.eliostruyf.com/custom-security-agent-github-copilot-actions/)

***

## CI/CD Security Gate Integration

Pair the skill with a GitHub Actions pipeline for continuous enforcement:

```yaml
# .github/workflows/vuln-scan.yml
name: AI Vulnerability Scan
on: [pull_request]
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run vuln-scanner skill via Claude Code
        run: claude -p "Run vuln-scanner on this PR diff" --output report.md
      - name: Security Gate
        run: |
          if grep -q "CRITICAL" report.md; then
            echo "Critical vulnerability found — blocking merge"
            exit 1
          fi
```

***

## What Makes This "Mythos-Class"

Anthropic's Mythos model demonstrated that AI can autonomously find and exploit real vulnerabilities in production codebases like the Linux kernel. The three design choices that replicate this are: [dev](https://dev.to/maximsaplin/ai-agents-vs-code-vulnerabilities-was-anthropic-mythos-a-big-deal-or-fear-mongering-8ci)

1. **Repo-specific threat modeling first** — not a generic OWASP checklist, but a structural map of *your* code's attack surface [shawnkanungo](https://shawnkanungo.com/blog/openai-codex-security-ai-agent-finds-code-vulnerabilities)
2. **Variant analysis as a first-class phase** — finding one bug means finding the whole family, which is how Mythos achieved scale [dev](https://dev.to/maximsaplin/ai-agents-vs-code-vulnerabilities-was-anthropic-mythos-a-big-deal-or-fear-mongering-8ci)
3. **Sandboxed PoC validation** — confirming exploitability before reporting, which is how Codex Security eliminates false positives [shawnkanungo](https://shawnkanungo.com/blog/openai-codex-security-ai-agent-finds-code-vulnerabilities)

The Trail of Bits security skills (CodeQL + Semgrep execution) are the best existing reference implementation and a strong complement to this custom skill. [firecrawl](https://www.firecrawl.dev/blog/best-claude-code-skills)

Would you like me to generate the complete file set ready to drop into your repo, or would you prefer to customize the language/framework targets first (TypeScript/Node, Java Spring, Python Django, etc.)?