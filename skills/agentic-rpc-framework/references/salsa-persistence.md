---
version: 1.0.0
author: Nous Research
license: MIT
metadata:
  hermes:
    tags: [salsa, persistence, incremental]
    related_skills: [agentic-rpc-framework]
---

## S2 — Salsa persistence (v0.28.5)

`crates.io/salsa` crate, `v0.28.5` (MSRV 1.88.0, edition 2024).
Feature flag: `persistence`.

Persistence API (verified via `tests/persistence.rs` in salsa repo):
- `#[salsa::input(persist)]` / `#[salsa::tracked(persist)]`
- `as_serialize` / `Database::deserialize`
- `Database::deserialize` reads serialized DB; `persist` saves it.

Usage for the framework:
- `SalsaEngine` adapter (`rpc-core/src/salsa_engine/lib.rs`) uses `#[salsa::database]` with `#[salsa::database]` macro.
- `SalsaDatabase::serialize` / `deserialize` handled by the feature.
- `persistence` feature must be enabled in the workspace `Cargo.toml` when compiling with salsa.
