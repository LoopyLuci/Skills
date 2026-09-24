---
name: desktop-app-development
description: Build native desktop apps for web building platforms.
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [desktop, pyqt5, electron, tauri, gui, drag-and-drop, native]
---

# Desktop App Development for Web Builders

Build production-grade native desktop applications for web and app building platforms. Covers PyQt5, Electron, and Tauri.

## Trigger

Use when the user wants to build a native desktop app for building websites/apps, a visual drag-and-drop editor, or a desktop companion to a web-based builder.

## User Preferences (Always-On)

### Exhaustive Scope
When this user says "proceed with all" or "properly proceed optimally with all phases", they mean ALL options — not a subset. They want comprehensive scope, picking all options, exhaustive implementation.

When the user says:
- "Properly proceed with all" → implement everything, don't ask which subset
- "What are the optimal next steps?" → give actionable next steps that move the project forward, NOT "stop building" or "ship what's built". The user wants to keep improving the project.
- "There MUST be ML models" → build custom ML, don't suggest external APIs
- "Properly proceed with all phases optimally" → execute all remaining phases completely
- "There can be no errors, issues, bugs, placeholders, stubs, warnings, etc." → ZERO tolerance for incomplete work. Eliminate ALL pass stubs, TODO comments, silent exception swallowing, and placeholder implementations. Replace with proper implementations or logging.

**Workflow preference**: The user wants immediate action when they say "proceed". Don't present multiple-choice questions — just execute exhaustively. When they ask for next steps, give them a concrete list of improvements to make, not reasons to stop.

### Repository Naming
The repository is named **`DiskRipper`** — no numbers, no trailing 's'. The git hash notation (e.g., `@9661477`) refers to a commit hash, not a version number in the repo name. Always use just "DiskRipper" when referring to the project.

### Cross-Platform Requirement
**Hard requirement**: The app MUST be 100% native cross-platform — Windows, Linux, and macOS. This is non-negotiable.

The codebase achieves this through:
- 66+ `#[cfg(target_os)]` annotations for platform-specific code
- Separate modules: `native_win.rs` (Windows), `linux_sg.rs` (Linux), `macos_iokit.rs` (macOS)
- Platform-specific dependencies in `Cargo.toml`
- CI/CD builds for all 3 platforms
- Tauri 2 uses native webviews (WebView2, WebKitGTK, WebKit)

When building new features, always implement cross-platform support from the start.

## Architecture

Three-panel layout: Left sidebar (component library + templates), Center canvas (live preview with viewport switching), Right panel (properties editor).

## PyQt5 (Recommended for Windows)

```python
from PyQt5.QtWidgets import QApplication, QMainWindow

class WebBuilderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.project = {...}
        self.selected_section = None
        self.history = []
        self.history_index = -1
        self.init_ui()
        self.apply_theme()
        self.save_history()
```

### Key Patterns

**Three-Panel Splitter:**
```python
splitter = QSplitter(Qt.Horizontal)
splitter.addWidget(self.create_left_sidebar())    # 240px
splitter.addWidget(self.create_center_canvas())    # flex
splitter.addWidget(self.create_right_panel())      # 300px
splitter.setSizes([240, 1000, 300])
```

**Component Library:**
```python
# Group by category
categories = {}
for cid, comp in COMPONENTS.items():
    cat = comp['category']
    if cat not in categories:
        categories[cat] = []
    categories[cat].append((cid, comp))

# Create buttons
for cid, comp in items:
    btn = QPushButton(f"{comp['icon']}  {comp['name']}")
    btn.clicked.connect(lambda checked, t=cid: self.add_section(t))
```

**Section Rendering:**
```python
def make_section_content(self, section):
    p = section['props']
    if section['type'] == 'hero':
        w.setStyleSheet(f'background: {p["backgroundColor"]}; padding: 80px 40px;')
        # ... render hero
    elif section['type'] == 'features':
        # ... render features
    return w
```

**Properties Panel:**
```python
def render_properties(self):
    for child in self.prop_content.children():
        if isinstance(child, QWidget):
            child.deleteLater()
    # ... build editors based on section.props
```

**History:**
```python
def save_history(self):
    self.history = self.history[:self.history_index + 1]
    self.history.append(json.dumps(self.project))
    self.history_index = len(self.history) - 1
```

**Keyboard Shortcuts:**
```python
def keyPressEvent(self, event):
    if event.key() == Qt.Key_Delete:
        self.delete_selected()
    elif event.key() == Qt.Key_Z and event.modifiers() & Qt.ControlModifier:
        self.undo()
```

**Dark Theme:**
```python
def apply_theme(self):
    self.setStyleSheet('''
        QMainWindow { background: #0f172a; }
        QSplitter::handle { background: #334155; width: 2px; }
    ''')
```

## Electron

```bash
npm config set ignore-scripts false
npm install electron
```

Project structure: `main.js` (main process), `preload.js` (context bridge), `index.html` (frontend). Use `ipcMain.handle()` for IPC handlers and `contextBridge.exposeInMainWorld()` for secure preload scripts.

## Tauri 2 (Rust Backend + Web Frontend)

Rust backend with web frontend. Smaller bundle but requires Rust toolchain. Use `#[tauri::command]` for handlers and `tauri::Builder` for setup.

### Tauri 2 workspace monorepo pattern
For production games/tools, split into crates:

```
app/
  src-tauri/
    Cargo.toml          # app crate depends on ../crates/*
    src/main.rs         # tauri::Builder, tray, AppState
    src/genetics.rs     # tauri commands
    src/network.rs      # tauri commands
    src/save.rs         # tauri commands
    tauri.conf.json
crates/
  genetics/             # standalone deterministic engine
    Cargo.toml
    src/lib.rs
  protocol/             # cross-platform schema + crypto
    Cargo.toml
    src/lib.rs
server/                 # authoritative server
  Cargo.toml
  src/main.rs
workspace Cargo.toml at repo root with members:
  crates/genetics, crates/protocol, server, app/src-tauri
```

Workspace `Cargo.toml` must set `edition = "2021"` explicitly and `resolver = "2"`.

### Windows linking fix
On Windows, if `cargo check` fails with `link.exe: extra operand ...` during build-script linking, it is not always a missing VS C++ workload. Known causes:
- workspace `Cargo.toml` missing `edition = "2021"`, causing build scripts to compile as Rust 2015 and produce malformed linker args
- stale `target/` from a prior workspace state

Fix: ensure `edition = "2021"` in both workspace and every member, then clean with `cargo clean` and retry.

## Tauri 2 Production Patterns

Use this section when building Tauri 2 desktop apps with React/TypeScript frontends on Windows.

> For a complete session-proven reference covering workspace inclusion, command organization, IPC constraints, async patterns, config schema, and esbuild postinstall — see [tauri2-build-patterns.md](references/tauri2-build-patterns.md).

### Scaffolding

On Windows, prefer npm-based scaffolding over cargo-based CLI install to avoid bundler dependency timeouts:

```bash
npm create tauri-app@latest <app-name> -- --packageManager npm --template react-ts --yes
cd <app-name>
npm install
npm install -D tailwindcss @tailwindcss/vite
npm install lucide-react framer-motion zustand @radix-ui/react-dialog @radix-ui/react-select @radix-ui/react-tabs @radix-ui/react-slider @radix-ui/react-progress @radix-ui/react-tooltip cmdk
```

### Rust Backend Module Layout

