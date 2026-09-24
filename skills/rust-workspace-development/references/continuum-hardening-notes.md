# Continuum Hardening Notes

## Auth Hardening
- Add `--require-pake` only when the local pair flow supports it; do not block all non-PAKE peers by default in existing networks.
- Validate resume tokens with a TTL and evict expired entries from `resume_tokens` on a background timer, not only on access.
- Check pairing state at stream accept time (`Media`, `Audio`, `Clipboard`, `FileTransfer`) before processing payloads.

## Cross-Platform Feature Gating
- Add optional platform deps under `[features]`:
  - `platform-macos = ["scrap", "core-graphics"]`
  - `platform-linux = ["scrap", "libxdo"]`
- Keep platform-specific Rust code behind `#[cfg(any(target_os = "macos", target_os = "linux"))]` so Windows hosts still pass workspace checks.
- Validate on the Windows host with `cargo check --workspace`; test on the target platform later.

## Relay Server Expansion
- Reuse existing state initialization rather than introducing a second listener.
- Handle `register`, `connect`, and `relay_ready` message types with real state transitions; never leave transport dispatch as `Ok(())`.

## Audio / Clipboard / File Transfer Streams
- Use a 4-byte length-prefixed JSON envelope for stream messages.
- Enforce max message size early; break on read errors instead of logging and continuing.
- For `FileTransfer`, normalize upload destinations under a dedicated temp directory and do not trust client-supplied paths blindly.

## Client State Wiring
- When adding new UI state fields, update the struct and `new()` initializer together to avoid compile misses.
- Convert unused catchall `_ => {}` arms into explicit variants when the worker can emit new events.

## Test Verification Strategy
- Run `cargo test --workspace --quiet`.
- For environment-specific doctest failures unrelated to runtime logic, run unit coverage with `cargo test --workspace --quiet -- --skip <crate>` instead of disabling tests globally.
