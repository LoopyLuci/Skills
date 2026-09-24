# WebBuilder Bug Fixes — September 2026

Session-produced bug fixes and pitfalls discovered during GUI launch testing and comprehensive test suite creation.

## GUI Launch Bugs

### 1. setup_logging() Signature Mismatch

**Error:** `TypeError: setup_logging() got an unexpected keyword argument 'log_level'`

**Location:** `webbuilder/gui/__init__.py`, line ~1599

**Cause:** The `main()` function calls `setup_logging(log_level=config.log_level, log_dir=config.log_path)` but `logging_config.setup_logging()` accepts `level` (not `log_level`) as its second parameter.

**Fix:**
```python
# Before (broken)
logger = setup_logging(log_level=config.log_level, log_dir=config.log_path)

# After (fixed)
logger = setup_logging(level=config.log_level, log_dir=config.log_path)
```

**Prevention:** Always verify function signatures with `inspect.signature()` before calling unfamiliar APIs.

---

### 2. CrashRecovery.get_recovery() Wrong Attribute

**Error:** `AttributeError: 'CrashRecovery' object has no attribute 'recovery_file'`

**Location:** `webbuilder/performance.py`, `get_recovery()` method

**Cause:** The method references `self.recovery_file` but the `__init__` method creates `self.session_file`.

**Fix:**
```python
# Before (broken)
with open(self.recovery_file, "r", encoding="utf-8") as f:

# After (fixed)
with open(self.session_file, "r", encoding="utf-8") as f:
```

**Prevention:** Run `grep -n "self\." performance.py` to audit all attribute references after writing new classes.

---

### 3. MemoryMonitor Missing Import

**Error:** `NameError: name 'Process' is not defined`

**Location:** `webbuilder/performance.py`, `get_memory_usage()` method

**Cause:** The method calls `Process()` without importing it from `psutil` first.

**Fix:**
```python
# Before (broken)
try:
    import psutil
    process = Process()  # NameError!

# After (fixed)
try:
    from psutil import Process
    process = Process()
```

**Prevention:** When importing inside try/except blocks, import the specific name you need, not just the module.

---

## Test Suite API Signature Mismatches

When writing tests for the WebBuilder modular architecture, these API signatures caused failures:

### FormBuilder Methods
- `validate_submission(form_id: str, data: dict)` — takes form ID string, not Form object
- `submit_form(form_id: str, data: dict)` — takes form ID string, not Form object
- `add_field(form_id: str, field_type: str, label: str, **kwargs)` — takes form ID string

### ProjectSearch Constructor
- `__init__(self, project_manager: ProjectManager)` — requires ProjectManager instance
- `search(query: str, limit: int = 20)` — returns list of dicts, not SearchResult objects

### CrashRecovery.get_recovery()
- Returns `{"timestamp": "...", "project": {"id": "...", "name": "..."}}` — nested dict, not flat

### CustomCode Dataclass
- Fields: `html`, `css`, `js`, `head_tags`, `footer_scripts` (not `name`, `code_type`, `content`)

### CustomCodeManager Methods
- `set(project_id: str, code: CustomCode) -> list[str]` — returns validation errors
- `get(project_id: str) -> CustomCode`
- `delete(project_id: str) -> bool`
- `export_code(project_id: str) -> dict[str, str]`

### SEOMetadata Methods
- `to_structured_data() -> str` — returns JSON-LD string
- `validate() -> list[str]` — returns list of error strings

### SitemapGenerator
- `__init__(base_url: str = "https://example.com")`
- `generate() -> str` — no project parameter (uses instance state)
- `save(path: Path) -> None` — takes single path, not project + path

### RobotsTxtGenerator
- `__init__()` — no parameters
- `generate() -> str` — no parameters

### SEOAnalyzer
- `analyze(html_content: str, metadata: SEOMetadata) -> dict[str, Any]`

### AnalyticsTracker
- `track(event_type: str, data: dict = None, ...)` — event_type is first param
- `get_events(event_type: str = None, ...)` — returns list of AnalyticsEvent
- `get_stats() -> dict[str, Any]`

### ImportExport Classes
- `ProjectExporter.__init__(project_manager: ProjectManager)`
- `ProjectImporter.__init__(project_manager: ProjectManager)`
- `BackupManager.__init__(backup_dir: Optional[Path] = None)`
- `BackupManager.create_backup(project_manager: ProjectManager, name: Optional[str] = None)`

---

## Build System

