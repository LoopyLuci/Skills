# WebBuilder-Specific PyQt5 Patterns

These patterns are specific to the WebBuilder desktop app. For general PyQt5 patterns, see the main SKILL.md.

## Hardware Abstraction Layer (Multi-Threading + Multi-GPU)

For CPU/GPU-aware work distribution, implement a Hardware Abstraction Layer.

**Modules:**
```
webbuilder/hardware/
├── detector.py    # CPU/GPU/memory detection (NVML, psutil, platform)
├── gpu.py         # GPUManager — device assignment, load tracking
├── scheduler.py   # TaskScheduler — distribute work across threads + GPUs
├── pool.py        # ComputePool — dynamic worker scaling
└── workstealing.py # WorkStealingQueue — optimal load balancing
```

**Detection priority:**
1. NVIDIA: `pynvml` (NVML) → fallback to `nvidia-smi` subprocess
2. AMD: `rocm-smi` subprocess
3. Intel: platform-specific detection
4. Apple Silicon: `platform.system() == 'Darwin' and platform.machine() == 'arm64'`

## MCP (Model Context Protocol)

For AI-to-application tool integration, implement an MCP server.

**Pattern:**
```python
# JSON-RPC 2.0 envelope
class MCPRequest:
    jsonrpc: str = "2.0"
    id: Optional[str]
    method: str  # "initialize", "tools/list", "tools/call"
    params: dict

class MCPResponse:
    result: Any = None
    error: Optional[dict] = None
```

**Server must implement:**
- `initialize` → return protocol version + server info
- `tools/list` → return tools with `name`, `description`, `inputSchema`
- `tools/call` → execute tool by name with arguments

**GUI Integration:**
```python
class MCPSettingsDialog(QDialog):
    # Tab 1: Server list (add/edit/remove/connect/disconnect)
    # Tab 2: Available tools from connected servers
    # Tab 3: About MCP
```

**Pitfall:** MCP server runs IN-PROCESS with the GUI (not a separate process). Tool handlers receive `self.window` to interact with the application. This means a crashing tool handler crashes the app — wrap handlers in try/except.

## Live AI Model Discovery (NO Hardcoded Models)

**Critical user requirement:** Models MUST NOT be hardcoded. They must be fetched live from provider APIs.

**Providers to support:**
- OpenAI (`/v1/models`)
- Anthropic (`/v1/models`)
- OpenRouter (`/api/v1/models?limit=500`) — 400+ models
- xAI Grok (`/v1/models`)
- Nous Research (`/v1/models`)
- Ollama (`/api/tags` — local, no key needed)
- LM Studio (`/v1/models` — local, no key needed)

**Architecture:**
```python
# webbuilder/ai/__init__.py
class BaseProvider(ABC):
    api_key: str
    _models_cache: list[ModelInfo]
    _cache_ttl = timedelta(minutes=30)

    @abstractmethod
    async def fetch_models(self) -> list[ModelInfo]: ...

    @abstractmethod
    async def stream_chat(self, messages, model, **kwargs) -> AsyncIterator[str]: ...
```

**Model Router:**
```python
class ModelRouter:
    providers: dict[str, BaseProvider]
    fallback_order: list[str]

    async def get_all_models(self) -> list[ModelInfo]:
        # Fetch from all providers, aggregate results

    async def stream_chat(self, messages, model, provider_id=None):
        # If provider specified, use it
        # Otherwise try each provider in fallback order
```

## Post-Quantum Crypto Readiness

For 100-year durability, WebBuilder includes a post-quantum crypto module with hybrid classical + PQ operations.

**Algorithms:**
- **Kyber-768**: Key Encapsulation Mechanism (KEM) based on Module-LWE
- **Dilithium-2**: Digital Signature Scheme based on Module-LWE
- **Hybrid**: Classical ECDH + PQ Kyber key exchange
- **CryptoEngine**: Algorithm agility — swap algorithms without changing the API

**Pitfall**: The `CryptoEngine.generate_keypair()` returns `(pub, priv)` bytes, NOT nested tuples. For PQ algorithms, it returns the Dilithium key pair. For classical algorithms, it returns `(pub, priv)` where `pub = hashlib.sha256(priv).digest()`.

**Pitfall**: `dilithium_sign` embeds the public key in the signature (format: `pk || sig || commitment`). The commitment binds the signature to both the public key AND the message, preventing signature reuse across messages.

## 100-Year Architecture Principles

1. **Zero dependencies in core**: The core logic must depend ONLY on language standard library.
2. **Everything is a plugin**: Features beyond core are plugins.
3. **Open, human-readable formats**: Native storage uses open formats (JSON with schema versioning).
4. **Self-describing data**: All models implement `to_dict()` and `from_dict()` with schema identifiers.
5. **Composability over monoliths**: Small, focused tools that compose.
6. **Deterministic behavior**: Same input → same output.
7. **Community governance**: The platform should be governable by its community.

## Resilience Systems

**BackupManager**: Auto-backup with versioning and retention policy, integrity verification via SHA256 checksums, compression (gzip).

**SQLiteStorage**: Structured storage with WAL mode for crash recovery, migration support via `MigrationSystem`.

**HealthMonitor**: System resource monitoring (CPU, memory, disk), application health checks, alert thresholds.

**Watchdog**: Process monitoring and auto-restart on crash, resource leak detection, restart rate limiting.

**UpdateManager**: GitHub release checking, auto-update with rollback support.

## Self-Learning ML Pipeline

```python
pipeline = SelfLearningPipeline(model=model, min_interactions=10, retrain_interval=100)
pipeline.record_interaction(model_id, input_data, output_data, feedback=1.0)
should_retrain, metrics = pipeline.check_retrain()
if should_retrain:
    pipeline.retrain()
    pipeline.save()
```

**Pitfall**: The self-learning pipeline records interactions from user actions, not from training. Training generates the model, and the pipeline records when the model is used and what the feedback is.
