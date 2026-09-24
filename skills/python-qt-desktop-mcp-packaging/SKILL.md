---
name: python-qt-desktop-mcp-packaging
description: Build PyQt6 desktop apps with MCP backend as Windows EXE.
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [pyqt6, mcp, packaging, pyinstaller, windows]
---

# PyQt6 Desktop + MCP Packaging

Build native PyQt6 desktop apps with a Rust MCP backend, test with pytest-qt, package as standalone Windows EXE.

## Trigger

- PyQt6 GUI + Rust MCP (JSON-RPC) backend
- Target: standalone Windows .exe
- "Proceed with all" = implement immediately, verify, commit, push, NEVER plan-only

## 1. Project Structure

```
frontend/pyqt/
  main.py          # QMainWindow + all pages
  mcp_client.py    # JSON-RPC client (urllib)
  chat_store.py    # SQLite persistence
  config_store.py  # TOML settings persistence
  launcher.py      # Server + GUI subprocess manager
src-tauri/src/
  mcp.rs           # handle_jsonrpc, EngineToolHost
  server.rs        # Binary entry point
tests/
  conftest.py      # qapp, mock_mcp, mcp_server fixtures
  test_gui.py      # Per-page instantiation tests
  test_main_app.py # MainWindow + navigation + stores
  test_chat_persistence.py, test_settings_persistence.py
  test_config_store.py, test_dashboard.py, test_create_agent.py
SovereignTrader.spec    # PyInstaller spec
runtime_hook.py         # Frozen-mode path hook
scripts/build_exe.py    # Build + verify script
pyproject.toml          # [project.scripts] entry points
```

## 2. Page Constructor Pattern

Every page accepts `mcp` and optional stores. Stores must default to None:

```python
class FooPage(QWidget):
    def __init__(self, mcp, parent=None, chat_store=None, config_store=None):
        super().__init__(parent)
        self.mcp = mcp
        self._chat_store = chat_store
        self._config = config_store
        self._setup_ui()
        if config_store:
            self._load_from_config()
```

MainWindow passes stores:

```python
self.chat_store = ChatStore()
self.config = ConfigStore()
self.stack.addWidget(ChatPage(self.mcp, chat_store=self.chat_store))
self.stack.addWidget(SettingsPage(self.mcp, config_store=self.config))
```

## 3. ConfigStore — TOML Persistence

Stores providers, exchange, MCP, UI, agents sections.

```python
class ConfigStore:
    def __init__(self, config_path=None):
        if not config_path:
            base = Path(os.environ.get("APPDATA", Path.home())) / "SovereignTrader"
            base.mkdir(parents=True, exist_ok=True)
            config_path = base / "config.toml"
        self.config_path = config_path
        self._data = self._load()  # tomllib or manual fallback
        if not self.config_path.exists():
            self.save()  # Write defaults immediately
```

`set()` and `set_section()` auto-save. `save()` writes valid TOML (never import `toml`).

Pitfall: Quote all string values in TOML. Unquoted strings produce invalid TOML that tomllib rejects on reload.

## 4. ChatStore — SQLite Persistence

Multi-session support with ordered messages.

```python
class ChatStore:
    def __init__(self, db_path=None):
        if not db_path:
            # Platform-appropriate dir (%APPDATA%/SovereignTrader)
            base = Path(os.environ.get("APPDATA", Path.home())) / "SovereignTrader"
            base.mkdir(parents=True, exist_ok=True)
            db_path = base / "chat_sessions.db"
        self.db_path = db_path
        self._init_db()
```

Pitfall: Store DB in platform data dir, NOT program directory. A DB next to the EXE breaks distribution.

Schema: sessions (id, name, timestamps), messages (session_id, role, content, timestamp, metadata JSON).

## 5. MCP Client

```python
class McpClient:
    def __init__(self, url="http://127.0.0.1:8128/mcp"):
        self.url = url; self._id = 0
    def call_tool(self, name, arguments) -> dict:
        # POST JSON-RPC: {"jsonrpc":"2.0","id":N,"method":"tools/call",
        #                  "params":{"name":name,"arguments":args}}
        # Raises RuntimeError on JSON-RPC error
```

Hermes-style discovery: `initialize` -> `tools/list` -> `call_tool`.

## 6. MCP Tool Gating (Rust)

Write-gated tools only listed when `SOVEREIGN_MCP_WRITE=1`:

