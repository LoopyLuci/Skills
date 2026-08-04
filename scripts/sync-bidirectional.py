"""
Bidirectional skill sync between Hermes Agent skills directory and
the GitHub-backed repo, with automatic commit + push.

Sync strategy:
  1. Repo → Hermes: copy any repo skills that are newer or missing in Hermes
  2. Hermes → Repo: copy any Hermes skills that are newer or missing in Repo
  3. Conflicts (both modified): mtime wins — newer version overwrites older
  4. After merging: commit changed skills, push to origin/main
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_DIR = Path(r"D:\Projects\Skills")
REPO_SKILLS_DIR = REPO_DIR / "skills"
HERMES_SKILLS_DIR = Path(os.environ.get(
    "HERMES_HOME",
    str(Path.home() / "AppData" / "Local" / "hermes")
)) / "skills"

FORCE_PUSH = "--force" in sys.argv
DRY_RUN = "--dry-run" in sys.argv

print("=== Bidirectional Skills Sync ===")
print(f"  Hermes skills:    {HERMES_SKILLS_DIR}")
print(f"  Repo skills:      {REPO_SKILLS_DIR}")
print(f"  Dry run:          {DRY_RUN}")

for d in [HERMES_SKILLS_DIR, REPO_SKILLS_DIR]:
    if not d.is_dir():
        print(f"ERROR: Directory not found: {d}")
        sys.exit(1)

SUPPORT_DIRS = ["references", "templates", "scripts", "assets", "examples"]

def skill_entries(skills_dir: Path):
    """Yield (skill_name, skill_dir_path, SKILL.md_path) for each skill."""
    for d in skills_dir.iterdir():
        if not d.is_dir():
            continue
        md = d / "SKILL.md"
        if md.exists():
            yield d.name, d, md

def sync_file(src: Path, dst: Path, label: str, copied: list, updated: list):
    """Copy src → dst if newer/missing. Track changes."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not dst.exists():
        shutil.copy2(src, dst)
        copied.append(label)
        return True
    src_mtime = src.stat().st_mtime
    dst_mtime = dst.stat().st_mtime
    if src_mtime > dst_mtime:
        shutil.copy2(src, dst)
        updated.append(label)
        return True
    return False

def sync_support_dirs(src_dir: Path, dst_dir: Path, copied: list, updated: list):
    """Copy supporting dirs from src to dst."""
    changed = False
    for sub in SUPPORT_DIRS:
        src_sub = src_dir / sub
        if not src_sub.is_dir():
            continue
        dst_sub = dst_dir / sub
        if dst_sub.exists():
            # Check if source is newer
            src_newest = max(f.stat().st_mtime for f in src_sub.rglob("*") if f.is_file())
            dst_files = [f for f in dst_sub.rglob("*") if f.is_file()]
            if dst_files:
                dst_newest = max(f.stat().st_mtime for f in dst_files)
            else:
                dst_newest = 0
            if src_newest > dst_newest:
                shutil.rmtree(dst_sub)
                shutil.copytree(src_sub, dst_sub)
                updated.append(f"{src_dir.name}/{sub}")
                changed = True
        else:
            shutil.copytree(src_sub, dst_sub)
            copied.append(f"{src_dir.name}/{sub}")
            changed = True
    return changed

# Build maps: name → (dir, SKILL.md path, mtime)
repo_map = {}
for name, d, md in skill_entries(REPO_SKILLS_DIR):
    repo_map[name] = (d, md, md.stat().st_mtime)

hermes_map = {}
for name, d, md in skill_entries(HERMES_SKILLS_DIR):
    hermes_map[name] = (d, md, md.stat().st_mtime)

all_names = set(repo_map) | set(hermes_map)

copied = []
updated = []
skipped = 0

