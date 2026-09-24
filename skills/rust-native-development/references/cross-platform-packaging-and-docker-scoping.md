# Cross-Platform Packaging and Docker Scoping

Session learnings from building and packaging a Tauri 2 desktop app and validating its Docker server stack.

## Tauri Packaging on Windows

- `cargo tauri` may not exist even when Tauri builds succeed.
- Fix: install `@tauri-apps/cli` globally with npm and run `tauri build` directly.
- Verify with `tauri --version`.

## Frontend Build Gate

- `tauri build` runs `beforeBuildCommand` first.
- If `npm run build` fails TypeScript/Vite checks, no native binary is produced even when `cargo check` passes.
- Fix frontend build issues first.

## GitHub Actions Packaging Workflow

Use a matrix workflow for release artifacts:

```yaml
name: Desktop Packages
on:
  push:
    tags:
      - 'v*'
  workflow_dispatch:

jobs:
  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
        with:
          targets: x86_64-pc-windows-msvc
      - uses: taiki-e/install-action@v2
        with:
          tool: cargo-tauri
      - run: npm ci --prefix app
      - run: cargo tauri build --package cubeworld-app
        working-directory: app/src-tauri
      - uses: actions/upload-artifact@v4
        with:
          name: cubeworld-windows
          path: |
            target/release/cubeworld-app.exe
            target/release/*.pdb

  build-macos:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
      - uses: taiki-e/install-action@v2
        with:
          tool: cargo-tauri
      - run: npm ci --prefix app
      - run: cargo tauri build --package cubeworld-app
        working-directory: app/src-tauri
      - uses: actions/upload-artifact@v4
        with:
          name: cubeworld-macos
          path: |
            target/release/bundle/**/*

  build-linux:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
      - uses: taiki-e/install-action@v2
        with:
          tool: cargo-tauri
      - run: npm ci --prefix app
      - run: cargo tauri build --package cubeworld-app
        working-directory: app/src-tauri
      - uses: actions/upload-artifact@v4
        with:
          name: cubeworld-linux
          path: |
            target/release/bundle/**/*
```

## Docker Workspace Scoping

- When a Dockerfile builds one workspace package, Cargo resolves the entire workspace from `Cargo.toml`.
- The Docker build context must include every workspace member path listed in the root manifest.
- Missing members cause build failures like:
  - `error: failed to load manifest for workspace member /app/app/src-tauri`
  - `error: failed to load manifest for workspace member /app/crates/plugin`

Fix options:
1. Remove excluded members from `Cargo.toml` before Docker builds.
2. Add required member paths to the Docker build context and `COPY` them.
3. If `cargo build` fails with `edition2024` errors from transitive crates, bump the Rust base image to `rust:latest` or pin problematic transitive versions in `Cargo.lock`.

## Verified Build Artifacts

- Windows native desktop binary: `target/release/cubeworld-app.exe`
- Cross-platform GitHub Actions workflow: `.github/workflows/desktop-packages.yml`