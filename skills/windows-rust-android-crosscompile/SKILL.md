---
name: windows-rust-android-crosscompile
description: Cross-compile Rust for Android on Windows.
---

# Windows Rust Android cross-compilation

## Always-on rules

- All Rust builds, Cargo output, and toolchains live on the X: drive.
- C: stays at 90% full / unused.
- Verify the build artifact, not just the compile status.
- Commit before pushing — a `git push` with no commits fails with
  `src refspec main does not match any`.

## Order of operations

1. Build the Rust core for the **host** (Windows) first with `cargo build --release --lib`.
2. For Android, configure `.cargo/config.toml` with the NDK linker and archiver
   pointing at the `.exe` files directly (see 2.1).
3. Build for Android with `cargo build --release --target aarch64-linux-android`.
4. Verify the Android artifact exists: `target/aarch64-linux-android/release/libprism_core.so`.

## 1. Cargo manifest path trap

`cargo build --manifest-path core/Cargo.toml` from the project root fails with
`could not find Cargo.toml` because no `Cargo.toml` exists at the project root.

Fix: build from the project directory without an explicit `--manifest-path`
(or use the native Windows path `X:/Projects/OpticalTransfer/core/Cargo.toml`).
The MSYS shell mangles `/x/...` paths into `X:\x\...`, so Cargo cannot resolve them.

## 2. Android NDK cross-compilation on Windows

### 2.1 The NDK `clang` is a shell script, not an executable

Symptom: `cargo build --target aarch64-linux-android` fails with
`linker "<...>/aarch64-linux-android21-clang" not found`.

Cause: the NDK's `toolchains/llvm/prebuilt/windows-x86_64/bin/` directory
contains a **bash shell script** named `aarch64-linux-android21-clang`.

Fix: point `linker` in `.cargo/config.toml` at the `.exe` file directly:

```toml
[target.aarch64-linux-android]
linker = "X:/Dev/android-ndk/27.3.13750724/toolchains/llvm/prebuilt/windows-x86_64/bin/clang.exe"
ar = "X:/Dev/android-ndk/27.3.13750724/toolchains/llvm/prebuilt/windows-x86_64/bin/llvm-ar.exe"
```

### 2.2 The target spec passes `--eh-frame-hdr=llvm`, which the NDK's clang rejects

Symptom: after fixing 2.1, the link step fails with
`clang: error: unknown argument: '--eh-frame-hdr=llvm'`.

Cause: the `aarch64-linux-android` target spec appends
`--eh-frame-hdr=llvm` to the linker command.

Fix: use `ld.lld.exe` as the linker:

```toml
[target.aarch64-linux-android]
linker = "X:/Dev/android-ndk/27.3.13750724/toolchains/llvm/prebuilt/windows-x86_64/bin/ld.lld.exe"
ar = "X:/Dev/android-ndk/27.3.13750724/toolchains/llvm/prebuilt/windows-x86_64/bin/llvm-ar.exe"
```

### 2.3 Verify the build artifact

A clean build produces `target/aarch64-linux-android/release/libprism_core.so`.
The host-equivalent (`target/release/libprism_core.dll`) compiles cleanly.

## 4. Build verification checklist

A clean host build produces `target/release/libprism_core.dll`.
An Android build produces `target/aarch64-linux-android/release/libprism_core.so`.

When renaming user-facing artifacts or repos (e.g., `prism` → `photon-transfer-protocol`),
update user-facing names in `README.md`, `settings.gradle.kts`, `Cargo.toml`, `.github/workflows/`,
and `local.properties` — but keep internal package namespaces (`com.prism.ot`, `prism_core`)
unchanged to avoid changing Kotlin imports and JNI references.

**Before pushing, always commit.** If you try to push after `git init` with no
commits, you will get `src refspec main does not match any` — the branch has no
commits yet.

## 4. Git hygiene for Android/Rust repos

- Exclude `android/app/key.properties` (contains keystore details) and `keystore.jks`
  in `.gitignore`. These are not committed.
- `.gitignore` must cover Rust `target/` and Android `build/` directories.
- Use `.gitattributes` with `text=auto eol=lf` for consistent line endings on Windows.
