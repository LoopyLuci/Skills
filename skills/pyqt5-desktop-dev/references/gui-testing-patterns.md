# GUI Testing Patterns for PyQt5 QEMU Control

## When to use

- Testing a PyQt5 GUI that wraps QEMU/QMP/SSH bridges
- Building comprehensive test suites for desktop VM control apps
- Creating standalone test executors with machine-readable reporting

## Test Architecture

### 15 Test Categories

```python
TEST_CATEGORIES = {
    "PANEL_INIT":   ["panel_instantiate", "panel_names", "sidebar_count", "bridges"],
    "QMP":          ["connect", "query_status", "query_name", "query_uuid", "query_version", "query_kvm", "signals"],
    "DASHBOARD":    ["status_dot", "stat_labels", "buttons", "add_activity"],
    "VM_CONTROL":   ["lifecycle_buttons", "start", "stop", "reset", "suspend", "resume", "eject"],
    "SNAPSHOTS":    ["list", "create", "restore", "delete"],
    "STORAGE":      ["disk_list", "create", "resize", "convert", "delete"],
    "ISO_MANAGER":  ["table", "scan", "import", "add_source", "remove_source"],
    "QMP_CONSOLE":  ["send", "presets", "raw_json", "clear"],
    "TELEMETRY":    ["chart", "timer", "host_metrics"],
    "SETTINGS":     ["validation", "save", "reset"],
    "CLI":          ["status", "vm_list", "snapshot_list", "iso_list", "config"],
    "REST_API":     ["endpoints", "json_response"],
    "SELF_HEALING": ["atomic_state", "snapshot_restore", "wal_recovery"],
    "MULTI_VM":     ["add", "remove", "start", "stop", "list"],
    "CROSS_CUTTING": ["no_errors", "sidebar", "window_drag", "reconnect_timer", "telemetry_timer"],
}
```

## asyncio Event Loop in Pytest Fixtures

GUI tests run in the main Qt thread — there is NO asyncio event loop. Two patterns:

### Pattern 1: Per-fixture loop (for connection fixtures)

```python
@pytest.fixture
def qmp_client():
    from vm_mcp.setup import QMPClient
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    client = loop.run_until_complete(_connect())
    yield client
    loop.run_until_complete(client.disconnect())
    loop.close()
```

### Pattern 2: Per-test loop (for individual test methods)

```python
def test_query_status(self, qmp_client):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(qmp_client.send("query-status"))
    assert "return" in result
    loop.close()
```

**Why:** `asyncio.get_event_loop()` in the main thread raises `RuntimeError: There is no current event loop in thread 'MainThread'`. Creating a fresh loop per test is the safe pattern.

## CLI Testing via subprocess

```python
def test_cli_status(self):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(PROJECT_DIR / "src")
    result = subprocess.run(
        [sys.executable, str(GUI_DIR / "cli.py"), "status"],
        capture_output=True, text=True, timeout=10,
        cwd=str(PROJECT_DIR), env=env,
    )
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert "server" in data
```

**Key:** Set `PYTHONPATH` to include `src/` so `vm_mcp.config` can be imported. The CLI file must also add `sys.path.insert(0, str(SCRIPT_DIR / "src"))` and `sys.path.insert(0, str(SCRIPT_DIR.parent))`.

## Standalone Test Executor

For running outside pytest (e.g., from MCP terminal tool), build a `TestExecutor`:

```python
@dataclass
class TestResult:
    test_id: str
    name: str
    category: str
    passed: bool
    duration_ms: float
    error: str = ""

class MCPTestExecutor:
    def run_command(self, command, timeout=30):
        result = subprocess.run(
            command, capture_output=True, text=True, timeout=timeout,
            cwd=str(self._project_dir),
            env={**os.environ, "QT_QPA_PLATFORM": "offscreen", "VENV_PY": str(self._venv_py)},
            shell=True,
        )
        return result.stdout, result.stderr, result.returncode
    
    def run_test(self, test_dict):
        # Run single test, capture output, check expected substring in output
        pass
    
    def run_all_tests(self):
        # Run all categories, collect results
        # Analyze failures: ModuleNotFoundError→gap, Timeout→bug, AssertionError→bug
        # Save JSON + CSV reports to test-results/ directory
        pass
```

## QMP Response Unwrapping

QMP returns nested dicts. Handle both shapes:

```python
def unwrap_qmp(response):
    """Unwrap QMP response to inner data."""
    if "return" in response and isinstance(response["return"], dict):
        return response["return"]
    return response
```

**Pitfall:** Signals may emit either raw `{'return': {...}}` or unwrapped dicts. Always handle both.

## Panel Wiring Checklist

For each panel, verify:
1. ✅ Class instantiates
2. ✅ `set_qmp_bridge()` and/or `set_ssh_bridge()` methods exist
3. ✅ Bridge methods called when user triggers actions
4. ✅ Signal handlers exist for bridge signals
5. ✅ Panel updates UI in response to bridge signals
6. ✅ All buttons have `clicked.connect()` wired
7. ✅ All timers are started and parented correctly

## ISO Manager Implementation

```python
class ISOManager:
    """Internal + external ISO storage."""
    
    def __init__(self, internal_dir="iso/"):
        self._internal = Path(internal_dir)
        self._sources_file = self._internal / ".iso-sources.json"
        self._external_sources = self._load_sources()
    
    def scan_isos(self) -> list[dict]:
        results = []
        # Scan internal
        for f in self._internal.glob("*.iso"):
            results.append({"name": f.name, "size": f.stat().st_size, "path": str(f), "source": "internal"})
        # Scan external sources
        for src in self._external_sources:
            for f in Path(src).glob("*.iso"):
                results.append({"name": f.name, "size": f.stat().st_size, "path": str(f), "source": "external"})
        return results
    
    def import_iso(self, src_path: str) -> Path:
        src = Path(src_path)
        dest = self._internal / src.name
        import shutil
        shutil.copy2(src, dest)
        return dest
```

## Multi-VM Manager

JSON-based registry for controlling multiple QEMU instances:

```python
class MultiVMManager:
    def __init__(self, registry_file="vms.json"):
        self._registry_file = Path(registry_file)
        self._vms = self._load_registry()
    
    def add_vm(self, name, qmp_uri, disk_path, **kwargs):
        self._vms[name] = {"qmp_uri": qmp_uri, "disk_path": disk_path, **kwargs}
        self._save_registry()
    
    def start_vm(self, name):
        import subprocess
        vm = self._vms[name]
        args = self._build_qemu_args(vm)
        subprocess.Popen(args)
    
    def list_vms(self):
        return [{"name": k, **v} for k, v in self._vms.items()]
```

## Key Testing Principles

1. **Test panels individually** — each panel has its own test class (`TestXxxPanel`)
2. **Mock nothing for QMP** — use live QEMU; tests are integration-level
3. **Graceful degradation** — SSH tests skip when no guest sshd; document via `@pytest.mark.skipif`
4. **Assert structure AND behavior** — check widgets exist AND respond to method calls
5. **Capture asyncio errors** — always close event loops in `finally` blocks
6. **Test CLI and API** — not just GUI widgets; agents access via these interfaces
7. **Report in machine-readable format** — JSON + CSV for CI and gap analysis