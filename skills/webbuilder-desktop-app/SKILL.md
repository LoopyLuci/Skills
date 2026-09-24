---
name: webbuilder-desktop-app
description: Build PyQt5 desktop web builders with AI chat, multi-provider integration, and HTML export.
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [pyqt5, webbuilder, ai-chat, multi-provider, desktop-app, html-export]
---

# WebBuilder Desktop App Development

Build professional PyQt5 desktop applications for visual web/app building with integrated AI chat, multi-provider model support, real-time preview, and HTML export.

## Trigger

Use when the user wants to build a desktop application for visual web building with:
- Drag-and-drop section builder
- Integrated AI chat with multiple model providers
- Real-time HTML preview
- Export to production-ready HTML
- Provider configuration (cloud + local LLMs)

## Architecture

```
desktop/
├── desktop_app.py       # Main application (PyQt5)
├── components.py        # Custom widgets (SectionWidget, ProviderCard, etc.)
├── output/
│   ├── app.py           # Flask backend
│   └── index.html       # Frontend
├── test_integration.py  # Integration tests
└── assets/              # Icons, images, etc.
```

## Provider System

### Multi-Provider Support (12 providers)

Supported providers (all OpenAI-compatible except Anthropic and Google):
- OpenAI, Anthropic, Google Gemini, OpenRouter, Groq, Ollama, LM Studio, Grok, Nous Research, OpenCode Zen, OpenCode Go, Unsloth

All providers loaded dynamically from their APIs — no hardcoded placeholder model names.

```python
class Config:
    ALL_PROVIDERS = {
        # Cloud providers
        'openai': {
            'name': 'OpenAI',
            'icon': '🟢',
            'type': 'cloud',
            'endpoint': 'https://api.openai.com/v1/chat/completions',
            'models': [
                {'id': 'gpt-4o', 'name': 'GPT-4o', 'description': '...', 'free': False, 'context': 128000},
                {'id': 'gpt-4o-mini', 'name': 'GPT-4o Mini', 'description': '...', 'free': False, 'context': 128000},
            ]
        },
        # Local providers (no API key needed)
        'ollama': {
            'name': 'Ollama',
            'icon': '🦙',
            'type': 'local',
            'endpoint': 'http://localhost:11434/api/chat',
            'models': [
                {'id': 'llama3.2', 'name': 'Llama 3.2', 'description': '...', 'free': True, 'context': 8192},
            ]
        },
    }
```

### Model Router (Free-First Sorting)

```python
class ModelRouter:
    def get_provider_models(self, provider_id):
        """Get models sorted with free first, then by context size descending"""
        models = self.providers[provider_id].get('models', [])
        return sorted(models, key=lambda m: (
            not m.get('free', False),
            -m.get('context', 0)
        ))
    
    def get_all_free_models(self):
        """Aggregate free models from all providers"""
        # Iterate all providers, collect models where free=True
        # Attach provider_id, provider_name, provider_icon for UI
        pass
    
    def get_all_local_models(self):
        """Aggregate local provider models (Ollama, Unsloth, etc.)"""
        pass
```

### Provider Card Pattern

```python
class ProviderCard(QFrame):
    """Visual card showing provider status"""
    # Shows: icon, name, type, model count, status dot
    # Status: 🟢 configured, 🔵 local, ⚪ not configured
    # Click → opens configuration dialog
```

## AI Chat Integration

### Thread-Safe API Calls

```python
def get_ai_response(self, msg):
    provider = self.config.get('default_provider', 'openai')
    api_key = self.config.get_key(provider)
    
    if not api_key:
        self.add_chat_message("assistant", "Please configure API key...")
        return
    
    def do_api_call():
        try:
            response = self.real_api_call(msg, provider, model, api_key)
            self.add_chat_message("assistant", response)
        except Exception as e:
            self.add_chat_message("assistant", f"Error: {str(e)}")
        finally:
            self.chat_status.setText("🟢")
            self.chat_input.setEnabled(True)  # Re-enable on UI thread via QTimer
    
    threading.Thread(target=do_api_call, daemon=True).start()
```

### Multi-Provider API Handler

