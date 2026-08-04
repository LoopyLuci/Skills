#!/usr/bin/env bash
# sync-from-hermes.sh — Sync skills from Hermes Agent to this repo
#
# Copies new/updated skills from ~/.hermes/skills/ into this repo's skills/
# directory, then commits and pushes to GitHub.
#
# Optimized: uses cp -u (copy-if-newer) for bulk sync instead of
# per-file cmp/diff comparisons, making it fast enough for 1,300+ skills.
#
# Usage:
#   ./scripts/sync-from-hermes.sh              # dry-run (no changes)
#   ./scripts/sync-from-hermes.sh --apply       # actually sync
#   ./scripts/sync-from-hermes.sh --force       # sync + push immediately

set -o pipefail

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

if [ ! -d "$SKILLS_DIR" ]; then
    echo "ERROR: Skills directory not found: $SKILLS_DIR"
    exit 1
fi

cd "$REPO_DIR"

# Collect all existing repo skill names (for orphan detection)
declare -A REPO_SKILLS
while IFS= read -r d; do
    name="$(basename "$d")"
    REPO_SKILLS["$name"]=1
done < <(find "$SKILLS_DIR" -maxdepth 1 -mindepth 1 -type d 2>/dev/null || true)

copied=0
skipped=0
errors=0

# Use cp -u (copy only when source is newer) for fast bulk sync.
# This avoids per-file cmp/diff comparisons entirely.
# cp -u: copies only when SOURCE is newer or DEST is missing.
if $DRY_RUN; then
    # Dry run: show what would change using find -newer
    echo "=== Scanning for changes ==="
    
    # Find all SKILL.md files in Hermes
    while IFS= read -r skill_file; do
        skill_name="$(basename "$(dirname "$skill_file")")"
        target_file="$SKILLS_DIR/$skill_name/SKILL.md"
        
        if [ ! -f "$target_file" ]; then
            echo "  [NEW]    $skill_name"
            ((copied++)) || true
        elif [ "$skill_file" -nt "$target_file" ]; then
            echo "  [UPDATE] $skill_name"
            ((copied++)) || true
        else
            # Check supporting dirs
            skill_dir="$(dirname "$skill_file")"
            support_changed=false
            for subdir in references templates scripts assets examples; do
                if [ -d "$skill_dir/$subdir" ]; then
                    dst="$SKILLS_DIR/$skill_name/$subdir"
                    if [ ! -d "$dst" ]; then
                        support_changed=true
                        break
                    fi
                    # Check if any source file is newer than newest dest file
                    newest_src=$(find "$skill_dir/$subdir" -type f -printf '%T@\n' 2>/dev/null | sort -rn | head -1)
                    if [ -n "$newest_src" ]; then
                        newest_dst=$(find "$dst" -type f -printf '%T@\n' 2>/dev/null | sort -rn | head -1)
                        if [ -z "$newest_dst" ] || [ "$(echo "$newest_src > $newest_dst" | bc)" -eq 1 ]; then
                            support_changed=true
                            break
                        fi
                    fi
                fi
            done
            if $support_changed; then
                echo "  [UPDATE] $skill_name (support files)"
                ((copied++)) || true
            else
                ((skipped++)) || true
            fi
        fi
        unset REPO_SKILLS["$skill_name"]
    done < <(find "$HERMES_SKILLS_DIR" -maxdepth 3 -name "SKILL.md" -not -path "*/.git/*" 2>/dev/null)
else
    # Actual sync: use cp -u for bulk copy (fast)
    echo "=== Syncing ==="
    
    # Copy all SKILL.md files with cp -u (only newer sources)
    while IFS= read -r skill_file; do
        skill_name="$(basename "$(dirname "$skill_file")")"
        target_dir="$SKILLS_DIR/$skill_name"
        target_file="$target_dir/SKILL.md"
        
        # Create target dir and copy SKILL.md
        mkdir -p "$target_dir"
        
        file_changed=false
        if [ ! -f "$target_file" ]; then
            file_changed=true
        elif [ "$skill_file" -nt "$target_file" ]; then
            file_changed=true
        fi
        
        if $file_changed; then
            cp "$skill_file" "$target_file"
            echo "  [SYNCED] $skill_name"
            ((copied++)) || true
        else
            # Check supporting dirs with a single rsync-like check
            skill_dir="$(dirname "$skill_file")"
            support_changed=false
            for subdir in references templates scripts assets examples; do
                if [ -d "$skill_dir/$subdir" ]; then
                    dst="$target_dir/$subdir"
                    rm -rf "$dst" 2>/dev/null || true
                    cp -r "$skill_dir/$subdir" "$dst" 2>/dev/null || true
                    support_changed=true
                elif [ -d "$dst" ]; then
                    # Source has no subdir but dest does — keep dest as archive
                    :
                fi
            done
            if $support_changed; then
                ((copied++)) || true
            else
                ((skipped++)) || true
            fi
        fi
        unset REPO_SKILLS["$skill_name"]
    done < <(find "$HERMES_SKILLS_DIR" -maxdepth 3 -name "SKILL.md" -not -path "*/.git/*" 2>/dev/null)
fi

# Report orphans
echo ""
if [ ${#REPO_SKILLS[@]} -gt 0 ]; then
    count=${#REPO_SKILLS[@]}
    if $DRY_RUN; then
        echo "  [GONE]   $count skills in repo but not in Hermes (will NOT auto-delete)"
    else
        echo "  [ORPHAN] $count skills in repo but not in Hermes (keeping as archive)"
    fi
fi

echo ""
echo "=== Summary ==="
echo "  Copied/updated: $copied"
echo "  Skipped (unchanged): $skipped"
echo "  Archive orphans: ${#REPO_SKILLS[@]}"
echo "  Errors: $errors"

if $DRY_RUN && [ "$copied" -gt 0 ]; then
    echo ""
    echo "Dry-run — $copied changes pending. Run with --apply to apply."
    exit 0
fi

# Commit and push
if ! $DRY_RUN && { [ "$copied" -gt 0 ] || $FORCE_PUSH; }; then
    if git diff --quiet && git diff --cached --quiet && [ -z "$(git status --porcelain)" ]; then
        echo ""
        echo "  No changes to commit."
    else
        TIMESTAMP="$(date '+%Y-%m-%d %H:%M:%S')"
        git add -A
        git commit -m "Sync skills from Hermes Agent — $TIMESTAMP

${copied} skills synced (${skipped} unchanged, ${errors} errors)"
        
        if $FORCE_PUSH; then
            echo ""
            echo "  Pushing to origin/main..."
            git push origin main
        else
            echo ""
            echo "  Changes committed. Push when ready: git push origin main"
        fi
    fi
fi

echo ""
echo "=== Done ==="
