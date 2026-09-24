# Continuum Feature-Gating Pitfalls

This document captures cfg-gating mistakes encountered during Continuum stabilization.

## Pitfall 1: Gating a module but not its re-export

**Symptom**: `E0433: cannot find 'audio' in 'crate'` when tests reference `continuum_transport::audio::AudioCapturer`.

**Cause**: `lib.rs` had `#[cfg(feature = "audio")] pub mod audio;` but tests used the module path unconditionally.

**Fix**: Add `#[cfg(feature = "audio")]` to every test that references audio types, OR add the feature to the test crate's `Cargo.toml`. In Continuum, we gated the tests:

```rust
#[cfg(feature = "audio")]
#[test]
fn test_audio_capturer_frame_size() {
    let capturer = continuum_transport::audio::AudioCapturer::new(48000, 2);
    // ...
}
```

## Pitfall 2: Gating a match arm but not its handler

**Symptom**: `E0425: cannot find function 'handle_audio_stream' in this scope`.

**Cause**: The match arm `#[cfg(feature = "audio")] ApqStreamType::Audio => handle_audio_stream(...)` was gated, but the handler function was ungated (or vice versa).

**Fix**: Use paired gating — gate both the arm and the function, OR use a fallback arm:

```rust
#[cfg(feature = "audio")]
ApqStreamType::Audio => handle_audio_stream(&mut send, state, addr).await,
#[cfg(not(feature = "audio"))]
ApqStreamType::Audio => Ok(()),
```

## Pitfall 3: Catch-all arm placement

**Symptom**: `unreachable_pattern` warnings.

**Cause**: A `_ => {}` catch-all placed BEFORE specific match arms.

**Fix**: Always place catch-all arms LAST:

```rust
match event {
    ConnectionEvent::Frame { .. } => { ... }
    ConnectionEvent::Status(_) => { ... }
    _ => {},  // catch-all must be last
};
```

## Pitfall 4: System-library dependencies in CI

**Symptom**: CI fails with `pkg-config exited with status code 1 — Package alsa was not found` when building `cpal` on Linux runners.

**Fix**: Make audio dependencies optional:

```toml
# Cargo.toml
cpal = { version = "0.15", optional = true }

[features]
audio = ["cpal"]
```

Then gate the entire audio module with `#![cfg(feature = "audio")]` at the top of `audio.rs`.

## Pitfall 5: Cross-crate event variant gating

**Symptom**: `E0599: no variant named 'Audio' found for enum 'ConnectionEvent'` in downstream crates (`continuum`, `continuum-client`).

**Cause**: `ConnectionEvent::Audio` variant was gated with `#[cfg(feature = "audio")]` in `client.rs`, but match arms in other crates referenced it unconditionally.

**Fix**: Either remove the catch-all from the match (if the variant is conditionally present), or add the same cfg gate to downstream match arms:

```rust
// In app.rs / connection.rs — replace the specific arm with a catch-all
// (since the variant may not exist)
_ => continue,
```

## Pitfall 6: Test file not declared in main.rs

**Symptom**: New test file (e.g., `relay_integration_tests.rs`) compiled but tests not discovered.

**Cause**: Binary crates require explicit module declaration.

**Fix**: Add to `main.rs`:

```rust
mod relay_integration_tests;
mod resilience_tests;
```

## Pitfall 7: The `#[cfg(feature = "...")]` Import Trap

**Symptom**: After adding `#[cfg(feature = "observability")]` to imports in `server.rs`, the build fails with `E0425` / `E0433` "cannot find type `MetricsRegistry` / `AuditEvent` / `HealthServer` in this scope".

**Root cause**: The imports were gated behind a feature flag, but the usage sites throughout the file were unconditional. Rust resolves imports at the crate level — if an import is cfg'd out, the names are simply not available, even if the code that uses them is compiled.

**Fix**: Either:
1. Remove the cfg gate from the import (if the dependency is effectively required), OR
2. Gate EVERY usage site with the same cfg attribute

**Lesson**: Before gating an import, grep for all usage sites. If any are unconditional, the import must be unconditional too.

**Real case from session**: In `continuum-transport/src/server.rs`, the `continuum_observability` dependency is effectively required (audit logging, metrics, health checks). Attempting to gate it behind an optional `observability` feature failed because usage sites were unconditional. The fix was to keep the imports unconditional.

## Verification

After feature-gating changes, verify with:

```bash
cargo check --workspace                    # default features
cargo check --workspace --features audio   # with audio
cargo check --workspace --no-default-features  # minimal
```