```python
def real_api_call(self, msg, provider, model, api_key):
    provider_config = Config.ALL_PROVIDERS.get(provider, {})
    endpoint = provider_config.get('endpoint', '')
    
    if provider in ['openai', 'openrouter', ...]:
        # OpenAI-compatible: Bearer token auth
        r = requests.post(endpoint, headers={'Authorization': f'Bearer {api_key}'}, json=payload)
        return r.json()['choices'][0]['message']['content']
    
    elif provider == 'anthropic':
        # Claude API: x-api-key header
        r = requests.post(endpoint, headers={'x-api-key': api_key}, json=payload)
        return r.json()['content'][0]['text']
    
    elif provider == 'google':
        # Gemini API: key in URL query param
        r = requests.post(f"{endpoint}/{model}:generateContent?key={api_key}", json=payload)
        return r.json()['candidates'][0]['content']['parts'][0]['text']
    
    elif provider == 'ollama':
        # Local: no auth needed
        r = requests.post(endpoint, json=payload)
        return r.json()['message']['content']
```

## HTML Export System

### Production-Ready HTML Generator

```python
class HTMLExporter:
    def generate_html(self):
        sections = self.project.get('pages', [{}])[0].get('sections', [])
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{self.project.get('name', 'WebBuilder Project')}</title>
  <style>
    :root {{
      --c-primary: {self.colors.get('primary', '#3b82f6')};
      --c-secondary: {self.colors.get('secondary', '#8b5cf6')};
      /* CSS variables for design system */
    }}
    /* Responsive utilities, buttons, sections */
  </style>
</head>
<body>
  <main>
{"".join(self.render_section(s) for s in sections)}
  </main>
</body>
</html>'''
    
    def render_section(self, section):
        """Render each section type to HTML"""
        t = section['type']
        p = section.get('props', {})
        
        if 'hero' in t:
            return self._render_hero(p)
        elif 'features' in t:
            return self._render_features(p)
        elif 'pricing' in t:
            return self._render_pricing(p)
        # ... etc for each section type
```

### Section Types

| Section | Key Props |
|---------|-----------|
| `navbar` | logo, links, ctaText |
| `hero-centered` | title, subtitle, ctaText, backgroundColor |
| `features-grid-3` | title, subtitle, columns, items[] |
| `featues-cards` | title, items[] |
| `pricing-3-tiers` | title, subtitle, tiers[] |
| `stats-3-col` | title, items[] |
| `cta-simple` | title, subtitle, buttonText, backgroundColor |
| `testimonials-2-col` | title, items[] |
| `faq-accordion` | title, questions[] |
| `footer` | copyright, links[] |

## Tabbed Interface Pattern

```
Tabs: Editor | Preview | Chat | Providers | Settings
Dockable: Agent Chat (right side, Ctrl+Shift+C)
```

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+N | New Project |
| Ctrl+S | Save Project |
| Ctrl+E | Export HTML |
| Ctrl+G | Generate Project |
| Ctrl+K | Open Providers Tab |
| Ctrl+, | Open Settings Tab |
| Ctrl+Shift+C | Toggle Agent Chat |
| Ctrl+Shift+E | Export React |
| Ctrl+Shift+S | Start/Stop Server |

## Testing

### Integration Test Pattern

```python
def test_html_export():
    """Test all section types render to valid HTML"""
    project = {
        'pages': [{
            'sections': [
                {'id': 's1', 'type': 'navbar', 'props': {'logo': 'Brand', 'links': ['Home']}},
                {'id': 's2', 'type': 'hero-centered', 'props': {'title': 'Welcome'}},
                # ... all section types
            ]
        }]
    }
    
    exporter = HTMLExporter(project)
    html = exporter.generate_html()
    
    assert '<!DOCTYPE html>' in html
    assert 'Welcome' in html
    # ... verify each section's content
```

## Pitfalls

1. **Standalone windows in splitter**: Never put Chat or Properties windows inside the main window's `right_splitter` or any splitter. They are separate `QMainWindow` instances. Placing them in a splitter makes them invisible when the splitter collapses. Instead, use snap-in/snap-out via `QDockWidget` wrappers added to `RightDockWidgetArea`. See the Window Placement Rules below.

2. **PyQt circular imports**: Don't import from the main module in component files. Pass Config as a parameter.

3. **Threading with PyQt**: Use `threading.Thread` for API calls, but re-enable UI elements on the main thread via `QTimer.singleShot`.

