---
name: local-cicd-pipeline
description: "Build local CI/CD pipelines with preflight, tests, deploy."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [ci-cd, pipeline, automation, devops]
    related_skills: [github-pr-workflow, verified-release-artifacts]
---

# Local On-Device CI/CD Pipeline

## When to Use

Use this skill when building, maintaining, or troubleshooting a local on-device CI/CD pipeline. This includes:
- Setting up preflight checks, static analysis, test automation, smoke tests, build, and deploy stages
- Configuring git hooks (pre-commit, pre-push) for automated pipeline execution
- Troubleshooting pipeline failures (stale reports, historical diff ranges, Gradle error parsing)
- Adding file watchers or scheduler triggers for continuous automation

## Overview

A fully custom, self-contained CI/CD pipeline that runs entirely on the local machine with no cloud runners. It provides preflight checks, static analysis, parallel tests, smoke tests, build automation, and deployment — all orchestrated through a single Python script with git hooks, file watchers, and scheduler triggers.

## Pipeline Stages (in order)

1. **preflight** — Python version, venv, dependencies (pip check), git state, disk space, optional tools (QEMU, JDK)
2. **static** — compileall, ruff (E9,F63,F7,F82,B006,B008), bare except detection, secret pattern scanning, big file detection
3. **tests** — pytest with xdist parallel, flaky rerun, JUnit XML output, timeout
4. **smoke** — real hub in throwaway VMH_HOME, health/catalog/MCP over HTTP+stdio, clean shutdown
5. **android** — gradlew testDebugUnitTest assembleDebug (when android/ changed + JDK present)
6. **build** — PyInstaller executable
7. **deploy** — restart running hub from this checkout

## Always-On Rules

- **Comprehensive scope**: The user expects exhaustive implementation, never minimal. All stages, all checks, all features.
- **Working artifacts**: Every pipeline run must produce real reports (JSON + history.jsonl + logs). No placeholders.
- **Change-aware**: Use git diff to skip unneeded stages. Only run what changed.
- **Lock mechanism**: One pipeline at a time via a lock file naming the running PID.
- **Timeout everything**: Every command has a timeout; on timeout kill the whole process tree.
- **Flaky rerun**: Failed tests are re-run once on their own to distinguish flakes from real failures.

## Critical Pitfalls

### Big-file/secret checks: scan working tree, NOT historical range
When checking for big files or secrets, examine only the working tree (uncommitted + untracked + staged files) against HEAD. Do NOT scan the full historical diff range — old commits may have tracked build artifacts (e.g., `target/`) that were later removed, causing false failures.

### Gradle error parsing: use FAILURE:/What went wrong: blocks
When a Gradle build fails, parse for `FAILURE:` and `What went wrong:` blocks in the output. Do NOT use `tail(out)` — it grabs version numbers (e.g., `25.0.2`) instead of the real error message.

### Staticmethod self reference
A `@staticmethod` that references class attributes must use the class name directly (e.g., `ClassName._ATTR`), not `self._ATTR`.

### Exception variable lambda capture
Python 3 deletes the exception variable after the except block ends. If the exception is captured in a lambda (e.g., `QTimer.singleShot(0, lambda: ...)`), use a default argument: `lambda exc=exc: ...`.

### Bare except
Never use bare `except:` — it catches KeyboardInterrupt and SystemExit. Always use `except Exception:`.

### Build artifacts in git
Add `target/`, `dist/`, `build/` to `.gitignore`. If already tracked, remove with `git rm -r --cached target/`.

## CLI Usage

```bash
python -m ci --full          # Run all stages
python -m ci --fast          # Preflight, static, tests only
python -m ci --only tests    # Run specific stage(s)
python -m ci --list           # Show what would run and why
python -m ci --no-deploy     # Skip deploy stage
python -m ci --build         # Also build executable
```

## Git Hooks

- **pre-push**: Runs full pipeline before every push
- **pre-commit**: Runs static checks before every commit

Install with: `python ci/install_hooks.py`

## Triggers

- **File watcher**: Watches src/, tests/, crates/, scripts/, gui/ for changes
- **Scheduler**: Runs pipeline on a schedule (e.g., every 60 minutes)
- **Git hooks**: Pre-commit and pre-push hooks

## References

- `references/pipeline-stages.md` — Detailed stage implementations and configuration
- `references/troubleshooting.md` — Common failures and fixes