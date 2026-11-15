---
name: rust-workspace-audit-fixing
description: Audit, fix, and verify Rust workspaces to zero errors.
category: software-development
version: 1.0.0
author: Hermes Agent
license: MIT
tags: [rust, audit, clippy, verification]
related_skills: []
---

# Rust Workspace Audit & Fix

Audit, fix warnings, and remediate bugs in a Rust workspace to a clean verification gate.

## When to Use

Use this skill when an audit has been requested for a Rust workspace, when the user says "fix all warnings", or when a workspace is not building cleanly or passing tests. This is the standard workflow for code repair and verification in Rust projects.

## Verification gates (run in order)

These four commands define a clean build. All must pass before claiming completion:

1. **cargo check** — `cargo check --workspace` (0 errors)
2. **cargo fmt** — `cargo fmt --all --check` (0 diffs)
3. **cargo clippy** — `cargo clippy --workspace --all-targets` (0 errors, 0 warnings)
4. **cargo test** — `cargo test --workspace` (0 failures)

Run them after every edit batch so you catch regressions early.

## Procedure

### 1. Baseline
```

### 1. Baseline
```
export CARGO_HOME=/x/Dev/cargo
export CARGO_TARGET_DIR=/x/cargo-target
cargo check --workspace 2>&1 | tail -5
cargo fmt --all --check 2>&1 | head -20
cargo clippy --workspace --all-targets 2>&1 | grep -E "^error" | head -20
cargo test --workspace 2>&1 | grep -E "test result" | tail -5
```

Record: errors count, warning count, test results.

### 2. Fix CRITICAL errors first
- E0433, E0559, E0124 (duplicate fields), E0599 (method not found), E0425 (value not found)
- These block the build — fix before touching warnings

### 3. Fix warnings in dependency order
- Dead code / unused fields → remove or add `#[allow(dead_code)]`
- `unused_mut`, `unused_variables`, `unused_imports` → clean up
- `too_many_arguments` → refactor or `#[allow(clippy::too_many_arguments)]`
- `if_same_then_else` → collapse or `#[allow(clippy::if_same_then_else)]`
- `new_without_default` → add `impl Default`

### 4. Verify after each batch
Re-run the four gates. If errors return, stop and diagnose.

## Pitfalls

- **Patching corrupted files is dangerous.** A file that already has broken structure (duplicate code, mismatched braces) will break further when you patch it. When a `patch` reveals structural damage (wrong indentation, duplicate blocks, mismatched delimiters), STOP and rewrite the file from a clean source rather than patching it.
- **Do not hand-roll test mocks or reimplement existing shapes.** If a helper signature changed, grep the test tree for the SYMBOL first. Hand-rolled mocks reimplement the old shape and fail on sharding you did not run.
- **write_file refuses overwrites after a partial read.** If a file was loaded with `read_file` using offset/limit pagination, `write_file` is blocked with a 'stale_write_blocked' error. Fix with `patch` for small edits, or read the full file first (large limit), then `write_file`.
- **Scripts can break builds.** If a Python/PowerShell fix script modifies source files, verify the build afterwards. The script may have removed fields that were still being constructed by other code.
- **cargo clippy --fix does not work on files with broken structure.** Run it only after `cargo check` passes.
- **Cargo.lock is large and must not be edited by hand.** If dependencies change, `cargo update` regenerates it.

## Build environment

```
export CARGO_HOME=/x/Dev/cargo
export CARGO_TARGET_DIR=/x/cargo-target
```

Set in both `~/.bashrc` and Windows user env. Use `sudo` for system-level commands.