# Continuum v1.0 Implementation Notes

This document captures technical learnings from the Continuum v1.0 implementation pass (August 30, 2026).

## Goal
Implement all 12 workstreams from the v1.0 implementation plan to make Continuum competitive with Parsec, TeamViewer, AnyDesk, etc.

## Crates Created

| Crate | Purpose | Tests |
|-------|---------|-------|
| `continuum-ice` | ICE/STUN NAT traversal | 7 |
| `continuum-codec` | Video encoder/decoder traits | 3 |
| `continuum-discovery` | mDNS local peer discovery | 2 |
| `continuum-session` | Multi-viewer session management | 4 |
| `continuum-security` | CryptoProvider, post-quantum, security policy | 7 |
| `continuum-performance` | GPU pipeline, adaptive quality, bandwidth | 7 |
| `continuum-testing` | Chaos, fuzz, compatibility testing | 6 |
| `continuum-ui` | Address book, history, settings | 6 |
| `continuum-web` | WebRTC signaling server | 4 |
| `continuum-mobile` | iOS/Android FFI bindings | 3 |
| `continuum-enterprise` | SSO, LDAP, audit logging | 3 |
| `continuum-plugins` | WASM plugin system | 3 |

**Total: 55 new tests, 12 new crates**

## Crate Instability for 100-Year Projects

The STUN/TURN crate ecosystem is fragmented:
- `stun` crate was migrated to a webrtc-rs monorepo in 2022
- `turn` crate has limited maintenance
- Most ICE crates are wrappers around C libraries or WebRTC stacks

**Lesson:** For foundational infrastructure (NAT traversal, core protocols), implementing the protocol yourself from the RFC is often MORE durable than depending on potentially abandoned crates. STUN (RFC 5389) is a simple binary protocol (~200 lines of Rust).

**When to implement vs. depend:**
- Implement: small, stable protocols (STUN parsing, simple binary formats)
- Depend on: complex, evolving protocols (QUIC, TLS, H.264 encoding)

## Cross-Crate Error Propagation Pattern

When adding new variants to `ContinuumError` in `continuum-core`:

1. Add variant to `continuum-core/src/lib.rs`
2. Search ALL workspace members for `crate::ContinuumError` or `continuum_core::ContinuumError` references
3. Update each usage site (match arms, error conversions, etc.)
4. Run `cargo check --workspace` to catch stragglers

**Recurring pattern:** Adding `Ice`, `Stun`, `Timeout`, `InvalidAddress`, `Internal` errors required updates in `continuum-ice`, `continuum-discovery`, `continuum-session`, `continuum-security`, `continuum-codec`.

## ICE/STUN Implementation Notes

### STUN Message Structure
- 20-byte header: 2-bit zero, 14-bit method, 2-byte length, 4-byte magic cookie (0x2112A442), 12-byte transaction ID
- Attributes: type (2 bytes), length (2 bytes), value (variable, 4-byte aligned)
- XOR-MAPPED-ADDRESS: port XOR'd with 0x2112, IP XOR'd with magic cookie bytes

### ICE Candidate Types
- Host (local IP)
- Server reflexive (from STUN)
- Peer reflexive (discovered during connectivity check)
- Relayed (from TURN)

### Implementation Approach
```rust
// Custom STUN parser (no external deps)
pub struct StunMessage { ... }
impl StunMessage {
    pub fn binding_request() -> Self { ... }
    pub fn to_bytes(&self) -> Vec<u8> { ... }
    pub fn from_bytes(data: &[u8]) -> Result<Self, StunError> { ... }
    pub fn get_mapped_address(&self) -> Option<SocketAddr> { ... }
}
```

## mDNS Discovery with mdns-sd Crate

### API Differences (0.12 vs 0.21)
- 0.12: `ServiceInfo::new(service_type, instance_name, host_name, ip, port, properties)`
- 0.21: Different signature, more features

### Property Parsing
```rust
// TxtProperty::val() returns Option<&[u8]>, NOT &str
let props: HashMap<String, String> = info
    .get_properties()
    .iter()
    .filter_map(|p| {
        let key = p.key().to_string();
        let val = p.val().map(|v| String::from_utf8_lossy(v).to_string())?;
        Some((key, val))
    })
    .collect();
```

### Shutdown Returns Receiver
```rust
// mdns_sd 0.12: shutdown() returns Result<Receiver<DaemonStatus>>
self.daemon
    .shutdown()
    .map(|_receiver| ())
    .map_err(|e| ContinuumError::Internal(e.to_string()))
```

## CryptoProvider Trait Design

Post-quantum readiness requires swappable crypto:

