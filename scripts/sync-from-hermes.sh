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
# Resolve Hermes skills directory (supports Windows AppData path)
if [ -d "$HERMES_HOME/skills" ]; then
    HERMES_SKILLS_DIR="$HERMES_HOME/skills"
elif [ -d "$HOME/.hermes/skills" ]; then
    HERMES_SKILLS_DIR="$HOME/.hermes/skills"
elif [ -d "$LOCALAPPDATA/hermes/skills" ]; then
    HERMES_SKILLS_DIR="$LOCALAPPDATA/hermes/skills"
elif [ -d "/c/Users/$(whoami)/AppData/Local/hermes/skills" ]; then
    HERMES_SKILLS_DIR="/c/Users/$(whoami)/AppData/Local/hermes/skills"
else
    # Fallback: try common Windows path
    WIN_HOME=$(cmd /c "echo %USERPROFILE%" 2>/dev/null | tr -d '\r')
    if [ -n "$WIN_HOME" ] && [ -d "${WIN_HOME}/AppData/Local/hermes/skills" ]; then
        HERMES_SKILLS_DIR="${WIN_HOME}/AppData/Local/hermes/skills"
    else
        echo "ERROR: Cannot find Hermes skills directory"
        exit 1
    fi
fi
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

# Walk Hermes skills (handles both category/skill/SKILL.md and flat skill/SKILL.md)
while IFS= read -r skill_file; do
    # Normalize path separators for comparison
    norm_skill_file="$(echo "$skill_file" | sed 's|\\|/|g')"
    norm_skills_dir="$(echo "$HERMES_SKILLS_DIR" | sed 's|\\|/|g')"
    
    # Extract the relative path under the skills directory
    rel_path="${norm_skill_file#$norm_skills_dir/}"
    
    # Count path components — determine if this is category/skill/SKILL.md or just skill/SKILL.md
    parts_count="$(echo "$rel_path" | tr '/' '\n' | wc -l)"
    
    skill_name=""
    if [ "$parts_count" -eq 2 ]; then
        # skill/SKILL.md (flat)
        skill_name="$(echo "$rel_path" | cut -d/ -f1)"
    elif [ "$parts_count" -eq 3 ]; then
        # category/skill/SKILL.md  
        skill_name="$(echo "$rel_path" | cut -d/ -f2)"
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
            skill_dir="$(dirname "$skill_file")"
            for subdir in references templates scripts assets examples; do
                src="$skill_dir/$subdir"
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
        skill_dir="$(dirname "$skill_file")"
        for subdir in references templates scripts assets examples; do
            src="$skill_dir/$subdir"
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
