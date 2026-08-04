---
name: dns-proxy-filter
title: "DNS Proxy & Network Filter"
description: "Use when building DNS proxy/block/firewall tools in Python or Rust."
category: software-development
tags: [dns, proxy, adblocker, firewall, network-filter, python, rust, rayon, gpu-acceleration, asyncio]
---

# DNS Proxy & Network Filter — Building Network Security Tools

A reference architecture for building high-performance DNS proxies, ad-blockers, and network firewall management tools. Covers **Python** (FastAPI + dnspython + asyncio) and **Rust** (Hickory DNS + Tokio + Rayon + wgpu) implementations, plus GPU-accelerated packet inspection and cross-platform firewall management.

## Architecture Overview

**Python path:** DNS Query → DNS Proxy (asyncio UDP) → Blocklist Engine → Upstream Resolver or Block Response → SQLite Log → FastAPI REST API ←→ Dashboard → Firewall Manager (PowerShell)

**Rust path:** DNS Query → DNS Proxy (Tokio + Rayon) → Aho-Corasick Blocklist Engine → Hickory Upstream Resolver → GPU Accelerator (wgpu) → MCP/HTTP API ←→ Dashboard → Cross-Platform Firewall (WFP/nftables/pf)

## Core Patterns

### 1. Async DNS Proxy Server

Use `asyncio.DatagramProtocol` with `loop.create_datagram_endpoint()`:

```python
class DnsProtocol(asyncio.DatagramProtocol):
    def datagram_received(self, data: bytes, addr: tuple):
        asyncio.ensure_future(self._handle(data, addr))
```

Each query: parse, check blocklist, block or forward upstream, log to DB.

### 2. dnspython RDATA Construction (Critical Gotcha)

Must explicitly import submodules — dnspython lazy-loads `dns.rdtypes.IN.*`:
```python
import dns.rdtypes.IN.A
import dns.rdtypes.IN.AAAA
```

Constructor is three-arg `(rdclass, rdtype, address)`:
```python
# ✅ Correct
dns.rdtypes.IN.A.A(dns.rdataclass.IN, dns.rdatatype.A, "0.0.0.0")
# ❌ Wrong — silently fails with timeout
dns.rdtypes.IN.A.A(0, "0.0.0.0")
```

Build blocking response:
```python
response = dns.message.make_response(request)
rrset = dns.rrset.RRset(question.name, dns.rdataclass.IN, dns.rdatatype.A, ttl)
rrset.add(dns.rdtypes.IN.A.A(dns.rdataclass.IN, dns.rdatatype.A, "0.0.0.0"))
response.answer.append(rrset)
```

### 3. Blocklist Engine — Multi-Strategy Matching

Four strategies: **Exact** (set, O(1)), **Subdomain walk** (iterate parent domains), **Wildcard suffix** (set of .suffixes), **Regex** (list[re.Pattern]). Run in that order.

### 4. Multi-Format Parser

```python
PARSERS = {
    "hosts":   parse_hosts,   # "0.0.0.0 domain.com"
    "domains": parse_domains, # "domain.com" per line
    "adblock": parse_adblock, # "||domain.com^"
}
```

### 5. LRU DNS Cache

OrderedDict + timestamp-based TTL. Key: `f"{domain}:{qtype}"`.

### 6. Runtime Config Overrides

```python
class Config(BaseSettings):
    _runtime_overrides: dict[str, Any] = {}
    def set_runtime(self, key, value): ...
    def __getitem__(self, key): ...  # checks overrides first
```

Settings API handler should call `config.set_runtime()` for immediate effect.

### 7. Uvicorn Programmatically

```python
app = create_app()
uvicorn.run(app, host=config.host, port=config.port)
```
Avoid string references like `"module:app"` — they fail without `pip install -e .`

## Rust Implementation (High-Throughput)

For production systems handling millions of queries, use Rust with:

### DNS Protocol (Hickory DNS)

```rust
use hickory_proto::op::{Message, Query};
use hickory_proto::rr::{Name, RecordType};

let name = Name::from_utf8(domain)?;
let mut msg = Message::new();
msg.add_query(Query::query(name, RecordType::A));
let query_data = msg.to_vec()?;
```

### Manual Packet Construction (No Dependencies)

For minimal blocking responses, construct raw DNS packets byte-by-byte — avoids any library dependency:

```rust
let mut response = Vec::with_capacity(512);
response.extend_from_slice(&query[0..2]);        // Transaction ID
response.extend_from_slice(&[0x85, 0x80]);       // Flags: response, no error
response.extend_from_slice(&[0x00, 0x01]);       // Questions: 1
response.extend_from_slice(&[0x00, 0x01]);       // Answers: 1
response.extend_from_slice(&[0x00, 0x00]);       // Authority: 0
response.extend_from_slice(&[0x00, 0x00]);       // Additional: 0
// ... echo question section ...
response.extend_from_slice(&[0xc0, 0x0c]);       // Name pointer
response.extend_from_slice(&[0x00, 0x01]);       // Type A
response.extend_from_slice(&[0x00, 0x01]);       // Class IN
response.extend_from_slice(&[0x00, 0x00, 0x00, 0x1e]); // TTL 30s
response.extend_from_slice(&[0x00, 0x04]);       // Data length
response.extend_from_slice(&[0x00, 0x00, 0x00, 0x00]); // 0.0.0.0
```