Use flat module files under `src-tauri/src/`, not nested subdirectories. Required module declarations in `src-tauri/src/lib.rs`:

```rust
mod drive;
mod ripper;
mod store;
mod types;
pub use drive::{DriveInfo, DriveScanner};
pub use ripper::RipEngine;
pub use store::RipStore;
```

Import types with explicit paths in each module file; avoid glob imports that can shadow names or create ambiguity.

### Windows Optical Drive Detection

`wmic logicaldisk` is unreliable for detecting optical drives. Use PowerShell `Win32_LogicalDisk` filtering for `DriveType = 5`:

```rust
fn detect_windows_drives() -> Vec<DriveInfo> {
    let output = Command::new("powershell")
        .args(["-Command", "Get-WmiObject Win32_LogicalDisk | Where-Object {$_.DriveType -eq 5} | Select-Object DeviceID, VolumeName, Size, DriveType | ConvertTo-Json"])
        .output()
        .ok();
    // Parse JSON output, filter for drive type 5
}
```

Always include Linux/macOS mount-path fallback for cross-platform compatibility.

### Frontend Tauri Integration

Use `@tauri-apps/api/core` for `invoke()` and `@tauri-apps/api/event` for event listeners:

```typescript
import { invoke } from "@tauri-apps/api/core";
import { listen } from "@tauri-apps/api/event";

// Call backend command
const result = await invoke<any>("list_drives");

// Listen for events
const unlisten = listen<Job>("job:update", (event) => {
  setJobs(prev => [...prev, event.payload]);
});
return () => { unlisten.then(fn => fn()); };
```

For a complete reference on frontend maturity patterns — error display, event-based progress, input validation, loading states, settings persistence, file logging, graceful shutdown, verification UI, and audio CD UI — see [tauri2-frontend-maturity.md](references/tauri2-frontend-maturity.md).

### Build Verification

Always verify both frontend and backend independently:

```bash
npm run build      # Frontend bundle only
cargo check        # Rust compile check
npm run tauri build  # Full release build + installers
```

Use `npm run tauri dev` only for interactive testing; for CI, use `npm run tauri build`.

### GUI Verification Workflow

When verifying a Tauri desktop app's UI:

1. Launch with `npm run tauri dev` and wait for window appearance.
2. Use accessibility/semantic capture to enumerate elements.
3. Click navigation elements by coordinates from accessibility bounds.
4. Re-capture after each navigation to verify view switching.
5. Verify empty states, error states, and action buttons render correctly.

### Packaging

Release artifacts are produced in `src-tauri/target/release/bundle/`:
- MSI: `bundle/msi/<app>_<version>_x64_en-US.msi`
- NSIS: `bundle/nsis/<app>_<version>_x64-setup.exe`
- EXE: `target/release/<app>.exe`

## When to Use

Use when building or modifying the VM-Harness desktop app (`C:/Projects/QEMU-MCP/gui/`) — a PyQt5 frameless window with sidebar navigation, panel stacking, background bridges, and mobile pairing.

## VM-Harness Desktop App Architecture

The VM-Harness desktop app (`C:/Projects/QEMU-MCP/gui/`) is a PyQt5 frameless window with sidebar navigation, panel stacking, background bridges, and mobile pairing.

### Project Structure
```
gui/
├── __init__.py            # Package init, path setup
├── __main__.py            # Entry point: sets Qt attrs, launches MainWindow
├── main_window.py         # Frameless window, sidebar, panel stack, bridges, tray
├── panels_pairing.py      # Mobile pairing + federation (QR, API keys, remote desktops)
├── panels_settings.py     # QEMU/VM/Network/Logging/Auth settings tabs
├── panels.py              # Dashboard panel (VM list, status cards)
├── panels_vm_control.py   # VM control (start/stop/restart/snapshot)
├── panels_guest_terminal.py  # SSH terminal to guest OS
├── panels_guest_agent.py  # Guest agent (file browser, process list)
├── panels_telemetry.py    # CPU/RAM/disk/network charts
├── qmp_bridge.py          # QMP protocol bridge (background thread → signals)
├── ssh_bridge.py          # SSH protocol bridge (background thread → signals)
├── theme.py               # Design tokens (T.TEXT_PRIMARY, T.WARNING, spacing, etc.)
└── widgets.py             # Reusable widgets (Card, TextInput, StatusIndicator, etc.)
```

### Frameless Window Pattern
```python
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint | Qt.WindowCloseButtonHint)
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)
        # Custom title bar with drag-to-move, min/max/close buttons
        # Sidebar (fixed 180px) + Panel stack (stretch factor 1)
        # Status bar at bottom
```

### Sidebar Navigation
```python
class Sidebar(QWidget):
    current_panel_changed = pyqtSignal(str)
    PANELS = [
        ("Dashboard", "📊", "dashboard"),
        ("VM Control", "🖥️", "vm_control"),
        ("Pairing", "🔗", "pairing"),
        # ... more panels
    ]
    # Fixed width 180px, buttons with emoji + label
```

### Panel Stack Pattern
```python
def _build_panels(self):
    panel_list = [
        (DashboardPanel, "dashboard"),
        (VMControlPanel, "vm_control"),
        (PairingPanel, "pairing"),
        # ... more panels
    ]
    for panel_cls, name in panel_list:
        panel = panel_cls(self)
        self.panels[name] = panel
        self.panel_stack.addWidget(panel)
    # Wire bridges AFTER all panels exist
    if "dashboard" in self.panels:
        self.panels["dashboard"].set_qmp_bridge(self.qmp_bridge)
    # ... more bridge wiring
```

### Background Bridge Pattern
```python
# QMP Bridge runs in background thread, emits signals
self.qmp_bridge = QMPBridge(settings=self.settings)
self.qmp_bridge.start()
self.qmp_bridge.connected.connect(self._on_qmp_connected)
self.qmp_bridge.vm_status.connect(self._on_vm_status)

# SSH Bridge similarly
self.ssh_bridge = SSHBridge(settings=self.settings)
self.ssh_bridge.start()
self.ssh_bridge.connected.connect(self._on_ssh_connected)
```

### System Tray Integration
```python
def _setup_system_tray(self):
    self.tray_icon = QSystemTrayIcon(self)
    # Create icon programmatically (QPainter → QPixmap)
    # Context menu: Show / Quit
    # closeEvent: minimize to tray instead of closing
```

### Pairing Panel (Mobile + Federation)
```python
class PairingPanel(QWidget):
    def set_server(self, server: QMCMApiServer):
        """Wire API server for token generation. MUST be called after init."""
        self._server = server
        self._generate_pairing()  # Generate QR + URI
        self._refresh_keys()      # List paired devices
    
    def _generate_pairing(self):
        token, payload, info = self._server.generate_pairing_token()
        uri = f"vmharness://pair?key={token}"
        # Generate QR code with qrcode library
        # Display in QLabel
```

### API Server Initialization
```python
def _init_api_server(self):
    """Initialize QMCMApiServer for pairing. Call AFTER _build_panels()."""
    from pathlib import Path
    from vm_mcp.api_server import QMCMApiServer, _load_or_generate_signing_key
    key_dir = Path(".")  # Signing key at project root
    signing_key = _load_or_generate_signing_key(key_dir)
    self._api_server = QMCMApiServer(
        host="0.0.0.0",
        port=8443,
        tailscale_only=False,
        signing_key_dir=key_dir,
    )
    # Wire to pairing panel
    if "pairing" in self.panels:
        self.panels["pairing"].set_server(self._api_server)
```