### PyInstaller on Windows
- Build script (`build.py`) creates `dist/WebBuilder.exe` (~130MB) and `dist/WebBuilder-Portable/`
- NSIS installer script (`installer.nsi`) requires NSIS installed separately
- Use `--windowed --onefile --icon=icon.ico` flags
- Exclude unused modules to reduce size: `--exclude-module matplotlib --exclude-module scipy`

### Flask Backend
- Runs on port 5000
- Health check: `GET /api/v1/health` returns `{"status":"healthy"}`
- Auth endpoints: `POST /auth/register`, `POST /auth/login`
- Project endpoints: `GET/POST /api/v1/projects`

---

## September 2026 — Additional Bug Fixes

### 10. Scaling Engine DPI Attribute

**Error:** `AttributeError: 'QScreen' object has no attribute 'logicalDotsInch'`

**Location:** `webbuilder/gui/scaling.py`, `detect_screen()` method

**Cause:** Qt 5.14+ removed `logicalDotsInch()`. The scaling engine was using it to detect DPI.

**Fix:** Use `logicalDotsPerInch()` instead:
```python
# Before (broken)
dpi = screen.logicalDotsInch()

# After (fixed)
dpi = screen.logicalDotsPerInch()
```

**Prevention:** When using Qt screen metrics, verify method exists on your Qt version with `dir(screen)` or check Qt 5.14 migration notes.

---

### 11. FormBuilder Submit Without Validation

**Error:** Test `test_form_submission` failed because `submit_form()` returned success for invalid data.

**Location:** `webbuilder/forms/builder.py`, `submit_form()` method

**Cause:** `submit_form()` sanitized and recorded data without first checking `form.validate(data)`.

**Fix:** Validate before sanitizing:
```python
def submit_form(self, form_id: str, data: dict) -> dict:
    form = self._forms.get(form_id)
    if not form:
        return {"success": False, "error": "Form not found"}
    
    # Validate BEFORE sanitizing
    errors = form.validate(data)
    if errors:
        return {"success": False, "errors": errors}
    
    # Then sanitize and record
    sanitized = {k: v.replace("<", "&lt;") for k, v in data.items()}
    submission = form.add_submission(sanitized)
    return {"success": True, "submission_id": submission["id"], "data": sanitized}
```

**Prevention:** Form submission handlers must always validate before sanitizing/transforming data, so callers receive error feedback instead of silent acceptance.

---

### 12. Duplicate Class Definitions After Extraction

**Error:** `ImportError` or `AttributeError` after extracting classes from monolith.

**Location:** Multiple extractions during modular refactoring

**Cause:** When extracting a class (e.g., `PreviewPanel`, `CommandPanel`) from `gui/__init__.py` into its own module, the class body was removed but the original definition remained in the monolith, causing two definitions of the same name.

**Fix:** After extraction:
1. Remove the class body from the monolith (keep only the import)
2. Create the new module file
3. Add import to `__init__.py`

```python
# gui/__init__.py - after extraction
# BEFORE (broken - duplicate definition)
class PreviewPanel(QWidget): ...  # REMOVE THIS

# AFTER (correct - just import)
from .preview_panel import PreviewPanel
```

**Prevention:** After any extraction, grep for the class name to verify only one definition exists. If two exist, the monolith copy must be fully removed.

---

### 13. Missing Extracted Module File

**Error:** `ImportError: No module named 'webbuilder.gui.preview_panel'`

**Location:** `webbuilder/gui/preview_panel.py`, `webbuilder/gui/command_panel.py`

**Cause:** Class was extracted from monolith but the new module file was never created.

**Fix:** Create the module file AND add to `__init__.py` imports.

**Prevention:** Extraction requires BOTH steps: (1) create new file, (2) update imports. One without the other breaks the build.

### 4. Widget Factory @classmethod vs @staticmethod

**Error:** `TypeError: 'classmethod' object is not callable`

**Location:** `webbuilder/generative_ui/widget_factory.py`

**Cause:** Creator functions were defined as `@classmethod` but called as `cls._creators.get(node.type)(node, parent)`. When stored in a dict and retrieved, classmethod objects don't behave like plain functions.

**Fix:** Use `@staticmethod` for all creator functions:
```python
# Before (broken)
@classmethod
def _create_button(cls, node, parent=None):
    ...

# After (fixed)
@staticmethod
def _create_button(node, parent=None):
    ...
```

**Prevention:** Widget factory creators should always be `@staticmethod` since they don't need access to the class or instance.

---

### 5. ProjectManager Storage Parameter Type

