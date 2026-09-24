"""
Bidirectional skill sync between Hermes Agent and LoopyLuci/Skills repo.
Designed for Windows — resolves paths dynamically, no hardcoded drives.

Hermes structure:  skills/<category>/<skill-name>/SKILL.md (nested)
Repo structure:    skills/<skill-name>/SKILL.md (flat)

Sync strategy:
  1. Pull latest from origin/main
  2. Repo → Hermes: copy repo skills that are newer or missing in Hermes
  3. Hermes → Repo: copy Hermes skills that are newer or missing in repo
  4. Conflicts: mtime wins (newer overwrites older)
  5. Commit and push all changes

Usage:
  python scripts/sync-hermes-windows.py            # dry run
  python scripts/sync-hermes-windows.py --apply    # apply changes
  python scripts/sync-hermes-windows.py --force    # apply + push immediately
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

# --- Resolve paths dynamically ---
REPO_DIR = Path(__file__).resolve().parent.parent
REPO_SKILLS_DIR = REPO_DIR / "skills"

# Hermes skills directory
HERMES_HOME = os.environ.get("HERMES_HOME", "")
if HERMES_HOME:
    HERMES_SKILLS_DIR = Path(HERMES_HOME) / "skills"
else:
    local_app_data = os.environ.get("LOCALAPPDATA", "")
    if local_app_data:
        HERMES_SKILLS_DIR = Path(local_app_data) / "hermes" / "skills"
    else:
        HERMES_SKILLS_DIR = Path.home() / ".hermes" / "skills"

DRY_RUN = "--apply" not in sys.argv and "--force" not in sys.argv
APPLY = not DRY_RUN
FORCE_PUSH = "--force" in sys.argv
PULL_FIRST = "--no-pull" not in sys.argv

SUPPORT_DIRS = ["references", "templates", "scripts", "assets", "examples"]

SKIP_DIRS = {
    ".archive", ".curator_backups", ".bundled_manifest", ".curator_state",
    ".usage.json", ".usage.json.lock", ".hub", ".locks",
    ".skills_prompt_snapshot.json", ".curator_ledger.jsonl", ".env",
    ".env.bak", ".backup.lock", ".mcp-discovery.lock",
    ".npm_lock_hash_b630b7dc6242", ".npm_lock_hash_b630b7dc6242_desktop",
    ".processes_2sy4qh00.tmp", ".update_check", ".update_exit_code",
}

print("=== Hermes <-> Repo Bidirectional Sync (Windows) ===")
print(f"  Repo:            {REPO_DIR}")
print(f"  Repo skills:     {REPO_SKILLS_DIR}")
print(f"  Hermes skills:   {HERMES_SKILLS_DIR}")
print(f"  Dry run:         {DRY_RUN}")
print(f"  Force push:      {FORCE_PUSH}")
print(f"  Pull first:      {PULL_FIRST}")
print()

if not REPO_SKILLS_DIR.is_dir():
    print(f"ERROR: Repo skills directory not found: {REPO_SKILLS_DIR}")
    sys.exit(1)
if not HERMES_SKILLS_DIR.is_dir():
    print(f"ERROR: Hermes skills directory not found: {HERMES_SKILLS_DIR}")
    sys.exit(1)

if PULL_FIRST and APPLY:
    print("Pulling latest from origin/main...")
    os.chdir(REPO_DIR)
    fetch = subprocess.run(["git", "fetch", "origin"], capture_output=True, text=True)
    if fetch.returncode != 0:
        print(f"  WARNING: git fetch failed: {fetch.stderr.strip()}")
    else:
        reset = subprocess.run(["git", "reset", "--hard", "origin/main"], capture_output=True, text=True)
        if reset.returncode == 0:
            print("  Pulled latest from origin/main")
        else:
            print(f"  WARNING: git reset failed: {reset.stderr.strip()}")
    print()


def get_hermes_flat_skills():
    skills = {}
    for category_dir in HERMES_SKILLS_DIR.iterdir():
        if not category_dir.is_dir():
            continue
        cat_name = category_dir.name
        if cat_name.startswith(".") or cat_name in SKIP_DIRS:
            continue
        direct_md = category_dir / "SKILL.md"
        if direct_md.exists():
            skills[cat_name] = (category_dir, direct_md, direct_md.stat().st_mtime)
            continue
        for skill_dir in category_dir.iterdir():
            if not skill_dir.is_dir():
                continue
            skill_md = skill_dir / "SKILL.md"
            if skill_md.exists():
                skills[skill_dir.name] = (skill_dir, skill_md, skill_md.stat().st_mtime)
    return skills


def get_repo_flat_skills():
    skills = {}
    for skill_dir in REPO_SKILLS_DIR.iterdir():
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if skill_md.exists():
            skills[skill_dir.name] = (skill_dir, skill_md, skill_md.stat().st_mtime)
    return skills


def sync_support_dirs(src_dir, dst_dir):
    for sub in SUPPORT_DIRS:
        src_sub = src_dir / sub
        if not src_sub.is_dir():
            continue
        dst_sub = dst_dir / sub
        if dst_sub.exists():
            shutil.rmtree(dst_sub)
        shutil.copytree(src_sub, dst_sub)


hermes_map = get_hermes_flat_skills()
repo_map = get_repo_flat_skills()
all_names = set(hermes_map) | set(repo_map)

print(f"  Hermes skills: {len(hermes_map)}")
print(f"  Repo skills:   {len(repo_map)}")
print(f"  Total unique:  {len(all_names)}")
print()

new_to_hermes = []
new_to_repo = []
updated_hermes = []
updated_repo = []
skipped = 0

for name in sorted(all_names):
    if name not in repo_map:
        continue
    repo_dir, repo_md, repo_mtime = repo_map[name]
    if name not in hermes_map:
        if APPLY:
            dst_dir = HERMES_SKILLS_DIR / name
            dst_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(repo_md, dst_dir / "SKILL.md")
            sync_support_dirs(repo_dir, dst_dir)
        new_to_hermes.append(name)
    else:
        hermes_dir, hermes_md, hermes_mtime = hermes_map[name]
        if repo_mtime > hermes_mtime:
            if APPLY:
                dst_dir = hermes_dir
                shutil.copy2(repo_md, dst_dir / "SKILL.md")
                sync_support_dirs(repo_dir, dst_dir)
            updated_hermes.append(name)
        else:
            skipped += 1

for name in sorted(all_names):
    if name not in hermes_map:
        continue
    hermes_dir, hermes_md, hermes_mtime = hermes_map[name]
    if name not in repo_map:
        if APPLY:
            dst_dir = REPO_SKILLS_DIR / name
            dst_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(hermes_md, dst_dir / "SKILL.md")
            sync_support_dirs(hermes_dir, dst_dir)
        new_to_repo.append(name)
    else:
        repo_dir, repo_md, repo_mtime = repo_map[name]
        if hermes_mtime > repo_mtime:
            if APPLY:
                dst_dir = REPO_SKILLS_DIR / name
                dst_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy2(hermes_md, dst_dir / "SKILL.md")
                sync_support_dirs(hermes_dir, dst_dir)
            updated_repo.append(name)
        else:
            skipped += 1

total_changes = len(new_to_hermes) + len(new_to_repo) + len(updated_hermes) + len(updated_repo)

print("=== Summary ===")
print(f"  New to Hermes (from repo):   {len(new_to_hermes)}")
print(f"  New to Repo (from Hermes):   {len(new_to_repo)}")
print(f"  Updated in Hermes:           {len(updated_hermes)}")
print(f"  Updated in Repo:             {len(updated_repo)}")
print(f"  Unchanged:                   {skipped}")
print(f"  Total changes:               {total_changes}")
print()

if DRY_RUN:
    if total_changes > 0:
        print(f"Dry-run -- {total_changes} changes pending. Run with --apply to apply.")
    else:
        print("Already in sync -- no changes needed.")
    sys.exit(0)

if APPLY and total_changes > 0:
    os.chdir(REPO_DIR)
    status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    if not status.stdout.strip():
        print("  No changes to commit (files identical).")
        sys.exit(0)
    timestamp = subprocess.check_output(["date", "+%Y-%m-%d %H:%M:%S"], text=True).strip()
    subprocess.run(["git", "add", "-A"], check=True)
    msg = (
        f"Sync (two-way) Hermes <-> Repo -- {timestamp}\n\n"
        f"{len(new_to_hermes)} pulled to Hermes, {len(new_to_repo)} pushed to repo, "
        f"{len(updated_hermes)} updated in Hermes, {len(updated_repo)} updated in repo"
    )
    subprocess.run(["git", "commit", "-m", msg], check=True)
    print(f"  Committed: {msg.splitlines()[0]}")
    if FORCE_PUSH:
        print("\n  Pushing to origin/main...")
        push = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
        if push.returncode == 0:
            print("  Pushed to origin/main")
        else:
            print(f"  Push failed: {push.stderr.strip()}")
            sys.exit(1)
    else:
        print("\n  Changes committed locally. Push with --force or: git push origin main")

print()
print("=== Done ===")