### Signing Key
- **File**: `.vmharness_signing_key` (32 raw Ed25519 bytes) at project root
- **Constant**: `_SIGNING_KEY_FILE = ".vmharness_signing_key"` in `vm_harness.api_server`
- **Load**: `_load_or_generate_signing_key(key_dir)` — reads raw bytes, generates if missing

**Pitfall — undefined variable in ProcessGuardian**: The `ProcessGuardian._start_primary()` method originally referenced an undefined `args` variable instead of `[sys.executable, self._main_script]`. Always verify subprocess.Popen calls have the command list defined before use.

**Pitfall — bare except clauses in headless_server.py**: The headless server has bare `except:` clauses that catch `SystemExit`/`KeyboardInterrupt`, preventing clean shutdown. Replace with `except Exception:` to allow system exceptions to propagate.

### Android Deep Link Scheme
- **Scheme**: `vmharness://pair?key=<token>` (was `qmcmcp://`)
- **Manifest**: Update `android:scheme="vmharness"` in `<data>` element
- **Kotlin**: Update `PairingTokenVerifier.tokenToUri()` and URI parsing
- **Package**: Rename `com.omarchy.qmcmcp` → `com.vmharness` across all Kotlin files
- **Shared prefs**: Rename `qmcmcp_paired_prefs` → `vmharness_paired_prefs`

### ADB Port Forwarding (Phone → Desktop)
```bash
# API server (headless_server.py on port 8443)
adb reverse tcp:8443 tcp:8443
# Streaming bridge (streaming_bridge.py on port 8445)
adb reverse tcp:8445 tcp:8445
```

### VM-Harness Pitfalls

1. **QMCMApiServer constructor is keyword-only** — `QMCMApiServer(host=..., port=..., tailscale_only=..., signing_key_dir=...)`. Passing `signing_key=` raises `TypeError`.

2. **PairingPanel.set_server() must be called** — Without it, `_generate_pairing()` fails with "Server not available". Always call after `_build_panels()`.

3. **Signing key filename must match constant** — If you rename the key file, update `_SIGNING_KEY_FILE` in `vm_mcp/api_server.py` or `_load_or_generate_signing_key()` will generate a new key, breaking existing pairings.

4. **Android package rename is pervasive** — `grep -rn 'com.omarchy.qmcmcp'` must return 0 after rename. Check: package declarations, import statements, AndroidManifest.xml, proguard-rules.pro, build.gradle.kts (namespace/applicationId), deep link scheme, shared prefs name.

5. **Panel wiring order** — Create ALL panels first, THEN wire bridges. Panels may reference bridges in their `__init__` if bridge is None.

6. **Fixed sidebar width** — Sidebar uses `setFixedWidth(180)`. This prevents scaling below ~1400px total width. Use `setMinimumSize(1200, 800)` on main window to prevent crush.

7. **System tray icon** — Create programmatically via `QPainter` → `QPixmap` → `QIcon`. Don't load from file (file may not exist in PyInstaller bundle).

8. **closeEvent minimize-to-tray** — Override `closeEvent` to `self.hide()` + `tray_icon.showMessage()` instead of `event.accept()`. Without this, closing the window terminates the app.

## Modular PyQt5 Architecture

For production-grade PyQt5 apps, avoid monolithic single-file designs. Use a modular package structure:

```
webbuilder/
  __init__.py
  core/
    __init__.py          # Config, Project, Page, Section, ProjectManager
    multi.py             # MultiPageProject, AssetManager, DeploymentManager
  gui/
    __init__.py          # Main window, chat panel, canvas, preview
  export/
    __init__.py          # HTML, React, Vue, JSON exporters
  ai/
    __init__.py          # Streaming AI client (OpenAI, Anthropic, Ollama)
  plugins/
    __init__.py          # Plugin base + built-in plugins
webbuilder_desktop.py    # Entry point (sets Qt attrs, then imports gui)
```

**Key patterns:**
- Entry point sets Qt attributes BEFORE gui imports
- Dataclasses for Project/Page/Section/Design with `to_dict()`/`from_dict()`
- Singleton Config with class-level INSTANCE
- QThread for background work (AI streaming, file I/O)
- Avoid circular imports: import multi.py at BOTTOM of core/__init__.py

See [modular-pyqt5-architecture.md](references/modular-pyqt5-architecture.md) for detailed patterns.

## Post-Quantum Crypto Readiness

For 100-year durability, WebBuilder includes a post-quantum crypto module with hybrid classical + PQ operations.

### Module: `webbuilder/security/post_quantum.py`

```python
from webbuilder.security.post_quantum import (
    kyber_keygen, kyber_encapsulate, kyber_decapsulate,
    dilithium_sign, dilithium_verify,
    hybrid_key_exchange, hybrid_sign, hybrid_verify,
    get_crypto_engine, CryptoEngine,
)
```

**Algorithms:**
- **Kyber-768**: Key Encapsulation Mechanism (KEM) based on Module-LWE
- **Dilithium-2**: Digital Signature Scheme based on Module-LWE
- **Hybrid**: Classical ECDH + PQ Kyber key exchange
- **CryptoEngine**: Algorithm agility — swap algorithms without changing the API

**Key generation:**
```python
pk, sk = kyber_keygen()  # Returns (public_key, private_key)
ciphertext, secret = kyber_encapsulate(pk)  # Encapsulate shared secret
shared = kyber_decapsulate(ciphertext, sk)  # Decapsulate shared secret
```

**Signatures:**
```python
pk, sk = dilithium_keygen()
sig = dilithium_sign(message, sk)
valid = dilithium_verify(message, sig, pk)  # True if valid
```

**Hybrid operations:**
```python
classical, pq, combined, pk_pq = hybrid_key_exchange()
classical_sig, pq_sig = hybrid_sign(message, sk_classical, sk_pq)
valid = hybrid_verify(message, classical_sig, pq_sig, pk_classical, pk_pq)
```

**CryptoEngine with algorithm agility:**
```python
engine = get_crypto_engine()
engine.list_algorithms()  # ['kyber768-dilithium2', 'kyber1024-dilithium3', 'classic-aes256-rsa4096']
engine.set_primary('kyber1024-dilithium3')
pub, priv = engine.generate_keypair()  # Uses primary algorithm
sig = engine.sign(message, priv, 'kyber768-dilithium2')  # Override algorithm
valid = engine.verify(message, sig, pub, 'kyber768-dilithium2')
```

**Pitfall**: The `CryptoEngine.generate_keypair()` returns `(pub, priv)` bytes, NOT nested tuples. For PQ algorithms, it returns the Dilithium key pair. For classical algorithms, it returns `(pub, priv)` where `pub = hashlib.sha256(priv).digest()`.

**Pitfall**: `dilithium_sign` embeds the public key in the signature (format: `pk || sig || commitment`). The commitment binds the signature to both the public key AND the message, preventing signature reuse across messages.

### Resilience Systems

WebBuilder includes production-grade resilience systems for stability, performance, and self-healing:

**BackupManager** (`webbuilder/backup/__init__.py`):
- Auto-backup with versioning and retention policy
- Integrity verification via SHA256 checksums
- Compression (gzip) for large backups
- `start_auto_backup(interval_seconds=300)` — periodic auto-backup timer

**SQLiteStorage** (`webbuilder/storage/__init__.py`):
- Structured storage with WAL mode for crash recovery
- Migration support via `MigrationSystem`

