# Network Tools MCP Server — Sentinel Reference Pattern

A working MCP server for network security tools (adblocker + firewall) built in Rust,
with client libraries in Python, TypeScript, Swift, and Kotlin.

## Tool Inventory (10 tools)

| Tool | Description | Input |
|------|-------------|-------|
| `get_status` | System health + hardware capabilities | {} |
| `get_stats` | Real-time DNS/firewall counters | `{detailed?: bool}` |
| `get_capabilities` | CPU threads, GPU name/VRAM, platform | {} |
| `block_domain` | Add domain to blocklist | `{domain: str, list?: str}` |
| `allow_domain` | Remove domain from blocklist | `{domain: str}` |
| `get_query_log` | Paginated DNS query history | `{page, page_size, blocked_only}` |
| `add_firewall_rule` | Create allow/block rule | `{action, direction, port?, ip?, protocol?}` |
| `remove_firewall_rule` | Delete rule by ID | `{rule_id: str}` |
| `update_blocklists` | Refresh blocklists from sources | `{source?: str}` |
| `set_config` | Change runtime parameter | `{key: str, value: str}` |

## Rust Server Pattern

```rust
// WebSocket-based MCP server with tokio-tungstenite
pub async fn start(&self, port: u16) -> Result<()> {
    let listener = TcpListener::bind(format!("127.0.0.1:{}", port)).await?;
    loop {
        let (stream, peer) = listener.accept().await?;
        let ws = tokio_tungstenite::accept_async(stream).await?;
        let (write, mut read) = ws.split();
        while let Some(msg) = read.next().await {
            let response = Self::handle_request(&text, &state).await;
            write.send(Message::Text(response)).await?;
        }
    }
}
```

JSON-RPC dispatch via match on `request.method` with structured error responses:

```rust
match request.method.as_str() {
    "get_status" => handle_get_status(request.id, state).await,
    "block_domain" => handle_block_domain(request.id, params, state).await,
    // ... 8 more tools
    _ => JsonRpcResponse { error: Some(JsonRpcError { code: -32601, message: format!("Unknown: {}", method) }) }
}
```

## Client Consistency Pattern

The same 8 core tools (`get_status`, `get_stats`, `get_capabilities`, `block_domain`,
`allow_domain`, `get_query_log`, `add_firewall_rule`, `set_config`) must be implemented
identically across every client language. Verification: grep for tool names in each
client file and count matches.

## Hardware Capabilities Response

The `get_capabilities` tool returns a standardized shape that every client understands:

```json
{
  "cpu_cores": 12,
  "cpu_threads": 24,
  "memory_gb": 64.0,
  "gpu_available": true,
  "gpu_name": "AMD Radeon RX 7900 XTX",
  "gpu_vram_gb": 24.0,
  "igpu_available": true,
  "platform": "windows"
}
```

## Event Subscription Model

Clients can subscribe to real-time events via a persistent WebSocket connection:

| Event | Payload |
|-------|---------|
| `dns_query_blocked` | `{domain, blocklist, client_ip, timestamp}` |
| `dns_query_allowed` | `{domain, response_time_ms}` |
| `firewall_rule_matched` | `{rule_name, action, src_ip, dst_ip, port}` |
| `threat_detected` | `{domain, threat_score, action}` |
| `blocklist_updated` | `{rules_loaded, sources}` |

Implemented via a `broadcast::Sender<serde_json::Value>` in Rust — each new connection
subscribes to the receiver and forwards events as JSON-RPC notifications.