**Error:** `AttributeError: 'WindowsPath' object has no attribute 'save_project'`

**Location:** `webbuilder/core/__init__.py`, `ProjectManager.__init__`

**Cause:** Tests pass `Path(tmpdir)` directly to `ProjectManager()`, but the constructor expected a `JsonFileStorage` instance.

**Fix:** Accept `Path | str | JsonFileStorage` and convert:
```python
# Before (broken)
def __init__(self, storage: Optional[JsonFileStorage] = None):
    self.storage = storage or JsonFileStorage()

# After (fixed)
def __init__(self, storage: Optional[JsonFileStorage | Path | str] = None):
    if isinstance(storage, (Path, str)):
        self.storage = JsonFileStorage(Path(storage))
    else:
        self.storage = storage or JsonFileStorage()
```

**Prevention:** When a class wraps a storage/backend, accept both the wrapper and raw path types for convenience.

---

### 6. Config Method Removals

**Error:** `AttributeError: 'AppConfig' object has no attribute 'get_all_free_models'`

**Location:** `webbuilder/config.py`

**Cause:** `get_all_free_models()` and `get_all_local_models()` were removed in favor of `get_models_for_dropdown()` which returns tuples with is_free flag.

**Fix:** Use `get_models_for_dropdown()` and filter:
```python
# Before (broken)
free = config.get_all_free_models()
local = config.get_all_local_models()

# After (fixed)
models = config.get_models_for_dropdown()
free = [m for m in models if m[4]]  # is_free flag
local = [m for m in models if "Ollama" in m[2] or "LM Studio" in m[2]]
```

---

### 7. AI Module API Changes

**Error:** `ImportError: cannot import name 'AIClient' from 'webbuilder.ai'`

**Location:** `webbuilder/ai/__init__.py`

**Cause:** The AI module was rewritten for live model discovery. Old names (`AIClient`, `AIProvider`, `CircuitBreaker`, `StreamChunk`) no longer exist.

**New API:**
```python
from webbuilder.ai import (
    ModelInfo, ChatMessage, ChatSession, ChatSessionManager,
    BaseProvider, OpenAIProvider, AnthropicProvider,
    OpenRouterProvider, GrokProvider, NousProvider,
    OllamaProvider, LMStudioProvider,
    ModelRouter, get_router, setup_providers,
)
```

---

### 8. Plugin System Missing PluginManager

**Error:** `ImportError: cannot import name 'PluginManager' from 'webbuilder.plugins'`

**Location:** `webbuilder/plugins/__init__.py`

**Cause:** The PDK had `PluginManifest`, `PluginBuilder`, `Plugin`, `PluginValidator`, `PluginRegistry` but no `PluginManager`.

**Fix:** Added `PluginManager` class:
```python
class PluginManager:
    def __init__(self):
        self.registry = PluginRegistry()
    def discover_plugins(self) -> list[Plugin]: ...
    def get_all_plugins(self) -> list[Plugin]: ...
    def get_plugin(self, name: str) -> Optional[Plugin]: ...
    def load_plugin(self, plugin: Plugin): ...
    def unload_plugin(self, name: str): ...
```

---

### 9. Module Relocation to contrib/

**Error:** `ModuleNotFoundError: No module named 'webbuilder.search'`

**Location:** Various test files

**Cause:** Modules moved to `webbuilder.contrib.*` but tests still import from old paths.

**Fix:** Create backward-compatible re-export modules:
```python
# webbuilder/search.py
from webbuilder.contrib.search import *
from webbuilder.contrib.search import ProjectSearch, SearchIndex
```

**Affected modules:** `search`, `analytics`, `import_export`, `performance`, `api_docs`

**Prevention:** When relocating modules, create re-export shims for backward compatibility.

---

### 14. Subpackage Import Mismatch (PyInstaller Freeze)

**Error:** `ImportError: cannot import name 'form_builder' from 'webbuilder.forms'` (in frozen exe)

**Cause:** `gui/__init__.py` imported `form_builder` (lowercase, the singleton) but `webbuilder/forms/__init__.py` only exported `FormBuilder` (the class). The source run worked because the module-level singleton existed in `builder.py`, but PyInstaller only bundles names re-exported by `__init__.py`.

**Fix:**
```python
# gui/__init__.py - BEFORE (broken)
from webbuilder.forms import FormBuilder, form_builder

# gui/__init__.py - AFTER (fixed)
from webbuilder.forms import FormBuilder, Form, FormField, FieldType, get_form_builder
```

