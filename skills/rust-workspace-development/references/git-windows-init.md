# Git Initialization on Windows Non-Interactive Sessions

## Problem

`git commit` from a non-interactive terminal on Windows can stall or return exit 1 when the initial staged diff includes large numbers of build artifact deletions under `target/`.

## Reproduction

```bash
cd C:/Projects/cubeworld
git init
git add -A
git commit -m "initial"
```

If `target/` exists and is untracked, `git add -A` stages all build artifacts. The first commit then tries to record thousands of deleted-object entries and times out.

## Fix Pattern

1. Create `.gitignore` first.
2. Stage selectively: `git add .gitignore Cargo.toml CLAUDE.md crates/ server/ app/src/ app/src-tauri/Cargo.toml ...`
3. If `target/` was staged, remove from index: `git rm --cached -r target`
4. Configure identity: `git config user.email "dev@example.com"` and `git config user.name "Dev"`
5. Commit with concise message.

## Verification

After commit, `git log --oneline -n 1` should return immediately. `git status` should show only intended source changes.
