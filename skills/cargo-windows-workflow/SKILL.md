---
name: cargo-windows-workflow
description: "Use when managing Rust Cargo projects on Windows."
category: software-development
tags: [rust, cargo, windows, build, toolchain]
---
# Cargo Windows Workflow

Managing Rust Cargo projects on Windows.

## Toolchains

```powershell
# Install toolchains
rustup toolchain install stable-x86_64-pc-windows-msvc
rustup toolchain install stable-x86_64-pc-windows-gnu
rustup toolchain install nightly-x86_64-pc-windows-msvc

# Set default
rustup default stable-x86_64-pc-windows-msvc

# Per-project override
rustup override set nightly
```

## Common Commands

```powershell
cargo new myapp --bin
cargo new mylib --lib

cargo build                      # debug build
cargo build --release            # release build
cargo build --target x86_64-pc-windows-gnu

cargo check                      # fast type-check only
cargo clippy                     # lints
cargo fmt                        # formatting

cargo test                       # run tests
cargo test -- --nocapture        # show stdout
cargo test test_name             # run specific test

cargo run                        # build + run
cargo run -- arg1 arg2           # pass args to binary

cargo doc                        # generate docs
cargo doc --open                 # open in browser

cargo update                     # update dependencies
cargo outdated                   # check for outdated deps
```

## Cross-Compilation Config

```toml
# .cargo/config.toml
[target.x86_64-pc-windows-msvc]
linker = "link.exe"
rustflags = ["-C", "target-feature=+crt-static"]  # static CRT

[target.x86_64-pc-windows-gnu]
linker = "x86_64-w64-mingw32-gcc.exe"

[target.x86_64-unknown-linux-gnu]
linker = "x86_64-linux-gnu-gcc.exe"

# Faster linking
[target.x86_64-pc-windows-msvc]
linker = "lld-link.exe"
rustflags = ["-C", "link-arg=/DEBUG:FASTLINK"]
```

## Profile Configuration

```toml
# Cargo.toml
[profile.dev]
opt-level = 0
debug = true

[profile.release]
opt-level = 3
debug = false
lto = true
codegen-units = 1
strip = true
```

## Environment-Specific Builds

```toml
# Cargo.toml
[features]
default = ["std"]
std = []
no-std = []

[dependencies]
winapi = { version = "0.3", features = ["winnt", "handleapi"] }

[target.'cfg(windows)'.dependencies]
winreg = "0.50"

[target.'cfg(unix)'.dependencies]
libc = "0.2"
```

## Benchmarks

```powershell
# Requires nightly
rustup run nightly cargo bench

# Or use criterion (stable)
# [dev-dependencies]
# criterion = "0.5"
```

## Pitfalls

- MSVC toolchain needs Visual Studio Build Tools
- GNU toolchain links against MinGW -- different ABI
- lld-link is faster than link.exe for large projects
- `strip = true` in release profile removes debug symbols (smaller binary)
- `lto = true` increases compile time but improves performance