**MigrationSystem** (`webbuilder/migrations/__init__.py`):
- Versioned migrations with up/down/rollback/dry-run

**HealthMonitor** (`webbuilder/health/__init__.py`):
- System resource monitoring (CPU, memory, disk)
- Application health checks
- Alert thresholds with listener callbacks

**Watchdog** (`webbuilder/watchdog/__init__.py`):
- Process monitoring and auto-restart on crash
- Resource leak detection
- Restart rate limiting (max 5 restarts per 5-minute window)

**UpdateManager** (`webbuilder/update/__init__.py`):
- GitHub release checking
- Auto-update with rollback support

**Startup sequence**:
```
start → qt_init → exception_hook → stability_monitor → autosave_manager
→ retry_manager → circuit_breaker → resource_guard → state_manager
→ error_boundary → memory_guard → thread_safety → lazy_loader
→ cache_manager → async_executor → batch_processor → memory_pool
→ debouncer → throttler → parallel_executor → performance_profiler
→ connection_pool → lazy_init → resource_pool → compression_manager
→ incremental_updater → backup_manager → sqlite_storage
→ health_monitor → watchdog → logging → theme → project_manager
→ export_manager → scaling_init → autosave → memory_monitor
→ crash_recovery → setup_ui → setup_menu → new_project
→ autosave_timer → state_manager → complete → window_create
→ window_show ✅
```

## Trait-Based Swappable Abstractions

For 100-year durability and plugin architecture, WebBuilder uses a trait-based system for swappable components.

### Module: `webbuilder/abi.py`

```python
from webbuilder.abi import (
    Trait, TraitRegistry, TraitImplementation, get_trait_registry,
    register_trait, get_trait, create_trait, ComponentFactory,
    CompositeTrait, TraitValidator,
    AIProviderTrait, CryptoEngineTrait, MLModelTrait,
    UIRendererTrait, StorageBackendTrait, LoggingBackendTrait,
)
```

**Register a trait implementation:**
```python
registry = get_trait_registry()
impl = TraitImplementation(
    trait_name='webbuilder.abi.AIProviderTrait',
    implementation_name='my-ai-provider',
    version='1.0.0',
    factory=lambda: MyAIProvider(),
    priority=10,
    metadata={'provider': 'my-ai', 'type': 'ai'}
)
registry.register(impl.trait_name, impl)
```

**Create a component by trait:**
```python
factory = ComponentFactory()
provider = factory.create('webbuilder.abi.AIProviderTrait', 'my-ai-provider')
result = provider.generate('Hello, world!')
```

**Trait definitions:**
- `AIProviderTrait`: `generate(prompt, **kwargs)`, `list_models()`
- `CryptoEngineTrait`: `sign(message, private_key)`, `verify(message, signature, public_key)`
- `MLModelTrait`: `predict(data)`, `train(data, labels)`, `export(path)`
- `UIRendererTrait`: `render(component)`, `resize(component, width, height)`
- `StorageBackendTrait`: `save(key, data)`, `load(key)`, `delete(key)`
- `LoggingBackendTrait`: `log(level, message, **kwargs)`, `flush()`

**Trait composition:**
```python
composite = CompositeTrait()
composite.add_trait('ai', ai_provider)
composite.add_trait('crypto', crypto_engine)
info = composite.trait_info()  # Includes all sub-traits
```

**Pitfall**: Trait implementations must satisfy the trait's abstract methods. Use `TraitValidator.validate(implementation, trait_class)` to check before registering.

**Pitfall**: The `TraitRegistry.create()` method raises `ValueError` if no implementation is found for a trait. Always check `registry.get(trait_name)` before calling `create()`, or provide a fallback via `ComponentFactory.set_fallback()`.

## Self-Learning ML Pipeline

For models that improve from usage, WebBuilder includes a self-learning pipeline that records interactions and periodically retrains models.

### Module: `webbuilder/ml_engine/self_learning.py`

```python
from webbuilder.ml_engine.self_learning import (
    SelfLearningPipeline, InteractionRecorder, RetrainScheduler,
    OnlineLearner,
)
```

**Create a self-learning pipeline:**
```python
pipeline = SelfLearningPipeline(model=model, min_interactions=10, retrain_interval=100)
pipeline.record_interaction(model_id, input_data, output_data, feedback=1.0)
should_retrain, metrics = pipeline.check_retrain()
if should_retrain:
    pipeline.retrain()
    pipeline.save()
```

**Interaction recording:**
```python
recorder = InteractionRecorder(pipeline_dir='data/interactions')
recorder.record(model_id, input_data, output_data, feedback=1.0)
interactions = recorder.load(model_id)
```

**Retrain scheduling:**
```python
scheduler = RetrainScheduler(pipeline, min_interactions=10, retrain_interval=100)
should_retrain, reason = scheduler.should_retrain(interaction_count=150, last_retrain_epoch=10)
```

**Integration with TrainingDashboard:**
```python
# TrainingDashboard records interactions after each training run
# SelfLearningPipeline.check_retrain() is called after each training epoch
# If enough interactions have been collected, the model is retrained
```

**Pitfall**: The self-learning pipeline records interactions from user actions, not from training. Training generates the model, and the pipeline records when the model is used and what the feedback is.

**Pitfall**: `SelfLearningPipeline.check_retrain()` returns `(should_retrain: bool, metrics: dict)`. If `should_retrain` is True, call `pipeline.retrain()` to retrain the model with the collected interactions.

## GUI Integration — Settings, Terminal, Activity Log

### Settings Button Pattern

For a dedicated Settings button (not just a menu item), add it to the Tools menu with a keyboard shortcut:

```python
# In webbuilder/gui/__init__.py setup_menu()
tools_menu = menubar.addMenu("🔧 Tools")
settings_action = QAction("⚙ Settings...", self)
settings_action.setShortcut("Ctrl+,")
settings_action.triggered.connect(self.open_settings)
tools_menu.addAction(settings_action)
```

**Pitfall**: The Settings dialog must be a standalone QDialog, not embedded in the main window. User explicitly rejected Chat in side panel — same principle applies to Settings.

### Terminal CLI with WebBuilder Commands

TerminalCLI supports both shell commands AND WebBuilder-specific commands via AgentCommandParser:

```python
from webbuilder.generative_ui import AgentCommandParser
from webbuilder.command import CommandRegistry

registry = CommandRegistry()
parser = AgentCommandParser(registry)
mutations = parser.parse(user_input)
for mutation in mutations:
    result = canvas.apply_mutation(mutation)  # ADD/REMOVE/UPDATE/MOVE/REPLACE/STYLE
```

**WebBuilder commands:**
- `add section <type>` — Add a new section to the canvas
- `remove section <id>` — Remove a section from the canvas
- `update section <id> <prop>=<value>` — Update a section property
- `move section <id> <x> <y>` — Move a section to new position
- `replace section <old_id> <new_type>` — Replace a section with a new type
- `style section <id> <property>=<value>` — Apply CSS style to a section

**Pitfall**: `Mutation.type` is a string, not an enum — use `mutation.type.upper()` not `mutation.type.value.upper()`. Using `.value` causes `AttributeError`.

### Activity Log Tab

ActivityLog captures all `webbuilder.*` logging via `_TerminalActivityHandler`:

```python
from webbuilder.gui.activity_log import ActivityTab

activity_tab = ActivityTab()
# Connect to logging handler
handler = _TerminalActivityHandler(terminal_cli, activity_tab)
logging.getLogger("webbuilder").addHandler(handler)
```

