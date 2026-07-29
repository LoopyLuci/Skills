# Rust Build Patterns (prost-build + crate gotchas)

Captured during StreamSync prototype — applies to any project using prost-build with protoc-bin-vendored on Windows.

## prost-build 0.13 Setup

### Cargo.toml
```toml
[build-dependencies]
prost-build = "0.13"
protoc-bin-vendored = "3"
```

### build.rs — vendored protoc
```rust
use std::path::PathBuf;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let protoc = protoc_bin_vendored::protoc_bin_path()
        .expect("vendored protoc not found");
    std::env::set_var("PROTOC", protoc.as_os_str());

    let proto_file = PathBuf::from(std::env::var("CARGO_MANIFEST_DIR")?)
        .parent().unwrap().parent().unwrap()
        .join("protocol").join("streamsync.proto");

    println!("cargo:rerun-if-changed={}", proto_file.display());

    let proto_dir = proto_file.parent().unwrap().to_path_buf();

    prost_build::Config::new()
        .out_dir(std::env::var("OUT_DIR")?)
        .compile_protos(&[proto_file.clone()], &[proto_dir])?;
    Ok(())
}
```

### lib.rs — include the generated code
```rust
pub mod proto {
    #![allow(unused_imports, dead_code, clippy::all)]
    include!(concat!(env!("OUT_DIR"), "/streamsync.rs"));
}
```

## Generated Code Quirks

| Proto concept | Generated Rust | Note |
|---|---|---|
| Package `streamsync` | Module `stream_sync` | Snake_case of package name |
| Message `StreamSyncMessage` | `proto::StreamSyncMessage` | PascalCase preserved |
| Oneof `Payload` | `proto::stream_sync_message::Payload` | Module name = snake_case of parent message |
| `bytes` fields | `bytes::Bytes` (not `Vec<u8>`) | Convert with `.to_vec()` |
| `map<string, string>` | `HashMap<String, String>` | From `std::collections` |

Example oneof access:
```rust
match msg.payload {
    Some(proto::stream_sync_message::Payload::Transfer(tm)) => {
        match tm.msg {
            Some(proto::transfer_message::Msg::Request(req)) => { ... }
            _ => {}
        }
    }
    _ => {}
}
```

## Third-Party Crate Gotchas

### mdns-sd 0.13
- `ServiceInfo::new()` takes 6 positional args: (type, instance, host, target, port, props)
- `props` must be `Option<HashMap<String, String>>` — NOT slice of tuples
- `ServiceEvent` variants: `ServiceResolved(ServiceInfo)`, `ServiceRemoved(String, String)` — no `ServiceAdded`
- `browse()` returns a `flume::Receiver<ServiceEvent>`, call `.recv()` synchronously

### aes-gcm 0.10
- Use `Aes256Gcm::new_from_slice(&key)` — NOT `::new()`
- Nonce is exactly 12 bytes (`aead::Nonce::from_slice(&[u8; 12])`)
- Ciphertext format: `nonce_bytes + ciphertext` (prepend nonce)
- Import: `use aes_gcm::aead::{Aead, KeyInit}` — `AeadInOut` was removed in 0.10.3
- `aead::Aead` provides `.encrypt(nonce, plaintext)` and `.decrypt(nonce, ciphertext)`
- Returns `aead::Result<Vec<u8>>`

### tokio-tungstenite 0.24
- `TcpListener::bind()` requires `SocketAddr`, not `u16` or string:
  ```rust
  let addr: SocketAddr = format!("0.0.0.0:{}", port).parse()?;
  let listener = TcpListener::bind(addr).await?;
  ```
- `accept_async(stream)` returns `WebSocketStream<MaybeTlsStream<TcpStream>>`
- Message type is `tokio_tungstenite::tungstenite::Message`
- `connect_async(url)` requires full `ws://host:port/path` URL, not just addr