# --- Direction 1: Repo → Hermes (for skills not in Hermes, or Hermes is older) ---
for name in sorted(all_names):
    if name not in repo_map:
        continue  # Only in Hermes, handled below
    
    repo_dir, repo_md, repo_mtime = repo_map[name]
    
    if name not in hermes_map:
        # New skill: copy to Hermes
        if not DRY_RUN:
            dst_dir = HERMES_SKILLS_DIR / name
            dst_dir.mkdir(exist_ok=True)
            shutil.copy2(repo_md, dst_dir / "SKILL.md")
            sync_support_dirs(repo_dir, dst_dir, copied, updated)
            copied.append(name)
        else:
            print(f"  [NEW→HERMES] {name}")
            copied.append(name)
    else:
        # In both: compare mtime
        hermes_dir, hermes_md, hermes_mtime = hermes_map[name]
        if repo_mtime > hermes_mtime:
            # Repo is newer → update Hermes
            if not DRY_RUN:
                dst_dir = HERMES_SKILLS_DIR / name
                dst_dir.mkdir(exist_ok=True)
                shutil.copy2(repo_md, dst_dir / "SKILL.md")
                sync_support_dirs(repo_dir, dst_dir, copied, updated)
                updated.append(name)
            else:
                print(f"  [REPO→HERMES] {name}")
                updated.append(name)
        elif repo_mtime < hermes_mtime:
            # Hermes is newer → handled below
            pass
        else:
            skipped += 1

# --- Direction 2: Hermes → Repo (for skills not in Repo, or Repo is older) ---
for name in sorted(all_names):
    if name not in hermes_map:
        continue  # Only in repo, handled above
    
    hermes_dir, hermes_md, hermes_mtime = hermes_map[name]
    
    if name not in repo_map:
        # New skill: copy to repo
        if not DRY_RUN:
            dst_dir = REPO_SKILLS_DIR / name
            dst_dir.mkdir(exist_ok=True)
            shutil.copy2(hermes_md, dst_dir / "SKILL.md")
            sync_support_dirs(hermes_dir, dst_dir, copied, updated)
            copied.append(name)
        else:
            print(f"  [NEW→REPO] {name}")
            copied.append(name)
    else:
        # In both: repo_mtime < hermes_mtime (only if Hermes is newer)
        repo_dir, repo_md, repo_mtime = repo_map[name]
        if hermes_mtime > repo_mtime:
            if not DRY_RUN:
                dst_dir = REPO_SKILLS_DIR / name
                dst_dir.mkdir(exist_ok=True)
                shutil.copy2(hermes_md, dst_dir / "SKILL.md")
                sync_support_dirs(hermes_dir, dst_dir, copied, updated)
                updated.append(name)
            else:
                print(f"  [HERMES→REPO] {name}")
                updated.append(name)
        elif hermes_mtime > repo_mtime:
            pass  # same check
        else:
            skipped += 1

# De-duplicate changes
copied = list(set(copied))
updated = list(set(updated))

# Summary
print("")
print("=== Summary ===")
print(f"  New skills:       {len(copied)}")
print(f"  Updated skills:   {len(updated)}")
print(f"  Unchanged:        {skipped}")
print(f"  Total tracked:    {len(all_names)}")

if DRY_RUN:
    if copied or updated:
        print(f"\nDry-run — {len(copied) + len(updated)} changes pending. Run without --dry-run to apply.")
    else:
        print("\nAlready in sync — no changes needed.")
    sys.exit(0)

# Commit and push
os.chdir(REPO_DIR)
status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
has_changes = bool(status.stdout.strip())

if not has_changes:
    print("\n  No changes to commit.")
    sys.exit(0)

timestamp = subprocess.check_output(["date", "+%Y-%m-%d %H:%M:%S"], text=True).strip()
subprocess.run(["git", "add", "-A"], check=True)
msg = (
    f"Sync (two-way) Hermes ↔ Repo — {timestamp}\n\n"
    f"{len(copied)} new, {len(updated)} updated, {skipped} unchanged"
)
subprocess.run(["git", "commit", "-m", msg], check=True)

if FORCE_PUSH:
    print("\n  Pushing to origin/main...")
    subprocess.run(["git", "push", "origin", "main"], check=True)
else:
    print("\n  Changes committed. Push when ready: git push origin main")

print("")
print("=== Done ===")