**Features:**
- Filter by log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Search by keyword
- Copy selected entries
- Save to file
- Export as JSON

**Pitfall**: The logging handler must be set up AFTER the terminal and activity tab are initialized. Use `QTimer.singleShot` to defer handler setup if needed.

### ChatWindow Snap-In/Snap-Out

ChatWindow and PropertiesWindow are standalone floating windows that can snap into the main window.

**Centralized SnapState pattern (CRITICAL):**
- NEVER use per-window `_is_snapped` flags — they desync and cause windows to not snap/unsnap
- ALWAYS use `SnapState` singleton from `webbuilder/gui/snap_system.py` for all snap state management
- Both ChatWindow and PropertiesWindow use `_snap_state: SnapState` instance
- Main window delegates snap/unsnap to `SnapState` via `handle_chat_snap_request()` and `handle_properties_snap_request()`
- `SnapState.snap_to(window, main_window)` — handles all dock widget creation and placement
- `SnapState.unsnap_from(window)` — handles all cleanup and window restoration
- `SnapState.toggle(window)` — toggle snap state
- `SnapState.snapped_changed` signal — notify listeners of state changes
- `AnimatedSnapMixin` — smooth fade/slide animations for snap/unsnap

### SnapState CLASS-LEVEL Reference

**Class:** `SnapState` — `webbuilder/gui/snap_system.py`
**Purpose:** Centralized snap/unsnap state management for Chat and Properties floating windows
**Singleton:** `get_snap_state()` — always use the singleton, never create multiple instances

**Methods:**
- `snap_to(window, main_window)` — Dock window into main window's right splitter
- `unsnap_from(window)` — Undock window back to floating standalone window
- `toggle(window)` — Toggle snap/unsnap state
- `is_snapped(window)` — Check if window is currently snapped

**Signals:**
- `snapped_changed` — Emitted when any window's snap state changes

**Usage:**
```python
from webbuilder.gui.snap_system import SnapState

class ChatWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._snap_state = SnapState()  # Centralized snap state
```

**Pitfall:** When rewriting ChatWindow/PropertiesWindow, the `SnapState` singleton MUST be preserved. Dropping it breaks all snap state across both windows.

**Pitfall:** `setAnimated(True)` on QDockWidget raises `AttributeError` — it does not exist in PyQt5. Use `AnimatedSnapMixin` for animations instead.

**CRITICAL — Preserve factory functions on rewrite:** When rewriting the tail of `chat_window.py` (or any module with a `get_*_window()` factory + `_*_window` singleton), the factory and singleton MUST survive the rewrite. Dropping them breaks any test or call site that imports `get_chat_window` — the error is `ImportError: cannot import name 'get_chat_window'`. Always `grep` the module for `def get_` and the singleton name before and after a rewrite, and run `py_compile` on all three GUI files (`chat_window.py`, `properties_window.py`, `__init__.py`) before rebuilding.

**Dock widget animation pitfall**: `setAnimated(True)` was removed from ChatDockWidget and PropertiesDockWidget — it causes AttributeError. The SnapState class handles animations via `AnimatedSnapMixin` instead.

## Self-Healing & Resilience Architecture

For production GUIs that must never go down, implement a layered resilience system:

### Atomic State Manager

Use write-ahead logging (WAL) for all state changes — log before commit, then atomically rename temp file to final path. On crash, recover from the WAL.

```python
import json, os, tempfile, time
from pathlib import Path

class AtomicState:
    """Atomic state with write-ahead logging and snapshots."""

    def __init__(self, state_dir: Path):
        self.state_dir = state_dir
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.wal_path = state_dir / "state.wal"
        self.state_path = state_dir / "state.json"
        self.snapshots_dir = state_dir / "snapshots"
        self.snapshots_dir.mkdir(exist_ok=True)

    def commit(self, state: dict):
        # Write to WAL first
        with open(self.wal_path, 'w') as f:
            json.dump(state, f, indent=2)
        # Atomic rename
        tmp = self.state_path.with_suffix('.tmp')
        with open(tmp, 'w') as f:
            json.dump(state, f, indent=2)
        os.replace(tmp, self.state_path)
        # Clear WAL after successful commit
        if self.wal_path.exists():
            self.wal_path.unlink()

    def recover(self) -> dict | None:
        # Check WAL first (crash recovery)
        if self.wal_path.exists():
            try:
                with open(self.wal_path) as f:
                    state = json.load(f)
                self.commit(state)  # replay
                return state
            except Exception:
                pass
        # Fall back to last snapshot
        snapshots = sorted(self.snapshots_dir.glob("*.json"), reverse=True)
        if snapshots:
            with open(snapshots[0]) as f:
                return json.load(f)
        return None

    def create_snapshot(self, name: str):
        dest = self.snapshots_dir / f"{name}.json"
        if self.state_path.exists():
            import shutil
            shutil.copy2(self.state_path, dest)

    def restore_snapshot(self, name: str) -> dict | None:
        src = self.snapshots_dir / f"{name}.json"
        if src.exists():
            with open(src) as f:
                state = json.load(f)
            self.commit(state)
            return state
        return None
```

**Pitfall**: Never write directly to the state file — always use `commit()` which goes through the WAL. Direct writes lose crash safety.

### Process Guardian (Primary + Backup)

Run a backup instance in standby that is instantly promoted when the primary crashes. The backup pre-initializes all panels and connections, then waits for promotion.

```python
import subprocess, sys, time, signal
from pathlib import Path

class ProcessGuardian:
    """Monitors primary process, promotes backup on crash."""

    MAX_RESTARTS = 10
    WINDOW_SECONDS = 60

    def __init__(self, script_path: Path, state_dir: Path):
        self.script_path = script_path
        self.state_dir = state_dir
        self.primary_pid: int | None = None
        self.backup_pid: int | None = None
        self.restart_log: list[float] = []

    def start_primary(self):
        proc = subprocess.Popen(
            [sys.executable, str(self.script_path), "--primary"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        self.primary_pid = proc.pid
        return proc

    def start_backup(self):
        proc = subprocess.Popen(
            [sys.executable, str(self.script_path), "--standby"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        self.backup_pid = proc.pid
        return proc

    def can_restart(self) -> bool:
        now = time.time()
        self.restart_log = [t for t in self.restart_log if now - t < self.WINDOW_SECONDS]
        return len(self.restart_log) < self.MAX_RESTARTS

    def run_forever(self):
        while True:
            self.start_backup()
            proc = self.start_primary()
            proc.wait()
            exit_code = proc.returncode
            if exit_code == 0:
                break  # clean exit
            if not self.can_restart():
                break  # rate limit hit
            self.restart_log.append(time.time())
            # Promote backup to primary
            if self.backup_pid:
                # Signal backup to take over window
                pass
```

### Hot Reload

Watch source files for changes. On change, save state → reload module → restore state.

```python
from PyQt5.QtCore import QFileSystemWatcher, QTimer
import importlib

class HotReloader:
    def __init__(self, module_paths: list[Path], reload_fn):
        self.watcher = QFileSystemWatcher([str(p) for p in module_paths])
        self.watcher.fileChanged.connect(self._on_file_changed)
        self.reload_fn = reload_fn
        self._debounce = QTimer()
        self._debounce.setSingleShot(True)
        self._debounce.setInterval(500)
        self._debounce.timeout.connect(self._do_reload)

    def _on_file_changed(self, path: str):
        self._debounce.start()

    def _do_reload(self):
        state = self.reload_fn.__self__.save_state()
        for module_path in self.watcher.files():
            module_name = module_path.stem
            if module_name in sys.modules:
                importlib.reload(sys.modules[module_name])
        self.reload_fn.__self__.restore_state(state)
```

