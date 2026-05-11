#!/usr/bin/env bash
# scripts/install-hooks.sh
# One-liner to wire the pre-commit hook into .git/hooks/
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cp "$REPO_ROOT/hooks/pre-commit" "$REPO_ROOT/.git/hooks/pre-commit"
chmod +x "$REPO_ROOT/.git/hooks/pre-commit"
echo "✓ pre-commit hook installed."