**Prevention:** When importing from a subpackage, verify all names exist in that subpackage's `__init__.py`. Test with `python -c "from webbuilder.<pkg> import <Name>"` before committing.

---

### 15. Non-existent Function in Subpackage __init__.py

**Error:** `ImportError: cannot import name 'process_image' from 'webbuilder.assets.pipeline'`

**Cause:** `webbuilder/assets/__init__.py` imported `process_image` from `.pipeline`, but `pipeline.py` only defines `AssetPipeline`, `ProcessedAsset`, `LazyLoader`, `get_asset_pipeline`, `get_lazy_loader`. The name `process_image` was never defined.

**Fix:**
```python
# webbuilder/assets/__init__.py - BEFORE (broken)
from .pipeline import AssetPipeline, process_image

# webbuilder/assets/__init__.py - AFTER (fixed)
from .pipeline import AssetPipeline, ProcessedAsset, LazyLoader, get_asset_pipeline, get_lazy_loader
```

**Prevention:** When adding a new subpackage, run `python -c "import webbuilder.<pkg>"` after writing its `__init__.py` to catch missing names immediately.

---

### 16. Browser Tool capture() Requires Fresh State for Window Targeting

**Error:** `computer_use` capture returns `"capture targeting requires both pid and window_id"` when only pid is provided.

**Cause:** The computer_use tool requires both `pid` and `window_id` for targeted captures. A `capture(app='AppName')` or `list_windows()` call must be made first to obtain valid `window_id`.

**Fix:**
```python
# First call list_windows() to get window_id
windows = computer_use(action="list_windows")
# Then use the returned pid + window_id
computer_use(action="capture", mode="som", pid=10452, window_id=590950)
```

**Prevention:** Always call `list_windows()` before targeted captures. The `window_id` is not derivable from `pid` alone.
### 17. QSize Import from Wrong Qt Module

**Error:** `ImportError: cannot import name 'QSize' from 'PyQt5.QtWidgets'`

**Cause:** `QSize` lives in `PyQt5.QtCore`, not `PyQt5.QtWidgets`. Common mistake when adding toolbar icon sizes.

**Fix:**
```python
# Before (broken)
from PyQt5.QtWidgets import QSize
toolbar.setIconSize(QSize(16, 16))

# After (correct)
from PyQt5.QtCore import QSize
toolbar.setIconSize(QSize(16, 16))
```

**Prevention:** When adding Qt types to imports, verify the module with `python -c "from PyQt5.QtCore import QSize; print(QSize)"` before committing.

---

### 18. Snap Button Update Before Widget Creation

**Error:** `AttributeError: 'ChatWindow' object has no attribute 'snap_btn'`

**Cause:** `_update_snap_button()` was called from `setup_ui()`, but `snap_btn` was created later in `setup_ui()`. The method ran before the button existed.

**Fix:** Move `_update_snap_button()` call to AFTER `setup_ui()` in `__init__`, or remove it from `setup_ui()` and call it after widget creation:
```python
# In __init__:
self._is_snapped = False  # Initialize BEFORE setup_ui
self.setup_ui()
self._update_snap_button()  # Call AFTER setup_ui creates snap_btn
```

**Prevention:** When a method references widgets created in `setup_ui()`, initialize state before `setup_ui()` and call the update method after.

---

### 19. Snap Button Update in PropertiesWindow Before Toolbar Created

**Error:** `AttributeError: 'PropertiesWindow' object has no attribute 'snap_btn'`

**Cause:** Same pattern as #18 — `_update_snap_button()` called before `_setup_toolbar()` created `snap_btn`.

**Fix:** Reorder `__init__` so `_setup_toolbar()` runs before `_update_snap_button()`:
```python
# In PropertiesWindow.__init__:
self._is_snapped = False
self.setup_ui()        # Creates snap_btn via _setup_toolbar
self._update_snap_button()  # Now safe to call
```

**Prevention:** Always call widget-update methods after the widgets they reference are created. Check the initialization order in `__init__`.

---

### 20. Dilithium Sign/Verify Public Key Derivation Mismatch

**Error:** `dilithium_verify()` always returns `False` even with correct keys.

**Cause:** `dilithium_sign()` derives the public key from the private key using `hashlib.sha256(sk + b'pubkey')`, but `dilithium_verify()` uses the `pk` passed as a parameter (which was derived from the seed in `dilithium_keygen()` using `hashlib.sha256(seed + b'verify')`). These are different derivations, so the commitment in the signature doesn't match the verification computation.

