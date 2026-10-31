---
version: 1.0.0
author: Nous Research
license: MIT
metadata:
  hermes:
    tags: [verification]
    related_skills: [agentic-rpc-framework]
---

## F1 verification gate

Run in order; stop on the first failure:

```bash
cargo build --workspace --all-targets   # exit 0
cargo fmt --all -- --check               # FMT_OK
cargo clippy --workspace --all-targets -- -D warnings   # 0 errors
cargo test --workspace                   # all crates green
```

Every crate must pass before a binding or feature is considered done. Per-crate verification (`cargo build -p X`, `cargo test -p X`) is only for fast iteration — the final claim of "done" requires the workspace gate.

### Per-crate iteration

```bash
cargo build -p rpc-cli   # fast red-green on CLI edits
cargo test -p rpc-cli
```

### Salsa feature gate

When a crate gates a real engine behind a Cargo feature, verify BOTH configurations:

```bash
cargo build -p rpc-core --features salsa   # feature build
cargo build -p rpc-core                    # baseline build
```

### Doc-test gate

`rpc-core` and `rpc-daemon` doc comments are compiled as tests; `rpc-api` ships a doctest. If a doctest fails to compile, it is a lint-level failure (the `-D warnings` gate catches it) and the docs must be fixed, not skipped.
