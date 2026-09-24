#!/bin/bash
# Two-way skills sync wrapper for cron.
# Syncs Hermes ↔ LoopyLuci/Skills repo, commits, and pushes.

set -o pipefail

REPO_DIR="Z:/Projects/Skills/LoopyLuci-skills"
PY="$APPDATA/hermes/hermes-agent/venv/Scripts/python.exe"

# Fallback: try to find python
if [ ! -f "$PY" ]; then
    PY=$(which python 2>/dev/null || which python3 2>/dev/null)
fi

if [ -z "$PY" ]; then
    echo "ERROR: Cannot find Python"
    exit 1
fi

cd "$REPO_DIR" || exit 1

# Run bidirectional sync with apply + push
"$PY" scripts/sync-machine.py --apply --force 2>&1
