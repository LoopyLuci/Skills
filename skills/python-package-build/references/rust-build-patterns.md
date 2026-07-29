# Rust Protobuf Compilation & Build Patterns

## Problem

When building a Rust crate that uses prost-generated protobuf code, you get a
chicken-and-egg problem: the build script (build.rs) generates the Rust code
from .proto files, but the main library references the generated types and
wont compile without them. Additionally, prost-build 0.13 has API differences
from earlier versions.

## Pattern: Isolated gen-project

Create a minimal temporary Cargo project to run prost-build in isolation,
verify API compatibility, and inspect generated code:

```
/tmp/protogen/
├── Cargo.toml          # minimal: prost + prost-types + protoc-bin-vendored
├── build.rs            # compile .proto -> src/protobuf/streamsync.rs
└── src/
    └── lib.rs          # include!("protobuf/streamsync.rs")
```

Then copy `src/protobuf/streamsync.rs` into the real project. This lets you
validate proto compilation without fighting the real project's dependency graph.

## Key prost-build 0.13 Deviations from Earlier Versions

| What was expected | What prost-build 0.13 actually does |
|---|---|
| `Config::protoc_executable(path)` — does not exist | Use `std::env::set_var("PROTOC", path)` before `compile_protos()` |
| `protoc_bin_vendored::protoc_bin_path()` returns `PathBuf` | Call `.as_os_str()` to set the env var |
| `bytes = "bytes"` produces `bytes::Bytes` fields | `bytes = "vec"` in generated code means `Vec<u8>`, not `bytes::Bytes` |
| Oneof module: `streamsync_message::Payload` | Generated as `stream_sync_message::Payload` (prost applies `heck` crate word-splitting) |
| Proto field `string action = 3` → `Notification.actions` | Generated field is `Notification.action` (singular, not plural) |
| `ClipboardMessage.image_mime` as a direct field | It is a oneof variant: `clipboard_message::Content::ImageMime(String)` |

## Common Third-Party API Gotchas (as of mid-2026)

### mdns-sd 0.13
- `ServiceInfo::new()` is generic: `(ty_domain, my_name, host_name, ip, port, properties)`
  where `ip: impl AsIpAddrs` and `properties: impl IntoTxtProperties`
- Service properties: `&[(&str, &str)]` or `HashMap<String, String>` both work
- `ServiceEvent::ServiceFound(service_type, fullname)` — not `ServiceAdded`
- `ServiceEvent::ServiceResolved(info)` where `info: ServiceInfo`
- `ServiceEvent::ServiceRemoved(service_type, fullname)`
- `ServiceInfo` has: `get_hostname()`, `get_port()`, `get_addresses()`, `get_properties()`
- `get_instance_name()` may not exist — use `get_hostname()` instead
- `ServiceDaemon::unregister()` takes no args in 0.13 (or use `shutdown()`)
- `ServiceDaemon::resolve()` static method may not exist — daemon auto-resolves via the browse receiver

### aes-gcm 0.10
- `AeadInOut` does NOT exist — use `aes_gcm::aead::Aead` trait
- Both `encrypt()` and `decrypt()` are provided by the `Aead` trait, imported from `aes_gcm::aead::Aead`
- Key creation: `Key::<Aes256Gcm>::from_slice(&key_bytes)`
- Nonce: `Nonce::from_slice(&nonce_bytes)` — 12 bytes for AES-256-GCM

### tokio-tungstenite 0.24
- `MaybeTlsStream<TcpStream>` does not implement `peer_addr()` directly
- Get peer address from the underlying `TcpStream` before wrapping in WebSocket
- `tungstenite::Message::Frame(_)` variant exists in some minors — must be matched

### tokio 1.x
- `AsyncSeekExt` trait must be imported: `use tokio::io::AsyncSeekExt;`
- `File::seek()` requires this trait in scope
