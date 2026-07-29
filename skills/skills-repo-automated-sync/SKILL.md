---
name: skills-repo-automated-sync
description: Auto-sync Hermes skills to a GitHub repo via cron job.
---

# Skills Repo Automated Sync

**Trigger**: Use when setting up automatic sync between Hermes Agent's local skills and a GitHub skills tap repository.

## Architecture

```
Hermes skills (~/.hermes/skills/)
        │
        │  Cron job (every 6h)
        ▼
scripts/sync-from-hermes.sh
        │
        │  git add + commit + push
        ▼
GitHub repo (owner/skills-repo/skills/)
        │
        │  External dirs / tap
        ▼
Hermes / other agents consume
```

## Sync Script

### Core Logic
```bash
#!/usr/bin/env bash
# Sync from Hermes → repo
# Dry-run: bash scripts/sync-from-hermes.sh
# Apply:   bash scripts/sync-from-hermes.sh --apply

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILLS_DIR="$REPO_DIR/skills"

# Resolve Hermes skills directory
if [ -d "$LOCALAPPDATA/hermes/skills" ]; then
    HERMES_DIR="$LOCALAPPDATA/hermes/skills"
elif [ -d "$HOME/.hermes/skills" ]; then
    HERMES_DIR="$HOME/.hermes/skills"
else
    echo "ERROR: Cannot find Hermes skills directory"
    exit 1
fi

# Walk Hermes skills
for skill_file in $(find "$HERMES_DIR" -maxdepth 3 -name "SKILL.md"); do
    # Normalize and extract skill name
    norm_path=$(echo "$skill_file" | sed 's|\\|/|g')
    parts=$(echo "${norm_path#$HERMES_DIR/}" | tr '/' '\n' | wc -l)
    
    if [ "$parts" -eq 2 ]; then
        # skill/SKILL.md (flat)
        name=$(echo "${norm_path#$HERMES_DIR/}" | cut -d/ -f1)
    elif [ "$parts" -eq 3 ]; then
        # category/skill/SKILL.md
        name=$(echo "${norm_path#$HERMES_DIR/}" | cut -d/ -f2)
    else
        continue
    fi
    
    # Compare and copy
    target="$SKILLS_DIR/$name/SKILL.md"
    if [ -f "$target" ] && cmp -s "$skill_file" "$target"; then
        continue  # Unchanged
    fi
    
    mkdir -p "$SKILLS_DIR/$name"
    cp "$skill_file" "$target"
    
    # Copy supporting dirs
    for sub in references templates scripts assets examples; do
        src_dir="$(dirname "$skill_file")/$sub"
        [ -d "$src_dir" ] && cp -r "$src_dir" "$SKILLS_DIR/$name/"
    done
done
```

## Cron Setup

```bash
# Copy script to Hermes scripts dir
cp scripts/sync-from-hermes.sh ~/AppData/Local/hermes/scripts/

# Register cron (no-agent mode — runs script, no LLM)
hermes cron-job create \
  --name skills-sync-to-github \
  --schedule "every 6h" \
  --script sync-from-hermes.sh \
  --no-agent \
  --deliver local
```

## Git Operations in the Script

```bash
cd "$REPO_DIR"
git add -A
if ! git diff --cached --quiet; then
    git commit -m "Sync skills from Hermes — $(date '+%Y-%m-%d %H:%M')"
    git push origin main
fi
```

## Two-Way Flow

| Direction | Mechanism | Frequency |
|-----------|-----------|-----------|
| Hermes → GitHub | Cron job runs sync script | Every 6 hours |
| GitHub → Hermes | External dirs in config.yaml | Instant (on each session) |
| GitHub → Other users | They clone/pull the repo | On demand |

## Pitfalls
- **Path resolution**: Windows uses `%LOCALAPPDATA%/hermes/skills` — script must check both Windows and Unix paths
- **Cron timeouts**: 1,000+ file comparisons take minutes on MSYS — runs in background
- **Deletion safety**: Sync script doesn't delete skills from repo when they're removed from Hermes (repo is the archive)
- **CRLF warnings**: Git on Windows warns about line endings — use `.gitattributes` to normalize

## Verification
```bash
# Dry-run test
bash scripts/sync-from-hermes.sh

# Check cron health
hermes cron-job list
hermes cron-job logs skills-sync-to-github

# Verify on GitHub
git log --oneline -5 origin/main
```
