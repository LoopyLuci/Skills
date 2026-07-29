#!/usr/bin/env bash
# sync-from-hermes.sh — Sync skills from Hermes Agent to this repo
#
# Copies new/updated skills from ~/.hermes/skills/ into this repo's skills/
# directory, preserves category metadata, then commits and pushes to GitHub.
#
# Usage:
#   ./scripts/sync-from-hermes.sh              # dry-run (no changes)
#   ./scripts/sync-from-hermes.sh --apply       # actually sync
#   ./scripts/sync-from-hermes.sh --force       # sync + push immediately
#
# Installing as scheduled cron (Hermes Agent):
#   hermes cron-job create \
#     --name "skills-sync" \
#     --schedule "every 6h" \
#     --script "D:\Projects\Skills\scripts\sync-from-hermes.sh" \
#     --no-agent

set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILLS_DIR="$REPO_DIR/skills"
HERMES_SKILLS_DIR="${HERMES_HOME:-$HOME/.hermes}/skills"
DRY_RUN=true
FORCE_PUSH=false

for arg in "$@"; do
    case "$arg" in
        --apply) DRY_RUN=false ;;
        --force) DRY_RUN=false; FORCE_PUSH=true ;;
    esac
done

echo "=== Skills Sync ==="
echo "  Repo skills:      $SKILLS_DIR"
echo "  Hermes skills:    $HERMES_SKILLS_DIR"
echo "  Dry run:          $DRY_RUN"
echo ""

if [ ! -d "$HERMES_SKILLS_DIR" ]; then
    echo "ERROR: Hermes skills directory not found: $HERMES_SKILLS_DIR"
    exit 1
fi

if [ ! -d "$SKILLS_DIR/.git" ] && [ ! -d "$REPO_DIR/.git" ]; then
    echo "ERROR: Not a git repository: $REPO_DIR"
    exit 1
fi

# Collect all existing repo skill names (for delete detection)
declare -A REPO_SKILLS
while IFS= read -r d; do
    name="$(basename "$d")"
    REPO_SKILLS["$name"]=1
done < <(find "$SKILLS_DIR" -maxdepth 1 -type d -not -name "." 2>/dev/null || echo "")

copied=0
updated=0
skipped=0
errors=0

# Walk Hermes skills in category/<skill>/SKILL.md format
while IFS= read -r skill_file; do
    # Extract relative path from HERMES_SKILLS_DIR
    rel_path="${skill_file#$HERMES_SKILLS_DIR/}"
    # rel_path is like "creative/ascii-art/SKILL.md" or "blocklist-manager/SKILL.md"
    category=""
    skill_name=""
    
    if [[ "$rel_path" == */*/* ]]; then
        # category/skill/SKILL.md
        category="$(echo "$rel_path" | cut -d/ -f1)"
        skill_name="$(echo "$rel_path" | cut -d/ -f2)"
    elif [[ "$rel_path" == */* ]]; then
        # skill/SKILL.md (flat at root of Hermes skills)
        skill_name="$(echo "$rel_path" | cut -d/ -f1)"
    fi
    
    [ -z "$skill_name" ] && { ((errors++)) || true; continue; }
    
    target_dir="$SKILLS_DIR/$skill_name"
    target_file="$target_dir/SKILL.md"
    
    # Check if this is already known in the repo
    if [ -f "$target_file" ]; then
        # Compare content
        if cmp -s "$skill_file" "$target_file"; then
            # Check supporting files too
            support_changed=false
            for subdir in references templates scripts assets examples; do
                src="$HERMES_SKILLS_DIR/$category/$skill_name/$subdir"
                dst="$target_dir/$subdir"
                if [ -d "$src" ]; then
                    if [ ! -d "$dst" ] || ! diff -rq "$src" "$dst" >/dev/null 2>&1; then
                        support_changed=true
                        break
                    fi
                fi
            done
            if ! $support_changed; then
                ((skipped++)) || true
                continue
            fi
        fi
    fi
    
    # Copy or update
    if $DRY_RUN; then
        if [ -f "$target_file" ]; then
            echo "  [UPDATE] $skill_name"
        else
            echo "  [NEW]    $skill_name"
        fi
        ((copied++)) || true
    else
        mkdir -p "$target_dir"
        cp "$skill_file" "$target_file"
        
        # Copy supporting directories
        for subdir in references templates scripts assets examples; do
            src="$HERMES_SKILLS_DIR/$category/$skill_name/$subdir"
            if [ -d "$src" ]; then
                dst="$target_dir/$subdir"
                rm -rf "$dst" 2>/dev/null || true
                cp -r "$src" "$dst"
            fi
        done
        
        echo "  [SYNCED] $skill_name"
        ((copied++)) || true
    fi
    
    # Remove from REPO_SKILLS set (so remaining = deleted)
    unset REPO_SKILLS["$skill_name"]
    
done < <(find "$HERMES_SKILLS_DIR" -maxdepth 3 -name "SKILL.md" -not -path "*/.git/*" 2>/dev/null || echo "")

# Report deleted skills (skills in repo but gone from Hermes)
deleted=0
if [ ${#REPO_SKILLS[@]} -gt 0 ]; then
    if $DRY_RUN; then
        for name in "${!REPO_SKILLS[@]}"; do
            echo "  [GONE]   $name (in repo but not in Hermes — will NOT auto-delete)"
        done
    else
        for name in "${!REPO_SKILLS[@]}"; do
            echo "  [ORPHAN] $name (in repo but not in Hermes — keeping as archive)"
        done
    fi
    deleted=${#REPO_SKILLS[@]}
fi

echo ""
echo "=== Summary ==="
echo "  Copied/updated: $copied"
echo "  Skipped (unchanged): $skipped"
echo "  Archive orphans: $deleted"
echo "  Errors: $errors"

if $DRY_RUN && [ "$copied" -gt 0 ]; then
    echo ""
    echo "Dry-run — $copied changes pending. Run with --apply to apply."
    exit 0
fi

# Commit and push
if ! $DRY_RUN && { [ "$copied" -gt 0 ] || $FORCE_PUSH; }; then
    cd "$REPO_DIR"
    
    # Check if there are actual changes
    if git diff --quiet && git diff --cached --quiet && [ -z "$(git status --porcelain)" ]; then
        echo "  No changes to commit."
    else
        TIMESTAMP="$(date '+%Y-%m-%d %H:%M:%S')"
        git add -A
        git commit -m "Sync skills from Hermes Agent — $TIMESTAMP

${copied} skills synced (${skipped} unchanged, ${errors} errors)"
        
        if $FORCE_PUSH; then
            echo "  Pushing to origin/main..."
            git push origin main
        else
            echo "  Changes committed. Push when ready: git push origin main"
        fi
    fi
fi

echo "=== Done ==="