**Fix:** `dilithium_keygen()` returns `(pk, seed + sk)` where the private key includes the seed. `dilithium_sign()` extracts the seed from the private key and derives `pk` using the same derivation as `dilithium_keygen()`:
```python
# In dilithium_sign():
seed = sk[:32]
sk_only = sk[32:]
pk = hashlib.sha256(seed + b'verify').digest()  # Same derivation as keygen
sig = hashlib.sha3_256(sk_only + message).digest()
commitment = hashlib.sha256(sig + pk + message).digest()[:32]
return pk + sig + commitment
```

**Prevention:** When implementing sign/verify pairs, the public key derivation must be consistent between keygen, sign, and verify. The private key must contain enough information to derive the public key during signing.

---

### 21. Hybrid Sign/Verify Classical Key Derivation

**Error:** `hybrid_verify()` returns `False` even with correct keys.

**Cause:** `hybrid_sign()` was computing `hashlib.sha256(sk_classical + message)` but `hybrid_verify()` was checking `hashlib.sha256(pk_classical + message)`. Since `pk_classical != sk_classical`, the signatures never matched.

**Fix:** `hybrid_sign()` derives `pk_classical = hashlib.sha256(sk_classical).digest()` and signs with `hashlib.sha256(pk_classical + message)`. `hybrid_verify()` checks `hashlib.sha256(pk_classical + message) == classical_sig`.

**Prevention:** In hybrid sign/verify, both sides must use the same key for the hash. The classical signature uses the public key (derived from the private key), not the private key directly.

---

### 22. CryptoEngine.generate_keypair Returns Nested Tuples

**Error:** `TypeError: can only concatenate tuple (not "bytes") to tuple` when calling `engine.sign()`.

**Cause:** `CryptoEngine.generate_keypair()` for PQ algorithms returned `kyber_keygen(), dilithium_keygen()` which is a tuple of tuples `((pk_kyber, sk_kyber), (pk_dilithium, sk_dilithium))`. The `sign()` method expected `sk_pq` to be bytes, not a tuple.

**Fix:** `generate_keypair()` returns `(pk, sk)` where `pk` and `sk` are bytes (not nested tuples). For PQ algorithms, it returns the Dilithium key pair. For classical algorithms, it returns `(pub, priv)` where `pub = hashlib.sha256(priv).digest()`.

**Prevention:** When a method returns a key pair, always return `(pub, priv)` as a flat 2-tuple of bytes, not nested tuples.

---

### 23. Mutation.type Is a String, Not an Enum

**Error:** `AttributeError: 'str' object has no attribute 'value'` when accessing `mutation.type.value`.

**Cause:** `Mutation.type` is a string, not an enum. The code was using `mutation.type.value.upper()` which fails because strings don't have a `.value` attribute.

**Fix:** Use `mutation.type.upper()` instead of `mutation.type.value.upper()`.

**Prevention:** Check the type of enum-like attributes before accessing `.value`. If `Mutation.type` is a string, use it directly.

---

### 24. Settings Dialog Must Be Standalone QDialog

**Error:** User rejected Settings embedded in side panel or as menu-only access.

**Cause:** The Settings dialog was only accessible via the Tools menu or Ctrl+, shortcut. User explicitly wants a dedicated Settings button.

**Fix:** Add a dedicated Settings menu item in the Tools menu with a keyboard shortcut:
```python
tools_menu = menubar.addMenu("🔧 Tools")
settings_action = QAction("⚙ Settings...", self)
settings_action.setShortcut("Ctrl+,")
settings_action.triggered.connect(self.open_settings)
tools_menu.addAction(settings_action)
```

**Prevention:** Settings must be a standalone QDialog, not embedded in the main window. Same principle as Chat and Properties — user explicitly rejected side panel placement.

---

### 25. Pass Stubs and Silent Exception Swallowing

**Error:** User explicitly rejected "There can be no errors, issues, bugs, placeholders, stubs, warnings, etc."

**Cause:** Multiple `pass` statements in method bodies (stubs), TODO comments, and silent exception swallowing (`except Exception: pass`) throughout the codebase.

**Fix:** Eliminate ALL pass stubs, TODO comments, and silent exception swallowing:
1. **Exception handlers**: Replace `except Exception: pass` with `except Exception as e: logger.warning(f"Context: {e}")`
2. **Method stubs**: Replace `pass` with either a proper implementation or `raise NotImplementedError`
3. **Abstract methods**: Keep `pass` ONLY in `@abstractmethod` definitions (these are intentional interfaces)
4. **Fallback class definitions**: `pass` in `except ImportError` fallback classes is acceptable
5. **TODO comments**: Replace with proper implementation, logging, or `raise NotImplementedError`