4. **QtWebEngineView causes Chromium crashes** — `QWebEngineView` spawns a Chromium network service process that crashes on Windows, producing `Network service crashed, restarting service` errors. **Never use QWebEngineView in the Preview panel.** Use `QTextBrowser` for HTML rendering instead — it's lightweight, no Chromium dependency, no crashes. If rich rendering is needed, use a bundled browser approach, not QtWebEngine.

5. **Grid layout addStretch**: QGridLayout doesn't have `addStretch()` — use `setRowMinimumHeight()` instead.

6. **QFormLayout addRow on QVBoxLayout**: Use QHBoxLayout for form-like layouts inside non-form layouts.

7. **Lambda capture in loops**: Always use default parameter binding: `lambda event, p=pid: func(p)`.

8. **File paths on Windows**: Use pathlib.Path for cross-platform compatibility.

9. **QFrame mousePressEvent**: To make a QFrame clickable, override `mousePressEvent` directly, not `clicked` (which doesn't exist).

10. **Qt.AA_ShareOpenGLContexts import ordering**: Setting `Qt.AA_ShareOpenGLContexts = True` AFTER `from PyQt5.QtCore import Qt` fails because the import itself triggers QCoreApplication creation. Set the flag via `os.environ` BEFORE any PyQt import. Not needed if QWebEngineView is not used.

11. **Splitter block indentation**: All code inside `setup_ui()` must use consistent 8-space indentation. Mixed indentation (e.g. 8 spaces for one line, 16 for the next) inside a splitter setup block causes `IndentationError` at import time and the window never appears. When adding panels to `right_splitter` or any splitter, keep every line at the same indent level — do not nest comments or widget creation at different depths.

12. **QT_QPA_PLATFORM for GUI visibility**: On Windows, `QT_QPA_PLATFORM` must be set to `'windows'` BEFORE any PyQt import. If the GUI is invisible or not showing, add `os.environ['QT_QPA_PLATFORM'] = 'windows'` in the entry point before `from PyQt5.QtCore import Qt`. Without this, Qt may default to an offscreen/minimal platform that renders nothing.

13. **QT_QPA_PLATFORM=offscreen segfault on Windows**: Running a PyQt5 GUI in full mode (not `--headless`) with `QT_QPA_PLATFORM=offscreen` causes a segmentation fault (signal 11/SIGSEGV) during `app.exec_()` teardown on some Windows hosts. The crash happens at Qt event loop teardown, after the app has run successfully. Workaround: use the `--headless` entrypoint which exits via `QTimer.singleShot(2000, app.quit)` before the segfault trigger. Do not run full GUI mode with offscreen platform on a headless server — the segfault is a Qt/PyQt5 platform limitation, not a code bug. See [references/qt-offscreen-segfault.md](references/qt-offscreen-segfault.md).

### Crash Reporting & Logging

13. **Invisible error dialogs**: QMessageBox with dark text on dark background is unreadable. Crash handler must write to files in `logs/crashes/`, never show dialogs. The console is also invisible with `--windowed` — file output is the only reliable channel.
14. **Crashes before Qt init**: The exception hook only catches Python exceptions after QApplication exists. Pre-Qt crashes (import errors, config errors) need early capture in `main()` before any Qt code.
15. **Crash report contents**: Include exception type, message, full traceback, local variables, Python version, platform, CPU, RAM, executable path, and telemetry context. Save as both JSON (machine-readable) and text (human-readable).
16. **PyInstaller hides stderr**: With `--windowed`, console output is suppressed. Crash reports and console output must be written to files in `logs/` for post-mortem analysis.

### Installer & Updater

17. **Installer/Updater system**: `webbuilder/installer/__init__.py` provides Installer class with:
    - Inno Setup / NSIS / ZIP installer creation
    - GitHub releases update checking
    - Auto-update with download, install, rollback
    - Progress tracking (status, percent, speed, ETA)
    - Silent (`/S`) and interactive modes
    - Backup before install for rollback safety
    - Singleton: `get_installer()`

18. **Update system**: `webbuilder/update/__init__.py` provides UpdateManager with:
    - GitHub releases API integration
    - Version comparison
    - Update download and installation
    - Rollback support
    - Singleton: `get_update_manager()`

### Crypto Pitfalls

12. **CryptoEngine.generate_keypair returns flat tuples**: `generate_keypair(algorithm)` returns `(pub_bytes, priv_bytes)` — NEVER nested tuples like `((pk, sk), (pk2, sk2))`. The PQ branch unpacks Kyber and Dilithium key pairs and returns only the Dilithium `(pk, sk)`. Always verify return type is bytes before passing to sign().

13. **Dilithium sign/verify byte offsets**: Signature format is `pk(32) || sig(64) || commitment(32)` = 128 bytes total. In `dilithium_verify`, extract with `sig_part = sig[32:96]` (skip pk prefix) and `commitment = sig[96:128]`. Using `sig[:64]` reads the last 32 bytes of pk + first 32 bytes of sig, causing verification to always fail.

14. **CryptoEngine.sign requires algorithm name**: `engine.sign(message, private_key)` without algorithm defaults to primary (PQ), which calls `dilithium_sign(message, private_key)`. If private_key is bytes (not a tuple), this causes `TypeError: can only concatenate tuple (not "bytes") to tuple`. ALWAYS specify algorithm: `engine.sign(message, private_key, 'kyber768-dilithium2')` or `engine.sign(message, private_key, 'classic-aes256-rsa4096')`.

### Crash Reporting & Logging

15. **Invisible error dialogs**: QMessageBox with dark text on dark background is unreadable. Crash handler must write to files in `logs/crashes/`, never show dialogs. The console is also invisible with `--windowed` — file output is the only reliable channel.
16. **Crashes before Qt init**: The exception hook only catches Python exceptions after QApplication exists. Pre-Qt crashes (import errors, config errors) need early capture in `main()` before any Qt code.
17. **Crash report contents**: Include exception type, message, full traceback, local variables, Python version, platform, CPU, RAM, executable path, and telemetry context. Save as both JSON (machine-readable) and text (human-readable).
18. **PyInstaller hides stderr**: With `--windowed`, console output is suppressed. Crash reports and console output must be written to files in `logs/` for post-mortem analysis.

**Crash reporting reference**: [references/crash-reporting.md](references/crash-reporting.md) — full pattern, log layout, verification steps, pitfalls.

**Qt offscreen segfault reference**: [references/qt-offscreen-segfault.md](references/qt-offscreen-segfault.md) — offscreen platform segfault on Windows, headless workaround, verification.

**SQLite + cryptography pitfalls reference**: [references/sqlite-crypto-pitfalls.md](references/sqlite-crypto-pitfalls.md) — `sqlite3.connect()` `uri=True` requirement for in-memory shared cache, `Fernet.InvalidToken` does not exist.

**Python error hardening skill**: [python-error-hardening](../python-error-hardening) — systematic bare-except elevation workflow, test singleton isolation, conftest pitfalls for Qt apps.

**42 crash stages** (start → qt_init → exception_hook → ... → window_show):
- Early capture: pre-Qt startup stages (start, qt_init, exception_hook)
- Stability: stability_monitor, autosave_manager, retry_manager, circuit_breaker, resource_guard, state_manager, error_boundary, memory_guard, thread_safety
- Performance: lazy_loader, cache_manager, async_executor, batch_processor, memory_pool, debouncer, throttler, parallel_executor, performance_profiler, connection_pool, lazy_init, resource_pool, compression_manager, incremental_updater
- UI setup: logging, theme, project_manager, export_manager, scaling_init, autosave, memory_monitor, crash_recovery, setup_ui, setup_menu, new_project, autosave_timer, state_manager, complete, window_create, window_show

| Window | Type | Access | Placement |
|--------|------|--------|-----------|
| Main Window | `QMainWindow` | Auto-created | Central application |
| Chat | `QMainWindow` (standalone) | `Ctrl+Alt+C` or auto-open | Floating, can snap to RightDockWidgetArea |
| Properties | `QMainWindow` (standalone) | `Ctrl+Alt+P` or auto-open | Floating, can snap to RightDockWidgetArea |
| DOM/Snippets/Command | Widget | Auto-added | `right_splitter` in main window |

**Snap-In/Snap-Out Pattern**: Both Chat and Properties implement `_toggle_snap()`, `_snap_to_main()`, and `_unsnap_from_main()`. The main window provides `handle_chat_snap_request()` and `handle_properties_snap_request()` handlers. Use `QDockWidget` wrappers (`ChatDockWidget`, `PropertiesDockWidget`) for docking. The snap button lives in the floating window's toolbar (📌 icon or "Snap to Main" action with `Ctrl+Alt+S` shortcut).

**Windows snap into main by default**: When the application launches, both Chat and Properties windows are automatically snapped into the main window's RightDockWidgetArea. They do not float by default. The snap button shows "📌 Unsnap from Main" when snapped. Users can unsnap to float, then re-snap with Ctrl+Alt+S or the button.

**Snap implementation requirements (both Chat and Properties):**
- `_is_snapped: bool = False` — tracks current state
- `_dock_widget: Optional[QDockWidget] = None` — the dock wrapper when snapped
- `_main_window_ref` — reference to the main window when snapped (for `removeDockWidget`)
- `Ctrl+Alt+S` shortcut on the floating window to toggle snap
- Toolbar toggle button (📌 Snap/Unsnap) that updates its text and style via `_update_snap_button()` after every snap/unsnap — without this the button shows stale state and the user cannot tell which mode is active
- `_snap_to_main()`: walks `self.parent()` chain to find a `QMainWindow` with `addDockWidget`, creates the `QDockWidget` wrapper if missing, transfers the window's central widget into it, calls `addDockWidget(Qt.RightDockWidgetArea, dock)`
- `_unsnap_from_main()`: calls `removeDockWidget(dock)`, `dock.setParent(None)`, resets state, then `show()`, `raise_()`, `activateWindow()` on the floating window so it reappears
- Main window handlers (`handle_chat_snap_request`, `handle_properties_snap_request`) accept the floating window instance and a `snap: bool | None` toggle; they import the matching `DockWidget` class, create it on first snap, and manage add/remove

See [references/snap-unsnap-pattern.md](references/snap-unsnap-pattern.md) for the full implementation reference with code samples, pitfall table, and state variable definitions.

## ML/AI Pipeline

### Self-Learning Pipeline
- `webbuilder/ml_engine/self_learning.py` — online learning from user interactions
- TrainingDashboard records interaction data during training for self-learning
- Models improve from usage without external API dependencies

### Post-Quantum Crypto
- `webbuilder/security/post_quantum.py` — Kyber KEM + Dilithium signatures, hybrid classical+PQ
- CryptoEngine with algorithm agility (3 algorithms, swappable via `set_primary()`)
- `generate_keypair(algorithm)` returns flat `(pub_bytes, priv_bytes)` — never nested tuples
- `sign(message, private_key, algorithm)` — ALWAYS specify algorithm name; omitting uses primary (PQ), causing TypeError if private_key is bytes not tuple
- See [references/pq-crypto-traits.md](references/pq-crypto-traits.md) for Dilithium byte offsets, signature format, and CryptoEngine usage patterns.

### Trait-Based Swappable Abstractions
- `webbuilder/abi.py` — Trait base class, TraitRegistry, ComponentFactory, CompositeTrait
- `webbuilder/integrations/traits.py` — registers AI/ML/crypto/UI/storage/logging as trait implementations
- Traits: AIProviderTrait, CryptoEngineTrait, MLModelTrait, UIRendererTrait, StorageBackendTrait, LoggingBackendTrait

## Updated Project Structure

```
C:\Users\Server\Desktop\WebBuilder\
├── webbuilder_desktop.py      # Main entry point (PyInstaller target)
├── webbuilder/
│   ├── __init__.py            # Main window, Activity tab, Terminal, Training Dashboard, Settings
│   ├── gui/
│   │   ├── chat_window.py     # ChatWindow + ChatDockWidget, model fetching, dock animation, SnapState
│   │   ├── properties_window.py  # PropertiesWindow + PropertiesDockWidget, dock animation, SnapState
│   │   ├── terminal_cli.py    # Terminal CLI (shell + WebBuilder commands)
│   │   ├── activity_log.py    # Activity Log tab (filter, search, copy, save, JSON)
│   │   ├── training_dashboard.py  # ML Training Dashboard (7 NumPy models)
│   │   ├── canvas.py          # Canvas with apply_mutation (MutationEngine)
│   │   ├── command_panel.py   # CommandPanel (natural language UI mods)
│   │   ├── preview_panel.py   # Preview panel (QTextBrowser, no QtWebEngine)
│   │   ├── snap_system.py     # SnapState class for centralized snap management
│   │   └── settings_window.py # SettingsWindow with 6 tabs, real model loading
│   ├── ml_engine/
│   │   ├── models.py          # 9 NumPy ML models
│   │   ├── training.py        # Training pipeline
│   │   ├── persistence.py     # Model save/load
│   │   └── self_learning.py   # Self-learning pipeline
│   ├── security/
│   │   ├── compliance.py      # CSP, security headers, CSRF, XSS
│   │   └── post_quantum.py    # Kyber KEM, Dilithium, hybrid crypto, CryptoEngine
│   ├── abi.py                 # Trait system (Trait, TraitRegistry, ComponentFactory)
│   ├── integrations/
│   │   └── traits.py          # Trait integration (register existing components as traits)
│   ├── ai/                    # AI providers (BaseProvider ABC)
│   ├── backup/                # BackupManager - auto-backup with versioning, retention, integrity
│   ├── storage/               # SQLiteStorage - structured storage with WAL mode, migration support
│   ├── health/                # HealthMonitor - system resource monitoring, app health checks
│   ├── watchdog/              # Watchdog - process monitoring, auto-restart, resource leak detection
│   ├── update/                # UpdateManager - GitHub release checking, auto-update, rollback
│   ├── installer/             # Installer - Inno/NSIS/ZIP installer creation, auto-update, rollback
│   ├── migrations/            # MigrationSystem - versioned migrations with up/down/rollback
│   ├── command/
│   │   └── palette.py         # CommandPalette
│   ├── command.py             # CommandRegistry
│   ├── history.py             # VersionHistory
│   ├── responsive.py          # ResponsivePreview
│   ├── css.py                 # CSSEditor
│   └── core/
│       └── __init__.py       # Project, Page, Section, Design
├── tests/unit/                # 293 tests passing
├── dist/WebBuilder.exe        # PyInstaller onefile build (127MB)
└── requirements.txt
```

**Auto-open on launch**: Call `QTimer.singleShot(500, self._auto_open_windows)` after `setup_ui()`. Both windows must be shown — if the user says "I do not see X", the window was likely never opened or was placed in a splitter.

**Keyboard shortcuts**: `Ctrl+Alt+C` = Chat, `Ctrl+Alt+P` = Properties, `Ctrl+Alt+S` = toggle snap on active floating window.

**Singleton reuse**: Use `get_chat_window()` / `get_properties_window()` singletons — reuse the same instance, don't create new ones each open.

**Unsnap visibility**: When unsnapping, always call `show()`, `raise_()`, `activateWindow()` on the floating window so it reappears.

**Preserve the factory function on rewrite**: When rewriting the tail of `chat_window.py` (or any module with a `get_*_window()` factory + `_*_window` singleton), the factory and singleton MUST survive the rewrite. Dropping them breaks any test or call site that imports `get_chat_window` — the error is `ImportError: cannot import name 'get_chat_window'`. Always `grep` the module for `def get_` and the singleton name before and after a rewrite, and run `py_compile` on all three GUI files (`chat_window.py`, `properties_window.py`, `__init__.py`) before rebuilding.

## Recovering a Lost PyInstaller Package

When the `webbuilder/` Python package is missing on disk but the bundled `WebBuilder.exe` still exists:

1. **Do NOT brute-force extract the exe.** PyInstaller bundles are archives, not source trees. Repeated extraction attempts with different scripts on the same failure mode is a loop — stop after two identical failures.
2. **Recover the interface from the existing test tree first.** The tests under `apps/desktop/tests/` already import the exact nested modules and exported names. Grep them for `from webbuilder` / `import webbuilder` to recover the module map and symbol contract. This is the durable spec; the binary is not.
3. **Rebuild `webbuilder/` from the test-derived shape,** implementing real constructors and the minimal methods the tests call. Use stubs only as scaffolding; replace them with working code as the tests demand it.
4. **Run the test suite early and often.** Do not rebuild the exe before the package imports and the tests pass. The exe is downstream of a working `webbuilder/` tree.
5. **Only then rebuild** with PyInstaller once the package is coherent and tests are green.

Pitfall: treating the exe as the source of truth leads to hours of extraction churn. The test tree is the source of truth for the package's public surface.

See [references/source-recovery-via-tests.md](references/source-recovery-via-tests.md) for the detailed recipe.

See [references/distribution-release.md](references/distribution-release.md) for GitHub release process, LICENSE, tag creation, and F-Droid notes.