```rust
pub trait CryptoProvider: Send + Sync {
    fn name(&self) -> &str;
    fn supported_algorithms(&self) -> Vec<KeyExchangeAlgorithm>;
    fn generate_keypair(&self, algorithm: KeyExchangeAlgorithm) 
        -> Result<(Vec<u8>, Vec<u8>), ContinuumError>;
    fn key_exchange(&self, algorithm: KeyExchangeAlgorithm, secret_key: &[u8], public_key: &[u8]) 
        -> Result<Vec<u8>, ContinuumError>;
    fn derive_session_key(&self, shared_secret: &[u8], salt: &[u8], info: &[u8]) 
        -> Result<Vec<u8>, ContinuumError>;
}

pub enum KeyExchangeAlgorithm {
    X25519,
    Kyber512,
    Kyber768,
    Kyber1024,
    X25519Kyber768,  // Hybrid
}
```

**Placeholder pattern for unstable PQ crates:** Use placeholder types that define the interface now, swap in real implementations (e.g., `pqcrypto` crate) when they stabilize.

## Video Codec Pipeline

```rust
pub trait VideoEncoder: Send {
    fn encode(&mut self, frame: &VideoFrame) -> ContinuumResult<EncodedFrame>;
    fn encode_keyframe(&mut self, frame: &VideoFrame) -> ContinuumResult<EncodedFrame>;
    fn set_bitrate(&mut self, kbps: u32);
    fn set_quality(&mut self, quality: u8);
    fn capabilities(&self) -> EncoderCapabilities;
}

pub trait VideoDecoder: Send {
    fn decode(&mut self, frame: &EncodedFrame) -> ContinuumResult<VideoFrame>;
}
```

**JPEG baseline:** Start with software JPEG (`image` crate), add H.264/H.265 hardware encoders as optional features.

## Session Management

Multi-viewer with permissions:

```rust
pub struct SessionPeer {
    pub machine_id: String,
    pub display_name: String,
    pub joined_at: DateTime<Utc>,
    pub permissions: Permissions,
}

pub struct Permissions {
    pub can_view: bool,
    pub can_control: bool,
    pub can_transfer_files: bool,
    pub can_clipboard: bool,
    pub can_audio: bool,
}
```

## Performance Optimization

### Adaptive Quality Controller
```rust
pub struct AdaptiveQualityController {
    target_latency_ms: f32,
    current_quality: u8,
    current_fps: u32,
}

impl AdaptiveQualityController {
    pub fn update(&mut self, stats: &ConnectionStats) -> QualityDecision {
        // Reduce quality if RTT > 1.5x target
        // Increase quality if RTT < 0.5x target
    }
}
```

### Bandwidth Estimator
Sliding window estimator with configurable window size and max duration.

## Testing Framework

### Chaos Engineering
```rust
pub struct ChaosEngine {
    network_conditions: NetworkConditions,
    cpu_load: Option<CpuLoad>,
}

impl ChaosEngine {
    pub async fn simulate_latency(&self) { ... }
    pub fn should_drop_packet(&self) -> bool { ... }
}
```

### Fuzz Harness
```rust
pub struct FuzzHarness {
    iterations: usize,
    seed: u64,
}

impl FuzzHarness {
    pub fn run<F, T>(&self, target: F) -> FuzzResult { ... }
}
```

## Common Errors This Session

| Error | Cause | Fix |
|-------|-------|-----|
| `E0433: cannot find ContinuumError in crate` | Using `crate::ContinuumError` instead of `continuum_core::ContinuumError` | Import from `continuum_core` |
| `E0670: async fn not permitted in Rust 2015` | Stale incremental artifacts | `cargo clean -p <crate>` |
| `E0308: mismatched types` | `shutdown()` returns Receiver, not () | `.map(\\|_receiver| ())` |
| `E0599: method cannot be called on Option<&[u8]>` | `TxtProperty::val()` returns Option, not String | Use `.map(\\|v\\| String::from_utf8_lossy(v).to_string())` |
| Unused import warnings | `use crate::ContinuumResult` when macros auto-import | Remove explicit import |
| `E0425: cannot find type in crate` | Missing `pub use` in lib.rs | Add re-export |
| `E0515: cannot return value referencing temporary` | Returning reference to RwLock guard | Clone the value before returning |

## Verification Commands

```bash
# Check single crate
cargo check -p continuum-ice

# Check entire workspace
cargo check --workspace

# Test specific crate
cargo test -p continuum-ice --lib

# Test workspace (excluding known-broken)
cargo test --workspace --tests -- --skip continuum_ai
```

## References

- `references/continuum-stabilization-notes.md` — v0.3.0 stabilization context
- `references/continuum-architecture-patterns.md` — trait abstractions and patterns
- `references/continuum-feature-gating-pitfalls.md` — cfg-gating mistakes