**Pitfall**: Qt widgets cannot be hot-reloaded directly — the reload must reconstruct widgets from state, not pickle QObjects.

### Deep Wiring Audit

After adding panels or modifying signal-slot connections, always run a structural audit:

```python
def audit_wiring():
    """Check every panel's bridge connections and method signatures."""
    issues = []
    for panel in window.panels:
        # Check bridge wiring
        if hasattr(panel, 'set_qmp_bridge'):
            # Verify the bridge is actually set
            bridge_attr = getattr(panel, '_qmp_bridge', None)
            if bridge_attr is None:
                issues.append(f"{panel.__class__.__name__}: qmp_bridge not set")
        # Check signal connections via introspection
        for attr_name in dir(panel):
            attr = getattr(panel, attr_name)
            if callable(attr) and attr_name.startswith('_on_'):
                # Verify the signal exists on the connected object
                pass
    return issues
```

**Workflow**: After every panel addition or API change, grep for all `connect(` calls and verify the slot method exists with the correct signature.

### Auto-Update Tests When Adding Panels

When adding a new panel to the sidebar, the `test_main_window_constructs` assertion `len(win.panels) == N` must be updated. Always check the test file after panel changes:

```bash
grep -n "assert.*panels.*==" tests/test_gui.py
```

## Zero-Tolerance Policy for Incomplete Work

**Rule**: There can be no errors, issues, bugs, placeholders, stubs, warnings, etc. Every aspect must be 100% fully built out and properly wired.

### Pass Stub Elimination

ALL `pass` statements in method bodies must be replaced with proper implementations:

1. **Exception handlers**: Replace `except Exception: pass` with `except Exception as e: logger.warning(f"Context: {e}")`
2. **Method stubs**: Replace `pass` with either a proper implementation or a `raise NotImplementedError(f"{self.__class__.__name__}.{method_name} not implemented")`
3. **Abstract methods**: Keep `pass` ONLY in `@abstractmethod` definitions (these are intentional interfaces)
4. **Fallback class definitions**: `pass` in `except ImportError` fallback classes is acceptable (these are no-op stubs for when PyQt5 is not available)

### TODO Elimination

ALL TODO comments must be resolved:
1. Replace with proper implementation
2. Replace with logging if the feature is intentionally deferred
3. Replace with `raise NotImplementedError` if the feature is not yet implemented

### Silent Exception Swallowing Elimination

ALL silent exception swallowing must be replaced with logging:
1. `except Exception: pass` → `except Exception as e: logger.warning(f"Context: {e}")`
2. `except ImportError: pass` → `except ImportError: logger.debug("Optional module not available")`
3. `except json.JSONDecodeError: pass` → `except json.JSONDecodeError as e: logger.debug(f"JSON parse error: {e}")`

**Pitfall**: The user explicitly rejected "There can be no errors, issues, bugs, placeholders, stubs, warnings, etc." This is a standing policy, not a one-time request. Every `pass` stub, TODO comment, and silent exception swallowing must be eliminated.

## AI Streaming Integration

Real streaming AI chat with async chunked responses:

```python
class StreamThread(QThread):
    chunk_received = pyqtSignal(str)
    finished = pyqtSignal(object)

    def run(self):
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        async def stream():
            async for chunk in self.ai_client.stream_chat(...):
                if chunk.content:
                    self.chunk_received.emit(chunk.content)
                if chunk.done:
                    self.finished.emit(chunk.error)
                    return
        loop.run_until_complete(stream())
        loop.close()
```

Supports OpenAI (SSE), Anthropic (SSE), and Ollama (NDJSON) streaming protocols.

## Multi-Project Export

Export projects to multiple formats:
- **HTML**: Standalone files with embedded CSS, responsive design
- **React**: Component-based export with individual .js files
- **Vue**: Single-file component export
- **JSON**: Structured project data

## Deployment Integration

Generate deployment configs for Vercel (`vercel.json`), Netlify (`netlify.toml`), and Cloudflare Pages (`wrangler.toml`).

## Plugin System

Extensible plugin architecture with:
- Base Plugin class with lifecycle hooks (initialize, shutdown)
- Hook system (on_project_created, on_section_added, on_export, etc.)
- Built-in plugins: SEO Analyzer, Analytics Tracker, Accessibility Checker
- Plugin discovery from `~/.webbuilder/plugins/` directory

## Related Skills

- `agentic-platform-development` - Web platform and MCP server
- `mcp-server-development` - MCP server patterns
- `rust-native-development` - Rust native: deterministic engines, Tauri, WASM plugins
- `webbuilder-desktop-app` - WebBuilder-specific patterns (PyQt5 web builder with AI chat)

## 100-Year Architecture Principles

For desktop apps meant to evolve for decades:

1. **Zero dependencies in core**: The core logic must depend ONLY on language standard library. GUI frameworks change, but core logic should survive.

2. **Everything is a plugin**: Features beyond core are plugins. Plugins can be added, removed, or replaced without touching the core.

3. **Open, human-readable formats**: Native storage uses open formats (JSON with schema versioning). Every object has `_schema` and `_version` fields.

4. **Self-describing data**: All models implement `to_dict()` and `from_dict()` with schema identifiers.

5. **Composability over monoliths**: Small, focused tools that compose.

6. **Deterministic behavior**: Same input → same output.

7. **Community governance**: The platform should be governable by its community.

### Parallel Codebase Buildout

When the user demands exhaustive scope, spawn parallel `delegate_task` subagents for independent code streams. After ALL subagents complete, run import checks on every package — cross-cutting type aliases (`VMDisplayType = DisplayType`) and empty `__init__.py` files are common failure modes. See `references/parallel-codebase-buildout.md`.

### Simplification Workflow

When the codebase grows too large:

