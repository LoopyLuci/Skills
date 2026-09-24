# Continuum Architecture Patterns

This document captures architectural patterns discovered during Continuum's 100-year durability redesign.

## Core Trait Abstractions

The foundation for evolvability: every component behind a swappable interface.

```rust
// continuum-core/src/video.rs
pub trait VideoEncoder: Send + Sync {
    fn encode(&mut self, frame: &VideoFrame, is_keyframe: bool, quality: u8) 
        -> ContinuumResult<EncodedFrame>;
    fn notify_network(&mut self, rtt_ms: f32, packet_loss: f32);
    fn bitrate_estimate_kbps(&self) -> u32;
    fn request_keyframe(&mut self);
    fn reset(&mut self);
}

// continuum-core/src/transport.rs
pub trait Transport: Send + Sync {
    fn connect(&mut self, addr: &str) 
        -> ContinuumResult<Box<dyn TransportConnection>>;
    fn accept(&mut self) -> ContinuumResult<Box<dyn TransportConnection>>;
    fn close(&mut self);
}

// continuum-core/src/crypto.rs
pub trait CryptoProvider: Send + Sync {
    fn init_with_secret(&mut self, secret: &[u8]);
    fn is_active(&self) -> bool;
    fn encrypt(&mut self, plaintext: &[u8]) -> ContinuumResult<Vec<u8>>;
    fn decrypt(&mut self, ciphertext: &[u8]) -> ContinuumResult<Vec<u8>>;
    fn algorithm_id(&self) -> u16;
    fn algorithm_name(&self) -> &str;
}
```

## Feature-Gating Cross-Crate Variants

When gating an enum variant behind a feature flag, ALL crates that match on that enum must handle the missing variant.

**Pattern:**

```rust
// In client.rs (continuum-transport)
#[cfg(feature = "audio")]
Audio(crate::audio::AudioFrame),

// In app.rs (continuum) and connection.rs (continuum-client)
// WRONG: continuum_transport::client::ConnectionEvent::Audio(_) => continue,
// RIGHT: Replace with catch-all (since variant may not exist)
_ => continue,
```

## Module-Level Gating

For entire modules that depend on system libraries:

```rust
// At top of audio.rs
#![cfg(feature = "audio")]

// In lib.rs
#[cfg(feature = "audio")]
pub mod audio;

// In Cargo.toml
cpal = { version = "0.15", optional = true }

[features]
audio = ["cpal"]
```

## Verification Checklist

After feature-gating changes:

```bash
cargo check --workspace                        # default features
cargo check --workspace --features audio       # with audio
cargo check --workspace --no-default-features  # minimal
```

## The Completion Loop Trap

**User preference (critical):** After completing a major phase, STOP. Report verified state concisely. Wait for explicit direction before starting the next phase.

Do NOT generate multi-phase roadmaps unprompted. If the user asks "what's next", give 3-5 options maximum and wait.

## Session Cleanup Pattern

For runtime maps that grow unbounded (`resume_tokens`, `partial_transfers`):

```rust
// Spawn cleanup task near server state initialization
let state = state.clone();
tokio::spawn(async move {
    let mut interval = tokio::time::interval(Duration::from_secs(300));
    loop {
        interval.tick().await;
        state.evict_expired_resume_tokens();
    }
});
```

## Protocol Version Negotiation

For 100-year wire format durability:

```rust
pub trait ProtocolNegotiator: Send + Sync {
    fn negotiate(&mut self, peer_versions: &[ProtocolVersion]) 
        -> ContinuumResult<ProtocolVersion>;
    fn supported_versions(&self) -> &[ProtocolVersion];
    fn supports_version(&self, version: &ProtocolVersion) -> bool;
}

pub struct ProtocolVersion {
    pub major: u16,
    pub minor: u16,
    pub patch: u16,
}

impl ProtocolVersion {
    pub fn is_compatible_with(&self, other: &Self) -> bool {
        self.major == other.major  // Major must match
    }
}
```

## References

- `references/continuum-feature-gating-pitfalls.md` — cfg-gating mistakes and fixes
- `references/continuum-stabilization-notes.md` — full session notes