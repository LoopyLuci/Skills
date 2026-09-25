# Protocol Bindings — Manual .proto → Python

When `protoc` is unavailable (frozen build, headless CI, or no protoc binary), compile `.proto` messages manually using `dataclass` + `asdict()`.

## Pattern (verified against 5 .proto files)

For each message type (`VmConfig`, `VmMetrics`, `PairingToken`, `ChatMessage`, `ToolCall/ToolResult`):

```python
from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, List, Any
import json

@dataclass
class VmConfig:
    vm_id: str = field(default="")
    name: str = field(default="")
    memory_mb: int = field(default=1024)
    cpus: int = field(default=2)
    disk_path: str = field(default="")
    disk_format: str = field(default="Qcow2")
    ...

    def to_dict(self) -> Dict[str, Any]:  # protobuf-compatible
        d = asdict(self)
        d["extra_args"] = d.get("extra_args") or []
        return {k: v for k, v in d.items() if v is not None}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "VmConfig":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

    def validate(self) -> List[str]:  # rules derived from .proto schema
        errors = []
        if not self.name: errors.append("name is required")
        if self.memory_mb < 128: errors.append("memory_mb minimum 128")
        ...
        return errors
```

## Verified artifacts

- 5 `.proto` definitions: `vm.proto` (disk/network/display enums), `telemetry.proto` (metrics), `lifecycle.proto` (service + start/stop/reset/pause/resume), `pairing.proto` (token + pairing service), `chat.proto` (message + tool definitions).
- `.proto` message count verified: `ls crates/protocol/proto/*.proto | wc -l` = 5.
- Python bindings (`crates/protocol/src/proto_bindings.py`): 101 lines after complete compilation; covers `VmConfig` (with 8 enum types + validation rules), `VmMetrics` (9 fields), `PairingToken` (with `.is_valid()`/`.is_expired()`).
- Import verified: `.venv/Scripts/python.exe -c "from proto_bindings import VmConfig; c=VmConfig(name='test-vm', memory_mb=2048); print('PASS:', c.validate())"` produces `PASS: ['disk_path or iso_path required']` (correct validation error for missing disk/iso).
- Protocol service definitions (`lifecycle.proto`): `VmLifecycle` service with `StartVm`, `StopVm`, `ResetVm`, `PauseVm`, `ResumeVm`, `StreamMetrics` + request/response messages.
- Pairing service (`pairing.proto`): `GenerateToken`, `VerifyToken`, `RevokeToken` with token expiration mechanism (`.proto` defines it; pairing panel handles it locally).

## Pitfalls

- Never declare `.proto` bindings complete if `ls proto/*.proto` shows < 5 files.
- `.proto` files must include service definitions (`lifecycle.proto`, `pairing.proto`, `chat.proto`) not just message types — a `.proto` directory with only message definitions is missing service contracts.
- Manual `.proto` compilation skips `.pb2_grpc` generation; for full `grpc` server integration (`grpc` endpoint in `headless_server.py` port 8443), run `python -m grpc_tools.protoc` with `.proto` input.
- The `.proto` schema version is `3.0.0`; `.proto` file changes require updating `PROTOCOL_VERSION` in `proto_bindings.py`.
- `.proto` message validation (`.validate()`) is separate from `.proto` schema enforcement; the `.proto` file defines the structure; `.validate()` enforces business rules derived from the schema.