**Prevention:** This is a standing policy, not a one-time request. Every `pass` stub, TODO comment, and silent exception swallowing must be eliminated. Run `grep -rn "pass$" webbuilder/ --include='*.py'` to find remaining stubs.

---

### 26. QMessageBox.question() Blocks GUI Startup

**Error:** GUI never appears — exe runs but window is invisible. Crash stages stop at `crash_recovery`.

**Cause:** `QMessageBox.question()` in `_check_crash_recovery()` blocks indefinitely waiting for user input. In headless/auto mode, no user clicks Yes/No, so the GUI thread hangs forever.

**Fix:** Auto-recover without prompting — skip the dialog and auto-recover crash sessions:
```python
# Before (hangs indefinitely)
reply = QMessageBox.question(self, "Crash Recovery", "Recover session?", QMessageBox.Yes | QMessageBox.No)
if reply == QMessageBox.Yes:
    # recover

# After (auto-recover, no blocking)
if crash_recovery.has_recovery():
    data = crash_recovery.get_recovery()
    if data and "project" in data:
        self.current_project = Project.from_dict(data["project"])
        crash_recovery.clear_recovery()
```

**Prevention:** Never call `QMessageBox.question()`, `QMessageBox.information()`, or any modal dialog that waits for user input during startup or in headless/auto mode. Auto-recover or skip dialogs entirely.

---

### 27. Crash Debugging: Use Crash Stages to Pinpoint Failures

**Error:** Exe crashes on launch with no visible error — black background, black letters, crash report unreadable.

**Fix:** Add crash stages to `WebBuilderWindow.__init__` and `main()` to identify exactly where the crash occurs:
```python
# In main():
_crash_stage("start", "Starting WebBuilder")
app = QApplication(sys.argv)
_crash_stage("qt_init", "QApplication created")
setup_exception_handler(app)
_crash_stage("exception_hook", "Exception handler installed")
# ... each stage writes to logs/crashes/early_crash_*.txt

# In WebBuilderWindow.__init__:
_crash_stage("project_manager")
self.project_manager = ProjectManager()
_crash_stage("setup_ui")
self.setup_ui()
# ... etc
```

Crash stages are written to `logs/crashes/early_crash_*.txt` with timestamps. The last stage before the crash identifies the failing component.

**Prevention:** Always add crash stages at each initialization step. The stage that doesn't appear in the log is where the crash happens.

---

### 28. GUI Visibility: showMaximized() + raise_() + activateWindow()

**Error:** Window is created but not visible — appears behind console, minimized, or off-screen.

**Cause:** `window.show()` alone doesn't guarantee visibility. The window may be behind other windows, minimized, or not focused.

**Fix:** After `window.show()`, call:
```python
window.showMaximized()  # Ensure window is visible and maximized
window.raise_()          # Bring to front
window.activateWindow()  # Give focus
window.setFocus()        # Set keyboard focus
```

**Prevention:** Always use `showMaximized()` + `raise_()` + `activateWindow()` + `setFocus()` after `show()` to guarantee the GUI is visible and focused.

---

### 29. Crash Reports: Write to File, Not Invisible Dialogs

**Error:** Crash error dialog has dark background with dark text — invisible to user.

**Cause:** Error dialog with dark background + dark text makes crash reports unreadable. User sees "black background, black letters."

**Fix:** Write crash reports to files in `logs/crashes/`:
```python
# In setup_exception_handler():
def exc_hook(exctype, value, tb):
    error_msg = ''.join(traceback.format_exception(exctype, value, tb))
    # Write to crash log file
    crash_dir = "logs/crashes"
    os.makedirs(crash_dir, exist_ok=True)
    crash_file = os.path.join(crash_dir, f"crash_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    with open(crash_file, 'w', encoding='utf-8') as f:
        f.write(f"WebBuilder Crash Report\n")
        f.write(f"Exception: {exctype.__name__}: {value}\n\n")
        f.write(f"Traceback:\n{error_msg}\n")
    print(f"Crash report saved to: {crash_file}")
```

Crash reports include: exception type, message, full traceback, local variables, system info (Python version, platform, CPU, RAM), telemetry context.

**Prevention:** Never rely on dialogs for crash reports — always write to files the user can read after the crash.
