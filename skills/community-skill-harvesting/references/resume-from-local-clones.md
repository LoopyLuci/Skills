# Resuming Skill Imports from Local Clones

When a bulk community-skill import is interrupted (network blip, timeout,
process kill), **resume from local clones rather than re-fetching from GitHub
raw**. The staging directory acts as a checkpoint.

## Why local clones

`import-community-skills.py` fetches each `SKILL.md` from
`raw.githubusercontent.com/{repo}/main/skills/{path}/SKILL.md`. If interrupted
midway, re-running re-fetches everything from scratch (slow + rate-limit-bound).
A local `git clone` / extracted copy is a durable, offline checkpoint.

## Resume procedure

1. **Locate the staging dir** — typically `D:\Projects\skills-import/` with
   one subdir per repo (e.g. `anthropics-skills`, `mattpocock-skills`).

2. **Iterate all SKILL.md** via `rglob("SKILL.md")`, skipping `.git/` and
   `template/` dirs:
   ```python
   for sk_dir in sorted(src_base.rglob("SKILL.md")):
       if ".git" in sk_dir.parts: continue
       if "template" in sk_dir.parent.name.lower(): continue
       sk_dir = sk_dir.parent  # the skill directory itself
   ```

3. **Skip already-imported targets** (idempotent resume):
   ```python
   target_file = DST_ROOT / skill_name / "SKILL.md"
   if target_file.exists():
       skipped += 1; continue
   ```

4. **Apply `enhance_frontmatter`** — must be idempotent (see Pitfalls).

5. **Copy supporting subdirs** (`references`, `templates`, `scripts`, `assets`,
   `examples`) via `shutil.copytree(..., dirs_exist_ok=True)`.

## Idempotency verification (critical)

Before committing to the import, always round-trip-test the enhancer:

```python
out1 = enhance_frontmatter(content, name, source_repo)
out2 = enhance_frontmatter(out1, name, source_repo)
assert out1 == out2, f"enhance_frontmatter is not idempotent for {name}"
```

The frontmatter parser must drop the **entire** indented `metadata:` subtree
on each pass — not just lines matching `hermes:`/`tags:`/`category:` by name —
or orphaned nested keys (e.g. `related_skills:`) cause `metadata:` blocks to
accumulate on every re-run.

## Git-Bash path handling (Windows)

When running resume scripts under git-bash, prefer **native Windows paths**
(`D:\Projects\...`) in `pathlib.Path(...)` calls, or use forward-slash
POSIX-style paths. The `pathlib` constructor handles both, but mixing `/d/`
POSIX prefixes inside Python string literals can cause `FileNotFoundError`
because Python's Windows build does not interpret MSYS2-style `/d/` prefixes.

```python
# ✅ Works
SRC = pathlib.Path(r"D:\Projects\skills-import")
# ✅ Also works
SRC = pathlib.Path("D:/Projects/skills-import")
# ❌ Broken on Windows Python
SRC = pathlib.Path("/d/Projects/skills-import")
```

## Script

See `scripts/resume_skill_import.py` — a self-contained resumable harvester
that reads from local clones, applies idempotent frontmatter enhancement,
copies supporting files, and reports a summary. Re-running is safe: it skips
all already-present target files.
