---
name: rust-workspace-audit-fixing
description: Audit, fix, and verify Rust workspaces to zero errors.
category: software-development
version: 1.0.0
author: Hermes Agent
license: MIT
tags: [rust, audit, clippy, verification]
related_skills: []
platforms: [any]
metadata:
  hermes:
    tags: [rust, audit, clippy, verification]
---

# Rust Workspace Audit & Fix

Audit, fix warnings, and remediate bugs in a Rust workspace to a clean verification gate.

## When to Use

Use this skill when an audit has been requested for a Rust workspace, when the user says "fix all warnings", or when a workspace is not building cleanly or passing tests. This is the standard workflow for code repair and verification in Rust projects.

Standing preferences when working a Rust workspace:
- Full implementation: complete, working, verified output; never a stub or a partial build.
- Zero tolerance for errors and warnings: a clean gate emits no warnings.
- Discover before editing: read the relevant docs and source files before making changes; trace a symbol to its definition and usages rather than guessing.

## Verification gates (run in order)

These four commands define a clean build. All must pass before claiming completion:

1. **cargo check** — `cargo check --workspace` (0 errors)
2. **cargo fmt** — `cargo fmt --all --check` (0 diffs)
3. **cargo clippy** — `cargo clippy --workspace --all-targets` (0 errors, 0 warnings)
4. **cargo test** — `cargo test --workspace` (0 failures)

Run them after every edit batch so you catch regressions early. On first `cargo test --workspace`, third-party dependency crates can panic or stack-overflow under the active toolchain (rustc version skew) — that fails the gate even though the project's own crates are fine. When the workspace test gate fails this way, scope it to the project's own crates and diagnose the dependency separately, below. Record: errors count, warning count, and test results per project crate, not just the aggregate.

## Procedure