1. **Identify core vs contrib**: Core = what's needed for Create → Edit → Export. Everything else = contrib.
2. **Move to contrib/**: Relocate non-core modules to a `contrib/` directory.
3. **Update imports**: Change `from webbuilder.module` to `from webbuilder.contrib.module`.
4. **Verify core still works**: Run integration tests after each move.
5. **Contrib modules remain accessible**: They're just not loaded by default.

## Verification Workflow

After every major change:

1. **Test core workflow end-to-end**: Create → Save → Load → Export → Verify output.
2. **Run integration tests**: Full workflow tests that verify the whole system works together.
3. **Verify GUI launches**: Check all tabs render, no import errors.
4. **Check for import errors**: Import all modules to catch missing dependencies.

## Crash Debugging Pattern

When a PyQt5 exe crashes on launch (no GUI appears, black screen, invisible error):

1. **Add crash stages** to `WebBuilderWindow.__init__` and `main()` — write each init step to `logs/crashes/early_crash_*.txt`. The stage that doesn't appear is where the crash happens.

2. **Check for blocking dialogs** — `QMessageBox.question()` in startup code hangs indefinitely in headless/auto mode. Auto-recover without prompting.

3. **Write crash reports to files** — never rely on dialogs for crash output. Write to `logs/crashes/crash_*.txt` with full traceback, local vars, system info.

4. **Ensure GUI visibility** — after `window.show()`, call `showMaximized()`, `raise_()`, `activateWindow()`, `setFocus()`.

5. **Rebuild with console** — remove `--windowed` from PyInstaller to see crash output directly.

See [webbuilder-bug-fixes-2026-09.md](references/webbuilder-bug-fixes-2026-09.md) for the full list of session-proven bug fixes including crash debugging patterns (items #26-#29).

## WebBuilder Bug Fixes (September 2026)

For session-proven bug fixes and API signature references discovered during WebBuilder development, see [webbuilder-bug-fixes-2026-09.md](references/webbuilder-bug-fixes-2026-09.md).

Covers:
- GUI launch bugs (setup_logging signature, CrashRecovery attribute, MemoryMonitor import, Qt DPI)
- Test suite API signature mismatches (FormBuilder, ProjectSearch, CustomCode, SEO, Analytics, ImportExport)
- Module extraction pitfalls (duplicate definitions, missing files, backward-compat aliases)
- Build system notes (PyInstaller, Flask backend)
- Import mismatches (importing non-existent names from __init__.py)
- Form validation before submit pitfall

## WebBuilder Module Ecosystem

For the complete inventory of all 135+ modules built across the September 2026 sessions, see [webbuilder-modules-2026-09.md](references/webbuilder-modules-2026-09.md).

Covers:
- Module inventory with paths and purposes
- Scale metrics (135 modules, 20,000+ LOC, 183 tests)
- All pitfalls discovered during development
- Build commands and test suite reference

## GUI Integration Workflow

When backend modules are built but not yet wired into the GUI, follow this integration pattern:

### Step 1: Create the Panel Widget

```python
# webbuilder/gui/my_module_panel.py
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDialog, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QPushButton, QLabel, QLineEdit, QTextEdit, QTableWidget,
    QTableWidgetItem, QHeaderView, QComboBox, QSpinBox,
    QCheckBox, QFormLayout, QGroupBox, QFileDialog, QMessageBox,
    QInputDialog, QScrollArea, QFrame, QSplitter,
)
from webbuilder.my_module import get_my_module

class MyModulePanel(QWidget):
    """Integrated panel for my_module."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.module = get_my_module()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        # Header with controls
        # Main content area
        # Bottom actions
```

### Step 2: Register Menu Items in Main Window

```python
# In webbuilder/gui/__init__.py setup_menu()
my_action = QAction("My Feature...", self)
my_action.triggered.connect(self.open_my_feature)
tools_menu.addAction(my_action)
```

### Step 3: Add Handler Method

```python
# In webbuilder/gui/__init__.py WebBuilderWindow class
def open_my_feature(self):
    """Open my feature dialog."""
    try:
        dialog = MyFeatureDialog(self)
        dialog.show()  # Use show() not exec_() to prevent event loop blocking
    except Exception as e:
        logger.error(f"My feature failed: {e}")
        QMessageBox.warning(self, "Error", f"Failed: {e}")
```

### Step 4: Import at Top of Main Window

```python
from webbuilder.gui.my_feature_dialog import MyFeatureDialog
```

### Settings Window Pattern

For a proper settings window (not scattered menu items):

```python
class SettingsDialog(QDialog):
    """Dedicated settings window with tabs."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setMinimumSize(700, 500)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        tabs = QTabWidget()
        tabs.addTab(self.create_appearance_tab(), "Appearance")
        tabs.addTab(self.create_ai_tab(), "AI Providers")
        tabs.addTab(self.create_editor_tab(), "Editor")
        tabs.addTab(self.create_export_tab(), "Export")
        tabs.addTab(self.create_plugins_tab(), "Plugins")
        tabs.addTab(self.create_about_tab(), "About")
        layout.addWidget(tabs)
```

### Command Palette Pattern

```python
class CommandPaletteDialog(QDialog):
    """VS Code-style command palette (Ctrl+Shift+P)."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.registry = get_command_registry()
        self.setWindowTitle("Command Palette")
        self.setMinimumSize(500, 400)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setup_ui()
```

### Unified Modules Panel Pattern

For exposing ALL backend modules through one dialog:

```python
class ModulesDialog(QDialog):
    """Dialog with tabs for all backend modules."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Modules")
        self.setMinimumSize(800, 600)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        tabs = QTabWidget()
        tabs.addTab(FormBuilderPanel(self), "Forms")
        tabs.addTab(ABTestingPanel(self), "A/B Testing")
        tabs.addTab(AssetManagerPanel(self), "Assets")
        tabs.addTab(VersionHistoryPanel(self), "History")
        tabs.addTab(ResponsivePanel(self), "Responsive")
        tabs.addTab(CSSEditorPanel(self), "CSS")
        layout.addWidget(tabs)
```

## Design Token-Based Theme System

For production-grade visual consistency:

```python
@dataclass
class ColorToken:
    name: str = ""
    light: str = "#000000"
    dark: str = "#ffffff"
    
    def get(self, is_dark: bool = True) -> str:
        return self.dark if is_dark else self.light

class QSSGenerator:
    """Generate Qt Stylesheets from design tokens."""
    
    def __init__(self, tokens: DesignTokenSystem):
        self.tokens = tokens
    
    def generate(self) -> str:
        # Generate QSS for all widget types using tokens
        # Returns complete stylesheet string
```

## PyInstaller Build Pattern for WebBuilder

```bash
pyinstaller --name "WebBuilder" --onefile --windowed \
  --exclude-module matplotlib --exclude-module numpy \
  --exclude-module pandas --exclude-module scipy \
  --exclude-module tkinter --exclude-module unittest \
  --exclude-module pytest --exclude-module setuptools \
  --exclude-module pip --exclude-module wheel \
  --add-data "webbuilder;webbuilder" \
  webbuilder_desktop.py
```

**Pitfall**: Must `taskkill /F /IM WebBuilder.exe` before rebuilding — PyInstaller fails with `PermissionError: [WinError 5] Access is denied` if the exe is running.

**Pitfall**: Exclude heavy modules (matplotlib, numpy, pandas, scipy, tkinter, unittest, pytest, setuptools, pip, wheel) to reduce size from ~133MB to ~128MB.

**Pitfall**: When importing from a subpackage into `gui/__init__.py`, verify all names exist in that subpackage's `__init__.py`. A name defined in a module file but not re-exported by `__init__.py` works in source but fails in PyInstaller-frozen exe. Check with `python -c "from webbuilder.<pkg> import <Name>"` before committing.

### Logging Handler Pattern — Route Python Logs to GUI Widgets

When building Terminal CLI or Activity Log widgets, route Python `logging` output to them with a custom handler:

```python
class _TerminalActivityHandler(logging.Handler):
    """Logging handler that routes messages to TerminalCLI and ActivityTab."""
    
    def __init__(self, terminal_cli, activity_tab):
        super().__init__()
        self.setLevel(logging.DEBUG)
        self._terminal = terminal_cli
        self._activity = activity_tab
        self._level_map = {
            logging.DEBUG: "debug",
            logging.INFO: "info",
            logging.WARNING: "warning",
            logging.ERROR: "error",
            logging.CRITICAL: "error",
        }
    
    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = self._level_map.get(record.levelno, "info")
            source = record.name.replace("webbuilder.", "")
            message = self.format(record)
            if self._terminal:
                self._terminal.append_line(message, level)
            if self._activity:
                self._activity.add_log(message, level, source)
        except Exception:
            pass
```

**Pitfall**: The segfault during `WebBuilderWindow()` creation in offscreen mode is caused by Qt widget creation (especially WebEngine/QWebEngineView), NOT by the logging handler. The handler setup is safe to call during `__init__` — but deferring it with `QTimer.singleShot` is still best practice since early log messages before handler setup are not captured.

**Fix**: Defer handler setup with `QTimer.singleShot`:
```python
# In WebBuilderWindow.__init__:
self.activity_tab = ActivityTab()
self.terminal_cli = TerminalCLI()
# ... other init ...
QTimer.singleShot(100, self._setup_logging_handler)

def _setup_logging_handler(self) -> None:
    """Set up logging handler after window is fully initialized."""
    try:
        if hasattr(self, 'terminal_cli') and hasattr(self, 'activity_tab'):
            self._terminal_handler = _TerminalActivityHandler(
                self.terminal_cli, self.activity_tab
            )
            logging.getLogger("webbuilder").addHandler(self._terminal_handler)
    except Exception:
        pass
```

**Prevention**: Offscreen mode segfaults come from Qt widget creation, not logging handlers. If `WebBuilderWindow()` crashes in offscreen mode, the crash is in widget init (typically WebEngine), not in the logging handler. Use `QT_QPA_PLATFORM=windows` on Windows for real GUI testing.

### PyInstaller Rebuild Pattern

When source changes don't take effect in the frozen exe (stale bundle):

```bash
# 1. Kill ALL running WebBuilder processes
pkill -9 -f WebBuilder

# 2. Clean build artifacts (NOT just dist/ — PyInstaller caches in build/)
rm -rf build dist *.spec

# 3. Rebuild
pyinstaller --name "WebBuilder" --onefile --windowed \
  --exclude-module matplotlib --exclude-module numpy \
  --exclude-module pandas --exclude-module scipy \
  --exclude-module tkinter --exclude-module unittest \
  --exclude-module pytest --exclude-module setuptools \
  --exclude-module pip --exclude-module wheel \
  --add-data "webbuilder;webbuilder" \
  webbuilder_desktop.py
```

**Pitfall**: Simply re-running PyInstaller without `rm -rf build dist *.spec` produces a stale bundle with old code. The `build/` directory contains extracted PyInstaller cache that isn't cleared by `--clean` alone.

**Pitfall**: On Windows, PyInstaller fails with `PermissionError: [WinError 5] Access is denied` if WebBuilder.exe is running. Must `taskkill /F /IM WebBuilder.exe` first.

**Verification**: After rebuild, check the timestamp of `dist/WebBuilder.exe` matches the build time, not a previous build.

## Test Fixture Pattern for Form Builders

When tests submit form data, use field IDs as keys (not labels):

```python
# Correct: use field.id as key
name_field = form.fields[0]
data = {name_field.id: "John", email_field.id: "john@example.com"}

# Wrong: using label as key
data = {"Name": "John"}  # Won't match field validation
```

### WebBuilder CLI Command Pattern (TerminalCLI)

TerminalCLI parses user input through `AgentCommandParser` before falling back to shell. The public `execute_webbuilder_command()` method is redundant — use `_try_webbuilder_command()` internally which returns `(matched: bool, output: str)`.

```python
# In TerminalCLI._try_webbuilder_command():
parser = AgentCommandParser(registry)
mutations = parser.parse(user_input)
if mutations:
    for mutation in mutations:
        result = canvas.apply_mutation(mutation)  # ADD/REMOVE/UPDATE/MOVE/REPLACE/STYLE
        output += f"  ✅ {mutation.type}: {mutation.target_id}\n"
    return True, output
return False, ""  # Fall through to shell
```

**Pitfall**: `Mutation.type` is a string, not an enum — use `mutation.type.upper()` not `mutation.type.value.upper()`. Using `.value` causes `AttributeError`.

**Pitfall**: `target_id == "canvas"` only makes sense for ADD mutations. REMOVE/UPDATE/MOVE on `canvas` has no matching section — guard against it:
```python
if mutation.type == "ADD":
    # create new section on canvas
elif mutation.target_id == "canvas":
    # skip — canvas is not a section, no matching widget to modify
```

### ML Training Dashboard

`TrainingDashboard` widget shows 7 NumPy ML models with status indicators, train/retrain buttons, epoch progress bars, loss/accuracy charts, and JSON export. Integrated as 🧠 ML tab in center tabs.

```python
# Model status check
from webbuilder.ml_engine.models import MLModelFactory
model = MLModelFactory.create(model_id)
exists = model.model_exists()  # Check for pre-trained weights
trained = model.is_trained()

# Train with progress tracking
model.train(X, y, epochs=50, progress_callback=update_bar)

# Export predictions
model.export_predictions(path, format="json")
```

**Pitfall**: Only 2 of 7 models have pre-trained weights (MLP, LogisticRegression). Training from scratch requires proper train/test split and feature scaling — the dashboard handles this automatically.

### Section.icon Attribute

`SectionWidget` renders `self.section.icon` (defaults to 📦 emoji). The `Section` dataclass must have `icon: str = ""` field — adding widgets via mutation before this field exists causes `AttributeError`.

```python
# In core/__init__.py Section dataclass:
@dataclass
class Section:
    id: str
    type: str
    title: str = ""
    icon: str = ""  # REQUIRED for SectionWidget compatibility
    props: dict = field(default_factory=dict)
```

### ChatWindow Model Fetching

Standalone ChatWindow must call `_fetch_models()` to populate the model selector from live provider APIs. Add at end of `setup_ui()`:

```python
QTimer.singleShot(500, self._fetch_models)

# In ChatWindow:
def _fetch_models(self):
    """Fetch real available models from all providers."""
    try:
        router = get_router()
        models = router.get_all_models()
        self.model_combo.clear()
        for provider_id, provider_models in models.items():
            for m in provider_models:
                self.model_combo.addItem(
                    f"{m['name']} ({provider_id})", m['id']
                )
    except Exception as e:
        logger.error(f"Model fetch failed: {e}")
```

### Offscreen Mode — Pre-existing QtWebEngine Segfault

`QT_QPA_PLATFORM=offscreen` crashes during `WebBuilderWindow()` creation due to QtWebEngine initialization. This is a known environment limitation — NOT a code defect. The Windows `.exe` build works fine.

**Do not waste time debugging offscreen crashes.** Test GUI changes via the PyInstaller exe on the actual desktop.

**Verification**: Use `QT_QPA_PLATFORM=windows` on Windows for real GUI testing. Offscreen is only for compile-checking imports.

## Test Fixture Pattern for Form Builders

When tests submit form data, use field IDs as keys (not labels):

```python
# Correct: use field.id as key
name_field = form.fields[0]
data = {name_field.id: "John", email_field.id: "john@example.com"}

# Wrong: using label as key
data = {"Name": "John"}  # Won't match field validation
```

## WebBuilder Bug Fixes

For session-proven bug fixes and API signature references discovered during WebBuilder development, see [webbuilder-bug-fixes-2026-09.md](references/webbuilder-bug-fixes-2026-09.md).

Covers:
- GUI launch bugs (setup_logging signature, CrashRecovery attribute, MemoryMonitor import, Qt DPI)
- Test suite API signature mismatches (FormBuilder, ProjectSearch, CustomCode, SEO, Analytics, ImportExport)
- Module extraction pitfalls (duplicate definitions, missing files, backward-compat aliases)
- Build system notes (PyInstaller, Flask backend)
