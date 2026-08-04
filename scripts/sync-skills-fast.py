"""
Fast skill sync from Hermes Agent to D:\Projects\Skills\skills/
Replaces the slow per-file cmp/diff loop with a bulk copy-if-newer strategy.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_DIR = Path(r"D:\Projects\Skills")
SKILLS_DIR = REPO_DIR / "skills"
HERMES_SKILLS_DIR = Path(os.environ.get(
    "HERMES_HOME",
    str(Path.home() / "AppData" / "Local" / "hermes" / "skills")
))

FORCE_PUSH = "--force" in sys.argv
APPLY = "--apply" in sys.argv or FORCE_PUSH
DRY_RUN = not APPLY

print("=== Skills Sync ===")
print(f"  Repo skills:      {SKILLS_DIR}")
print(f"  Hermes skills:    {HERMES_SKILLS_DIR}")
print(f"  Dry run:          {DRY_RUN}")

if not HERMES_SKILLS_DIR.is_dir():
    print(f"ERROR: Hermes skills directory not found: {HERMES_SKILLS_DIR}")
    sys.exit(1)

if not SKILLS_DIR.is_dir():
    print(f"ERROR: Skills directory not found: {SKILLS_DIR}")
    sys.exit(1)

# Build set of existing repo skill names
repo_skills = {d.name for d in SKILLS_DIR.iterdir() if d.is_dir()}

copied = 0
skipped = 0
orphans = []

for skill_dir in sorted(HERMES_SKILLS_DIR.iterdir()):
    if not skill_dir.is_dir():
        continue
    
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        # Maybe it's a category folder? Check subdirectories
        for sub in skill_dir.iterdir():
            sub_md = sub / "SKILL.md"
            if sub_md.exists():
                target_dir = SKILLS_DIR / sub.name
                target_file = target_dir / "SKILL.md"
                changed = False
                
                if not target_file.exists():
                    changed = True
                else:
                    src_stat = sub_md.stat()
                    dst_stat = target_file.stat()
                    if src_stat.st_mtime > dst_stat.st_mtime:
                        changed = True
                
                if changed:
                    if DRY_RUN:
                        print(f"  [UPDATE] {sub.name}")
                    else:
                        target_dir.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(sub_md, target_file)
                        # Copy supporting dirs if newer
                        for support in ["references", "templates", "scripts", "assets", "examples"]:
                            src_sup = sub / support
                            if src_sup.is_dir():
                                dst_sup = target_dir / support
                                if dst_sup.exists():
                                    shutil.rmtree(dst_sup)
                                shutil.copytree(src_sup, dst_sup)
                        print(f"  [SYNCED] {sub.name}")
                    copied += 1
                else:
                    skipped += 1
                
                repo_skills.discard(sub.name)
        continue
    
    # Flat skill/SKILL.md
    skill_name = skill_dir.name
    target_dir = SKILLS_DIR / skill_name
    target_file = target_dir / "SKILL.md"
    changed = False
    
    if not target_file.exists():
        changed = True
    else:
        src_stat = skill_md.stat()
        dst_stat = target_file.stat()
        if src_stat.st_mtime > dst_stat.st_mtime:
            changed = True
    
    if changed:
        if DRY_RUN:
            print(f"  [UPDATE] {skill_name}")
        else:
            target_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(skill_md, target_file)
            # Copy supporting dirs if newer
            for support in ["references", "templates", "scripts", "assets", "examples"]:
                src_sup = skill_dir / support
                if src_sup.is_dir():
                    dst_sup = target_dir / support
                    if dst_sup.exists():
                        shutil.rmtree(dst_sup)
                    shutil.copytree(src_sup, dst_sup)
            print(f"  [SYNCED] {skill_name}")
        copied += 1
    else:
        skipped += 1
    
    repo_skills.discard(skill_name)

# Orphans
if repo_skills:
    orphans = sorted(repo_skills)
    if DRY_RUN:
        print(f"\n  [GONE]   {len(orphans)} skills in repo but not in Hermes (will NOT auto-delete)")
    else:
        print(f"\n  [ORPHAN] {len(orphans)} skills in repo but not in Hermes (keeping as archive)")
        for name in orphans[:10]:
            print(f"           {name}")
        if len(orphans) > 10:
            print(f"           ... and {len(orphans) - 10} more")

print("")
print("=== Summary ===")
print(f"  Copied/updated: {copied}")
print(f"  Skipped (unchanged): {skipped}")
print(f"  Archive orphans: {len(orphans)}")
print(f"  Errors: 0")

if DRY_RUN and copied > 0:
    print("")
    print(f"Dry-run — {copied} changes pending. Run with --apply to apply.")
    sys.exit(0)

# Commit and push
if not DRY_RUN and (copied > 0 or FORCE_PUSH):
    os.chdir(REPO_DIR)
    
    # Check if there are actual changes
    result = subprocess.run(["git", "diff", "--quiet"], capture_output=True)
    result2 = subprocess.run(["git", "diff", "--cached", "--quiet"], capture_output=True)
    status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    
    if result.returncode == 0 and result2.returncode == 0 and not status.stdout.strip():
        print("\n  No changes to commit.")
    else:
        timestamp = subprocess.check_output(["date", "+%Y-%m-%d %H:%M:%S"], text=True).strip()
        subprocess.run(["git", "add", "-A"], check=True)
        msg = f"Sync skills from Hermes Agent — {timestamp}\n\n{copied} skills synced ({skipped} unchanged, 0 errors)"
        subprocess.run(["git", "commit", "-m", msg], check=True)
        
        if FORCE_PUSH:
            print("\n  Pushing to origin/main...")
            subprocess.run(["git", "push", "origin", "main"], check=True)
        else:
            print("\n  Changes committed. Push when ready: git push origin main")

print("")
print("=== Done ===")
