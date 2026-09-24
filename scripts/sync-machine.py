"""
Machine-local bidirectional skill sync.
Hermes ↔ LoopyLuci/Skills repo with auto-commit + push.

Usage:
  python scripts/sync-machine.py              # dry run
  python scripts/sync-machine.py --apply       # apply changes
  python scripts/sync-machine.py --force       # apply + push
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

# --- Machine-local paths ---
REPO_DIR = Path(r"Z:\Projects\Skills\LoopyLuci-skills")
REPO_SKILLS_DIR = REPO_DIR / "skills"
HERMES_SKILLS_DIR = Path(os.environ.get(
    "HERMES_HOME",
    str(Path.home() / "AppData" / "Local" / "hermes")
)) / "skills"

FORCE_PUSH = "--force" in sys.argv
DRY_RUN = "--apply" not in sys.argv and not FORCE_PUSH
APPLY = not DRY_RUN

PULL_FIRST = True  # pull latest from origin before sync

SUPPORT_DIRS = ["references", "templates", "scripts", "assets", "examples"]

print("=== Bidirectional Skills Sync (Machine) ===")
print(f"  Repo:            {REPO_DIR}")
print(f"  Repo skills:     {REPO_SKILLS_DIR}")
print(f"  Hermes skills:   {HERMES_SKILLS_DIR}")
print(f"  Apply:           {APPLY}")
print(f"  Force push:      {FORCE_PUSH}")

if not REPO_DIR.is_dir():
    print(f"ERROR: Repo not found: {REPO_DIR}")
    sys.exit(1)
if not REPO_SKILLS_DIR.is_dir():
    print(f"ERROR: Repo skills not found: {REPO_SKILLS_DIR}")
    sys.exit(1)
if not HERMES_SKILLS_DIR.is_dir():
    print(f"ERROR: Hermes skills not found: {HERMES_SKILLS_DIR}")
    sys.exit(1)

# Step 0: Pull latest from origin
if PULL_FIRST and not DRY_RUN:
    os.chdir(REPO_DIR)
    subprocess.run(["git", "fetch", "origin"], capture_output=True)
    # Reset to origin/main to avoid merge conflicts (remote is authoritative)
    subprocess.run(["git", "reset", "--hard", "origin/main"], capture_output=True)
    print("\n  Pulled latest from origin/main")

# Build maps: name → (dir, SKILL.md path, mtime)
def skill_entries(skills_dir: Path):
    for d in skills_dir.iterdir():
        if not d.is_dir():
            continue
        md = d / "SKILL.md"
        if md.exists():
            yield d.name, d, md

repo_map = {}
for name, d, md in skill_entries(REPO_SKILLS_DIR):
    repo_map[name] = (d, md, md.stat().st_mtime)

hermes_map = {}
for name, d, md in skill_entries(HERMES_SKILLS_DIR):
    hermes_map[name] = (d, md, md.stat().st_mtime)

all_names = set(repo_map) | set(hermes_map)

new_to_hermes = []
new_to_repo = []
updated_hermes = []
updated_repo = []
skipped = 0

def sync_support_dirs(src_dir, dst_dir):
    changed = False
    for sub in SUPPORT_DIRS:
        src_sub = src_dir / sub
        if not src_sub.is_dir():
            continue
        dst_sub = dst_dir / sub
        if dst_sub.exists():
            src_files = [f for f in src_sub.rglob("*") if f.is_file()]
            if not src_files:
                continue
            src_newest = max(f.stat().st_mtime for f in src_files)
            dst_files = [f for f in dst_sub.rglob("*") if f.is_file()]
            if dst_files:
                dst_newest = max(f.stat().st_mtime for f in dst_files)
            else:
                dst_newest = 0
            if src_newest > dst_newest:
                shutil.rmtree(dst_sub)
                shutil.copytree(src_sub, dst_sub)
                changed = True
        else:
            shutil.copytree(src_sub, dst_sub)
            changed = True
    return changed

# --- Direction 1: Repo → Hermes ---
for name in sorted(all_names):
    if name not in repo_map:
        continue
    repo_dir, repo_md, repo_mtime = repo_map[name]

    if name not in hermes_map:
        if APPLY:
            dst_dir = HERMES_SKILLS_DIR / name
            dst_dir.mkdir(exist_ok=True)
            shutil.copy2(repo_md, dst_dir / "SKILL.md")
            sync_support_dirs(repo_dir, dst_dir)
        new_to_hermes.append(name)
    else:
        _, _, hermes_mtime = hermes_map[name]
        if repo_mtime > hermes_mtime:
            if APPLY:
                dst_dir = HERMES_SKILLS_DIR / name
                dst_dir.mkdir(exist_ok=True)
                shutil.copy2(repo_md, dst_dir / "SKILL.md")
                sync_support_dirs(repo_dir, dst_dir)
            updated_hermes.append(name)
        else:
            skipped += 1

# --- Direction 2: Hermes → Repo ---
for name in sorted(all_names):
    if name not in hermes_map:
        continue
    hermes_dir, hermes_md, hermes_mtime = hermes_map[name]

    if name not in repo_map:
        if APPLY:
            dst_dir = REPO_SKILLS_DIR / name
            dst_dir.mkdir(exist_ok=True)
            shutil.copy2(hermes_md, dst_dir / "SKILL.md")
            sync_support_dirs(hermes_dir, dst_dir)
        new_to_repo.append(name)
    else:
        _, _, repo_mtime = repo_map[name]
        if hermes_mtime > repo_mtime:
            if APPLY:
                dst_dir = REPO_SKILLS_DIR / name
                dst_dir.mkdir(exist_ok=True)
                shutil.copy2(hermes_md, dst_dir / "SKILL.md")
                sync_support_dirs(hermes_dir, dst_dir)
            updated_repo.append(name)
        else:
            skipped += 1

# Summary
print("\n=== Summary ===")
print(f"  New Hermes←Repo:    {len(new_to_hermes)}")
print(f"  New Repo←Hermes:    {len(new_to_repo)}")
print(f"  Updated Hermes:     {len(updated_hermes)}")
print(f"  Updated Repo:       {len(updated_repo)}")
print(f"  Unchanged:          {skipped}")
total_changes = len(new_to_hermes) + len(new_to_repo) + len(updated_hermes) + len(updated_repo)
print(f"  Total changes:      {total_changes}")

if DRY_RUN:
    if total_changes > 0:
        print(f"\nDry-run — {total_changes} changes pending. Run with --apply to apply.")
    else:
        print("\nAlready in sync — no changes needed.")
    sys.exit(0)

# Commit and push
if total_changes > 0 or FORCE_PUSH:
    os.chdir(REPO_DIR)
    status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    if not status.stdout.strip():
        print("\n  No changes to commit.")
        sys.exit(0)
    timestamp = subprocess.check_output(["date", "+%Y-%m-%d %H:%M:%S"], text=True).strip()
    subprocess.run(["git", "add", "-A"], check=True)
    msg = (
        f"Sync (two-way) Hermes ↔ Repo — {timestamp}\n\n"
        f"{len(new_to_hermes)} pulled to Hermes, {len(new_to_repo)} pushed to repo, "
        f"{len(updated_hermes)} updated in Hermes, {len(updated_repo)} updated in repo"
    )
    subprocess.run(["git", "commit", "-m", msg], check=True)
    if FORCE_PUSH:
        print("\n  Pushing to origin/main...")
        subprocess.run(["git", "push", "origin", "main"], check=True)
    else:
        print("\n  Changes committed. Push when ready: git push origin main")
else:
    print("\n  No changes to commit.")

print("\n=== Done ===")
