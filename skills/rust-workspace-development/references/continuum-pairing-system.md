# Continuum Pairing System Design Reference

## Overview

Comprehensive zero-friction pairing and connection system designed for Continuum v0.3.0+. The goal: two machines connect with **zero networking knowledge, zero IP addresses, zero configuration** — just a short pairing code or QR scan.

## Design Principles

1. **Zero knowledge** — users never need to know IPs, ports, or network topology
2. **Zero configuration** — automatic discovery, automatic NAT traversal, automatic encryption
3. **Minimal data** — pairing codes are short (6-8 characters), all key exchange is derived
4. **Multiple paths** — local discovery, relay, direct — all automatic
5. **Cryptographic identity** — machines have persistent identities, pairing is binding identity to identity
6. **100-year durability** — modular, versioned, algorithm-agile

## Key Components

### Machine Identity
- Ed25519 signing keys (persistent, generated on first run)
- Machine ID = first 8 bytes of Blake3(public_key)
- Stored at `~/.config/continuum/identity.json`

### Pairing Code System
- Format: `XXXX-XXXX` (8 chars + dash)
- Alphabet: `0123456789abcdefghjkmnpqrstvwxyz` (no ambiguous chars)
- 40 bits entropy = ~1 trillion codes
- One-time codes expire after 10 minutes
- Rate limited: 10 attempts/minute

### Discovery Methods (Priority Order)
1. **Local cache** — previously paired machines
2. **mDNS** — same LAN, automatic via `mdns-sd` crate
3. **QR code** — proximity, scan to pair
4. **Relay** — any network, routes by pairing code
5. **Manual** — enter code, system tries all methods

### Pairing Protocol
- **SPAKE2+** — password-authenticated key exchange
- **Noise XX+PSK** — mutual auth, forward secrecy, 0-RTT
- **SAS** — Short Authentication String for MITM detection

### Connection Layer
- **ICE** — Interactive Connectivity Establishment (STUN + TURN)
- **QUIC** — encrypted transport with TLS 1.3
- **Relay fallback** — when direct connection fails

## Implementation Status (v0.3.0)

- [x] `continuum-core` crate with trait definitions
- [x] `MachineIdentity` with Ed25519 keys
- [x] Pairing code generation/validation
- [x] 8 unit tests passing
- [ ] mDNS discovery
- [ ] QR code generation/scanning
- [ ] SPAKE2+ integration
- [ ] ICE/STUN/TURN integration
- [ ] Relay server session management
- [ ] Connection state machine
- [ ] Trust store and key pinning

## Reference Implementation

See `docs/PAIRING_SYSTEM.md` for the complete 16-section design document.

## Key Crates

- `continuum-core` — core traits and types
- `continuum-security` — crypto implementations
- `continuum-transport` — QUIC, capture, codec
- `relay-server` — NAT traversal relay

## Security Considerations

- SPAKE2+ resists offline dictionary attacks
- SAS verification prevents MITM
- Key pinning detects identity changes
- Post-quantum ready (algorithm agility)
- Forward secrecy via ephemeral keys