```rust
pub fn tools(&self) -> Vec<ToolDef> {
    let mut tools = vec![ /* read tools always present */ ];
    if self.write_enabled {
        tools.extend([
            ToolDef { name: "create_agent".into(), ... },
            ToolDef { name: "set_default_provider".into(), ... },
        ]);
    }
    tools
}
```

Pitfall: `&str` from JSON doesn't survive into async blocks:
```rust
// WRONG: borrow escapes
let model = args["model"].as_str();
tokio_block(async move { engine.method(model).await })

// CORRECT: convert to String first
let model = args["model"].as_str().map(String::from);
tokio_block(async move { engine.method(model.as_deref()).await })
```

Async call sites need `Arc<TradingEngine>` clone + owned values.

## 7. pytest-qt GUI Tests

Session-scoped QApplication, module-level server fixture:

```python
@pytest.fixture(scope="session")
def qapp():
    return QApplication.instance() or QApplication([])

@pytest.fixture
def mock_mcp():
    client = MagicMock()
    client.call_tool = MagicMock(return_value={"content": [{"type":"text","text":"{\"ok\":true}"}]})
    return client

@pytest.fixture
def mcp_server():
    proc = subprocess.Popen(["sovereign-trader.exe"], env={**os.environ, "SOVEREIGN_MCP_WRITE":"1","SOVEREIGN_MCP_PORT":"8130"})
    # Wait for HTTP 200 on mcp endpoint
    yield "http://127.0.0.1:8130/mcp"
    proc.terminate(); proc.wait(timeout=5)

@pytest.fixture
def hermes_client(mcp_server):
    return HermesMcpClient(url=mcp_server)  # OOP client
```

Pitfall: New ImportError? Check the imported module for missing deps (e.g. `chat_store.py` needed `import os`).

## 8. Generative UI Pattern

Agents send JSON widget specs, page renders recursively:

```python
def _create_widget(self, spec: dict):
    match spec["type"]:
        case "label": return StyledLabel(spec["label"], ...)
        case "button":
            btn = StyledButton(spec["label"])
            if spec.get("action"):
                btn.clicked.connect(lambda _, a=spec["action"]: self._on_action(a))
            return btn
        case "slider": return StyledSlider(...)
        case "metric": return MetricCard(spec["title"], spec["value"])
        case "progress": return StyledProgressBar(...)
        case _: return StyledLabel(f"Unknown: {spec['type']}", color=Theme.DANGER)
```

Input JSON: `{"widgets": [...]}`. Render appends to scrollable container.

## 9. PyInstaller Spec (PyQt6)

Use `os.getcwd()` — NOT `SPECPATH` (unreliable variable).

```python
PROJECT_ROOT = Path(os.getcwd())
RUST_EXE = PROJECT_ROOT / "src-tauri/target/debug/sovereign-trader.exe"
datas = [(str(PROJECT_ROOT/"frontend/pyqt"), "frontend/pyqt")]
hiddenimports = ["PyQt6", "PyQt6.QtCore", "PyQt6.QtGui", "PyQt6.QtWidgets", "PyQt6.support"]
runtime_hooks = [str(PROJECT_ROOT / "runtime_hook.py")]
```

Pre-build: `taskkill /F /IM sovereign-trader.exe` — processes lock the output EXE.

Verification: `tempfile.mkdtemp()` + `shutil.rmtree(ignore_errors=True)`. `TemporaryDirectory` fails on Windows when the EXE holds DLLs open.

Build script:
```python
def verify_exe():
    tmpdir = tempfile.mkdtemp(prefix="sovereign_test_")
    proc = subprocess.Popen([str(exe)], cwd=tmpdir, env={**os.environ,"TEMP":tmpdir,"TMP":tmpdir})
    time.sleep(5)
    if proc.poll() is None:
        proc.terminate(); proc.wait(timeout=5)
        return True  # Self-contained confirmed
    return False  # Crashed
```

## 10. User Workflow Preference

"Properly proceed with all optimally" means:
- NEVER respond with a list of planning questions
- ALWAYS implement immediately: write code, run tests, commit + push
- If a test fails, fix the root cause (never skip or suppress)
- Run the full test suite before claiming completion
- Build script + EXE verification mandatory for packaging tasks
- Pre-commit hook must pass (fmt + clippy + tests)
