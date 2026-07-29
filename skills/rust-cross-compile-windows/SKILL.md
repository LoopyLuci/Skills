---
name: rust-cross-compile-windows
description: "Use when cross-compiling Rust for or from Windows."
category: software-development
tags: [rust, cross-compile, windows, msvc, gnu]
---
# Rust Cross-Compile on Windows

Cross-compiling Rust applications for and from Windows.

## Rust Targets for Windows

```powershell
# List installed targets
rustup target list --installed

# Common Windows targets:
# x86_64-pc-windows-msvc    (MSVC CRT, most common)
# x86_64-pc-windows-gnu     (MinGW/GCC, no VC++ redist needed)
# i686-pc-windows-msvc      (32-bit MSVC)
# aarch64-pc-windows-msvc   (ARM64 Windows)
# x86_64-unknown-linux-gnu  (Linux target from Windows)
```

## Add Targets

```powershell
rustup target add x86_64-pc-windows-msvc
rustup target add x86_64-pc-windows-gnu
rustup target add x86_64-unknown-linux-gnu
```

## Building

```powershell
# Build for MSVC (default)
cargo build --release

# Build for GNU/MinGW
cargo build --release --target x86_64-pc-windows-gnu

# Build for Linux from Windows
cargo build --release --target x86_64-unknown-linux-gnu
```

## Cross-Compile Config (.cargo/config.toml)

```toml
[target.x86_64-pc-windows-msvc]
linker = "link.exe"  # MSVC linker

[target.x86_64-pc-windows-gnu]
linker = "x86_64-w64-mingw32-gcc.exe"

[target.x86_64-unknown-linux-gnu]
linker = "x86_64-linux-gnu-gcc.exe"
```

## Using LLVM/Clang Linker

```toml
# .cargo/config.toml
[target.x86_64-pc-windows-msvc]
linker = "lld-link.exe"
rustflags = ["-C", "link-arg=-pdbaltpath:%_PDB%"]
```

## Environment Variables

```powershell
# MSVC
$env:CC = "cl.exe"
$env:CXX = "cl.exe"

# MinGW
$env:CC = "gcc.exe"
$env:CXX = "g++.exe"

# Clang for Windows
$env:CC = "clang-cl.exe"
$env:CXX = "clang-cl.exe"
```

## Cross-Compile C Dependencies

```powershell
# For crates with C bindings (openssl, vulkan, etc.)
# Set PKG_CONFIG_ALLOW_CROSS=1
# Set CC_<target> for the C compiler per target

# Example: Linux target from Windows
$env:CC_x86_64_unknown_linux_gnu = "x86_64-linux-gnu-gcc.exe"
```

## Pitfalls

- **MSVC target** requires Visual Studio Build Tools -- run from "x64 Native Tools Command Prompt"
- **GNU target** can conflict with MSVC CRT -- mix only with caution
- **OpenSSL** on Windows needs `openssl` crate with `vendored` feature
- **C dependencies** need matching cross-compilation toolchains
- **cargo build** without --target uses host target; with --target uses cross toolchain