### 1. Discovery before editing
Read every relevant doc the user asked you to read (docs/*.md, spec/, packages/, the crate READMEs) and the crate source files. Understand the project structure, the crate layout, and the existing patterns before writing any code. Trace a symbol to its definition and usages rather than guessing. Only after the whole picture is established do you edit.

### 1. Baseline
```bash
export CARGO_HOME=/x/Dev/cargo
export CARGO_TARGET_DIR=/x/cargo-target
cargo check --workspace 2>&1 | tail -5
cargo fmt --all --check 2>&1 | head -20
cargo clippy --workspace --all-targets 2>&1 | grep -E "^error" | head -20
cargo test -p nlpcli-core -p nlpcli-service -p nlp-cli 2>&1 | grep -E "test result" | tail -5
```

Record: errors count, warning count, and test results per project crate, not just the aggregate.

- Run `cargo check --workspace` (or `--all-targets`) first; it is the only gate that reliably crosses third-party crates.
- Run `cargo test -p <project crates>` to isolate the project's own tests; the `--workspace` test gate can panic on third-party crates under the active toolchain.

### 2. Fix CRITICAL errors first
- E0433, E0559, E0124 (duplicate fields), E0599 (method not found), E0425 (value not found)
- These block the build — fix before touching warnings

### 3. Fix warnings in dependency order
- `manual_range_contains` → use `range.contains(&x)` instead of chained comparisons, e.g. `!(200..=299).contains(&status)`
- `cloned_ref_to_slice_refs` → use `std::slice::from_ref(&x)` instead of `&[x.clone()]`
- Dead code / unused fields → remove or add `#[allow(dead_code)]`
- `unused_mut`, `unused_variables`, `unused_imports` → clean up
- `too_many_arguments` → refactor or `#[allow(clippy::too_many_arguments)]`
- `if_same_then_else` → collapse or `#[allow(clippy::if_same_then_else)]`
- `new_without_default` → add `impl Default`

### 4. Verify after each batch
Re-run the four gates. If errors return, stop and diagnose.

### 5. CLI feature exposure (when commands surface settings to a terminal)
When a CLI must expose every feature and setting from a terminal:
1. Read the settings schema (settings_schema in the service crate) to enumerate every setting and its category.
2. Write one command function per subcommand (show, set, import, export), each taking (args: &[String], project: &Path).
3. Add split_project to parse an optional --project DIR before dispatch.
4. Wire each command into the dispatch table with the subcommand name as the key; add a dispatch entry for the command family itself.
5. Update usage() so every command appears in the printed help.
6. Add tests: one per command, plus a regression test that the schema lists every setting.
7. Verify the whole family before behavioural tests: `cargo clippy --all-targets -- -D warnings` (0 errors, 0 warnings) and `cargo check -p nlpcli-cli`; then run the behavioural tests. Record per-crate test counts (core 106, service 39, cli 10 in this project) — aggregate only.

## Pitfalls

- **Patching corrupted files is dangerous.** A file that already has broken structure (duplicate code, mismatched braces) will break further when you patch it. When a `patch` reveals structural damage (wrong indentation, duplicate blocks, mismatched delimiters), STOP and rewrite the file from a clean source rather than patching it.
- **Do not hand-roll test mocks or reimplement existing shapes.** If a helper signature changed, grep the test tree for the SYMBOL first. Hand-rolled mocks reimplement the old shape and fail on sharding you did not run.
- **write_file refuses overwrites after a partial read.** If a file was loaded with `read_file` using offset/limit pagination, `write_file` is blocked with a 'stale_write_blocked' error. Fix with `patch` for small edits, or read the full file first (large limit), then `write_file`.
- **Scripts can break builds.** If a Python/PowerShell fix script modifies source files, verify the build afterwards. The script may have removed fields that were still being constructed by other code.
- **cargo clippy --fix does not work on files with broken structure.** Run it only after `cargo check` passes.
- **Cargo.lock is large and must not be edited by hand.** If dependencies change, `cargo update` regenerates it.
Scope the test gate to project crates. `cargo test --workspace` can fail on third-party crates (rustc version skew) even when the project's own crates are fine; use `cargo test -p <project crates>` while diagnosing the dependency separately.

- **Verify the binary where CARGO_TARGET_DIR points.** The repository's target/ may hold stale hard links to older builds; the fresh build is at CARGO_TARGET_DIR/debug/<bin-name>. Check the binary's mtime before trusting a smoke test.

## Diagnosing third-party crates by reading their real source

When a compiler error points at a third-party crate and does not match the crate's published docs (method missing, wrong signature, wrong trait bound), do not patch from memory — the published docs are often stale relative to the exact version in the registry.

1. Locate the crate in the cargo registry cache: `CARGO_HOME`/`registry`/`src`/`index.crates.io-...`/`<crate>-<version>/`.
2. Read the module the error mentions (e.g. `src/response.rs` for ureq's `Response`).
3. Read the real signatures of the methods named in the error and the trait bounds they carry.
4. Patch against those signatures.

Example — ureq 2's `Response`: the errors `no method named is_success`, `no method named read_string`, and `Vec<u8>` does not implement `Read` for `send` came from `.is_success()`, `.read_string()`, and `.send(&body)` on an `impl Read` value. The real API is `status()` (u16), `into_string()`, and `send(self, reader: impl Read)`. `Vec<u8>` satisfies `Read`, so `.send(body)` works; `std::io::Cursor<Vec<u8>>` always satisfies `Read`. The source is at `X:/Dev/cargo/registry/src/index.crates.io-1949cf8c6b5b557f/ureq-2.12.1/src/`.

Record the real API so a later error on the same crate does not loop through four guesses. After a dependency fix, re-run `cargo check --workspace` and `cargo clippy`; only re-run the full test gate once `cargo check` is clean.

## Build environment

```bash
export CARGO_HOME=/x/Dev/cargo
export CARGO_TARGET_DIR=/x/cargo-target
```

Set in both `~/.bashrc` and Windows user env. Use `sudo` for system-level commands.