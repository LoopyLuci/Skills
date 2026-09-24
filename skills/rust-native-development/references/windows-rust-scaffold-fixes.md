# Windows Rust Scaffold Fixes

Session-specific fixes discovered while building the CubeWorld genetics workspace on Windows with VS Build Tools 2022 + Git Bash.

## Crate API Gotchas

### ed25519-dalek 2.x
- `SigningKey::generate` was removed.
- Construct via `SigningKey::from_bytes(&seed.into())` after filling a `[u8; 32]` with `rand::thread_rng().fill(&mut seed)`.
- Import `Signer` trait to use `.sign(payload)`.

### rand 0.8 + Normal distribution
- `Normal` is not in `rand::distributions`; it lives in `rand_distr`.
- Add `rand-distr = "0.4"` to Cargo.toml.
- Import `rand_distr::{Distribution, Normal}`.

### HashMap nondeterminism
- `std::collections::HashMap` iteration order is not stable across processes.
- For deterministic genome hashing, use `indexmap::IndexMap` with `features = ["serde"]`.
- Without this, identical genomes can produce different hashes on different runs.

### Custom key types with serde
- When using `IndexMap<LocusId, Chromosome>`, implement `From<&str>` and `From<String>` for `LocusId`.
- Otherwise deserialization fails: "trait bound `LocusId: From<&str>` is not satisfied".

### rand_distr import pattern
- Use `use rand_distr::{Distribution, Normal};` at function scope or module scope.
- The import `use rand::distributions::Normal` does not work in rand 0.8.

## Workspace Configuration

### [workspace.dependencies] is required
- When member crates use `.workspace = true`, the root Cargo.toml must define `[workspace.dependencies]`.
- Missing this causes: "error inheriting from workspace root manifest's `workspace.dependencies`".

### Tauri 2 config field names
- `devPath` → `devUrl`
- `distDir` → `frontendDist`
- `package` is not a top-level key; move `productName` and `version` under `tauri`.

## Axum 0.7 Handlers
- Route handlers must satisfy the `Handler` trait exactly.
- Mismatched parameter counts produce opaque `top_level_handler_fn!` macro errors.
- Ensure signatures match `(State<S>, ...) -> ...`.

## Test Determinism
- UUIDs must be fixed in tests: use `Uuid::from_bytes([1u8; 16])` instead of `Uuid::new_v4()`.
- Otherwise genome hashes differ between test runs even with the same seed.
