# Cross-Platform Firewall & Thread Config Reference

## Platform-Specific Firewall Backends

| Platform | Library | Crate | API |
|----------|---------|-------|-----|
| Windows | Windows Filtering Platform (WFP) | `windows` (0.58) | `New-NetFirewallRule` via PowerShell |
| Linux | nftables | `nftables` (0.5) | Netlink socket API |
| Linux (legacy) | iptables | `iptables` (0.6) | iptables C library FFI |
| macOS | pf (Packet Filter) | subprocess | `pfctl` command |
| Universal | nftables JSON | `serde_json` | nftables JSON API via stdin |

## Thread Pool Config for 24-Thread CPUs (Ryzen 5900X)

```
Thread allocation:
  DNS workers:             4  
  Packet capture:          4
  Pipeline processing:    12
  GPU coordination:        2
  Background scheduler:    2
                        ─────
                          24
```

### Rust Implementation

```rust
use rayon::ThreadPoolBuilder;
use std::sync::Arc;
use tokio::net::UdpSocket;

// Worker pool for CPU-bound tasks (blocklist matching, packet analysis)
let data_pool = rayon::ThreadPoolBuilder::new()
    .num_threads(12)
    .thread_name(|i| format!("sentinel-data-{}", i))
    .build()?;

// Legacy: num_cpus crate provides available_parallelism()
use num_cpus;
let threads = num_cpus::get(); // Returns 24 on Ryzen 5900X
```

## Lock-Free Data Structures for High-Throughput Networking

```rust
use dashmap::DashMap;       // Sharded, lock-free reads
use scc::HashMap;           // Concurrent with fine-grained locking
use crossbeam::channel;     // Bounded channels for pipeline backpressure
use parking_lot::RwLock;    // Fastest RwLock implementation
```

## AhoCorasick API Migration (1.0+)

**Old API (0.x):**
```rust
let mut matches = ac.find(&text);
if matches.any(|m| m.end() == text.len()) { ... }
```

**New API (1.0+):**
```rust
if let Some(m) = ac.find(&text) {
    if m.end() == text.len() {
        let matched = &text[m.start()..m.end()];
        // matched may differ from text (substring match!)
    }
}
```

**Domain matching pattern:**
```rust
// AhoCorasick finds "doubleclick.net" inside "sub.doubleclick.net"
// m.start() = 4, m.end() = 19, domain.len() = 19
if let Some(m) = engine.find(&domain) {
    if m.end() == domain.len() {
        let matched = &domain[m.start()..m.end()]; // "doubleclick.net"
        return names.get(matched).map(|name| MatchResult { ... });
    }
}
```

**Wildcard (`*.domain.com`) — must not match bare domain:**
```rust
// Suffix after stripping "*." → "domain.com"
// "x.domain.com".ends_with("domain.com") && "x.domain.com".len() > "domain.com".len() → MATCH
// "domain.com".ends_with("domain.com") && "domain.com".len() > "domain.com".len() → NO MATCH
domain.ends_with(wildcard) && domain.len() > wildcard.len()
```

## Hickory DNS (formerly Trust-DNS)

```
trust-dns-proto 0.23 → renamed to hickory-proto 0.24+
trust-dns-server 0.23 → renamed to hickory-server 0.24+
trust-dns-resolver 0.23 → renamed to hickory-resolver 0.24+

Cargo.toml:
  hickory-proto = "0.24"
  hickory-server = "0.24"  
  hickory-resolver = "0.24"

Rust imports:
  use hickory_proto::op::{Message, Query};
  use hickory_proto::rr::{Name, RecordType};
```

## SvelteKit + Tailwind CSS v4 Static Adapter

- **Svelte 5 `$page`**: `$` prefix is reserved for runes. Use `window.location.pathname` with `$state()` and `$effect()` listeners instead.
- **Tailwind CSS v4 `@apply`**: Does NOT support custom class names (only built-in utilities like `bg-red-500`). Write component classes as plain CSS:
  ```css
  .glass {
    background: rgba(38, 42, 61, 0.6);
    backdrop-filter: blur(16px);
    border-radius: 1rem;
  }
  ```
- **`npm install --legacy-peer-deps`**: Required when SvelteKit + Tailwind v4 dependencies conflict.
- **Import path**: `./app.css` from `src/routes/+layout.svelte` → use `../app.css` (routes is a subdirectory of src).
