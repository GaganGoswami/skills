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

## Routing Decision Tree

| User intent | Phases to run |
|---|---|
| "scan" or "audit" | All 5 phases |
| "find variants of [vuln]" | Phase 3 only |
| "threat model" | Phase 1 only |
| "generate PoC" | Phase 4 only |
| "fix vuln at [file:line]" | Phase 5 remediation path |

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

## What Makes This "Mythos-Class"

Anthropic's Mythos model demonstrated that AI can autonomously find and exploit real
vulnerabilities in production codebases. Three design choices that replicate this:

1. **Repo-specific threat modeling first** — not a generic OWASP checklist, but a
   structural map of *your* code's attack surface
2. **Variant analysis as a first-class phase** — finding one bug means finding the
   whole family, which is how Mythos achieved scale
3. **Sandboxed PoC validation** — confirming exploitability before reporting, which
   eliminates false positives

## CI/CD Security Gate Integration

```yaml
# .github/workflows/vuln-scan.yml
name: AI Vulnerability Scan
on: [pull_request]
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run vuln-scanner skill
        run: claude -p "Run vuln-scanner on this PR diff" --output report.md
      - name: Security Gate
        run: |
          if grep -q "CRITICAL" report.md; then
            echo "Critical vulnerability found — blocking merge"
            exit 1
          fi
```

## Cross-Agent Compatibility

| Platform | Install Location | Activation |
|---|---|---|
| **Claude Code** | `.claude/skills/vuln-scanner/` | Automatic on security keywords |
| **GitHub Copilot** | `.github/copilot-instructions.md` (flatten to single file) | `@vuln-scanner` in chat |
| **OpenAI Codex CLI** | `.codex/skills/vuln-scanner/` | Automatic + `/vuln-scan` command |