### Parallel Blocklist Matching (Rayon + Aho-Corasick)

```rust
use rayon::prelude::*;
use aho_corasick::AhoCorasick;

// Build automaton — AhoCorasick::new() in 1.x returns Result.
// .find() returns Option<Match> (not an iterator like 0.x):
let ac = AhoCorasick::new(&patterns).expect("Aho-Corasick build");

// Exact match — check if full domain matched
if let Some(m) = self.exact.find(&domain) {
    if m.end() == domain.len() {
        return Some(MatchResult { ... });
    }
}

// Parallel matching across threads
let wildcard_match = self.wildcards.par_iter().find_any(|w| domain.ends_with(&w[..]));
let regex_match = self.regexes.par_iter().find_any(|r| r.is_match(&domain));
```

### Thread Pool Configuration

```rust
// One DNS worker per CPU thread
rayon::ThreadPoolBuilder::new()
    .num_threads(num_cpus::get())
    .thread_name(|i| format!("dns-worker-{}", i))
    .build_global()
    .unwrap();

tokio::runtime::Builder::new_multi_thread()
    .worker_threads(num_cpus::get())
    .enable_all()
    .build();
```

## GPU-Accelerated Packet Inspection

Use `wgpu` (WebGPU) compute shaders for massively parallel pattern matching:

```rust
use wgpu::*;

let instance = Instance::new(InstanceDescriptor {
    backends: Backends::all(),
    ..Default::default()
});

// Enumerate adapters — prefer discrete GPU (AMD/NVIDIA) over iGPU
let adapter = instance.enumerate_adapters(Backends::all())
    .find(|a| matches!(a.get_info().device_type, DeviceType::DiscreteGpu));
```

The RX 7900 XTX (24GB VRAM, 6144 stream processors) can process millions of patterns per kernel dispatch via WGSL compute shaders. Each GPU thread checks one blocklist pattern against the query domain.

## Cross-Platform Firewall

Use conditional compilation for platform-specific backends:

```rust
#[cfg(target_os = "windows")] // Windows Filtering Platform (WFP) or PowerShell
#[cfg(target_os = "linux")]   // nftables: `nft add rule inet filter input drop`
#[cfg(target_os = "macos")]   // pf: `pfctl -a sentinel -f -`
```

| Platform | Backend | Command |
|----------|---------|---------|
| Windows | PowerShell NetSecurity | `New-NetFirewallRule` |
| Linux | nftables | `nft add rule inet filter` |
| macOS | pf (Packet Filter) | `pfctl -a anchor -f -` |

Shared rule model across all platforms: `{ name, direction, action, protocol, port, remote_ip, process_path }`.

Use `asyncio.create_subprocess_exec("powershell.exe", "-NoProfile", "-Command", script)`:

| Operation | Command |
|-----------|---------|
| Add rule | `New-NetFirewallRule -DisplayName "PREFIX_Name" -Direction Outbound -Action Block` |
| Remove | `Remove-NetFirewallRule -DisplayName "PREFIX_Name"` |
| List | `Get-NetFirewallRule | Select DisplayName,Direction,Action,Enabled` |
| Profile | `Get-NetFirewallProfile | Select Name,Enabled,DefaultInboundAction` |

Prefix rules with a unique tag (e.g. `SENTINEL_`). Requires Administrator.

## Pitfalls

1. **dnspython rdtypes not auto-imported**: add explicit `import dns.rdtypes.IN.A`
2. **RDATA needs 3 args**: `A(rdclass, rdtype, address)` — not `(0, "0.0.0.0")`
3. **Relative imports in -m mode**: `from ..x import y` inside functions fails. Import at module level.
4. **Firewall needs Admin**: Check `IsInRole(Administrator)` before offering rule features.
5. **Data dir must exist before logging**: mkdir in `setup_logging()` before FileHandler.
6. **Vite minifier**: Use `minify: 'esbuild'` (built-in), not `terser` (extra dep).
7. **Rust wgpu InstanceDescriptor by value**: `Instance::new(InstanceDescriptor {...})` not `&InstanceDescriptor`.
8. **Rust DNS packet offset**: Manual construction's question parsing must track byte offsets. `0xc00c` = "offset 12 from message start."
9. **Rust `tokio::UdpSocket::try_clone()`**: Not available in all versions. Use `Arc::new(socket)` + `Arc::clone(&socket)` for multi-worker sharing.
10. **Rust AhoCorasick 1.x `find()`**: Returns `Option<Match>`, not an iterator. Check `if let Some(m) = ac.find(&domain)` — no `.any()` method.
11. **Rust Hickory DNS rename**: `trust-dns-proto` is now `hickory-proto` (0.24+). Use `hickory_proto::op`, not `trust_dns_proto`.
12. **Rust `#[cfg]` scope**: Conditional compilation applies to the NEXT item — each fn needs its own annotation.
13. **`skill_manage` description limit**: Creating skills via `skill_manage(action='create')` enforces descriptions ≤60 chars, not the 1024-char YAML limit. Keep under 60.

## Verification

Test each layer independently: config, database (temp DB), parsers (sample data), engine (all 4 strategies), DNS proxy (wire-format query → 0.0.0.0), schemas, firewall manager method signatures.
