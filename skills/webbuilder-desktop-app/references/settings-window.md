# Settings Window — Implementation Pattern

## Architecture

Settings is a **dedicated standalone window** (QDialog), NOT a panel inside the main window's properties area. The user explicitly rejected embedding settings in Properties.

```
webbuilder/gui/settings_window.py   ← SettingsWindow (QDialog, 6 tabs)
webbuilder/gui/__init__.py         ← open_settings() imports SettingsWindow
webbuilder/config.py               ← SettingsManager: load/save/settings.json
```

## SettingsWindow Tabs

| Tab | Widget | Purpose |
|-----|--------|---------|
| 🎨 Appearance | Theme selector (6 themes), accent color, font size, animation toggle, density | Visual customization |
| 🤖 AI Providers | Provider list, API key input, base URL, **real model fetch**, model dropdown | Provider config + live model loading |
| 📝 Editor | Tab size, word wrap, line numbers, minimap, auto-save interval, format on save | Editor behavior |
| 📤 Export | Format, minify, inline CSS, responsive images, performance budget | Export options |
| 🔌 Plugins | Plugin list, install/enable/disable | Extension management |
| ℹ About | Version, module count, lines of code, license | Information |

## Real Model Loading Pattern

Model selection must show REAL available models per provider, loaded dynamically from each API — never hardcoded placeholder names.

```python
class ModelFetchThread(QThread):
    """Fetch real models from a provider's API."""
    models_fetched = pyqtSignal(str, list)  # provider_id, models
    fetch_error = pyqtSignal(str, str)       # provider_id, error

    def __init__(self, provider_id: str, config: dict):
        super().__init__()
        self.provider_id = provider_id
        self.config = config

    def run(self):
        try:
            models = self._fetch_models()
            self.models_fetched.emit(self.provider_id, models)
        except Exception as e:
            self.fetch_error.emit(self.provider_id, str(e))
```

### Fetching per provider:

| Provider | Endpoint | Auth | Notes |
|----------|----------|------|-------|
| openai | `/v1/models` | Bearer token | Returns id, owned_by |
| anthropic | `/v1/models` | x-api-key | Returns id, model, context_window |
| google | `/v1/models` | API key in URL | Returns id, displayName, contextWindow |
| openrouter | `/v1/models` | Bearer token | Returns data[].id |
| groq | `/v1/models` | Bearer token | Returns data[].id |
| ollama | `/api/tags` | None (local) | Returns models[].name |
| lmstudio | `/v1/models` | None (local) | Returns data[].id |
| grok | `/v1/models` | Bearer token | Returns data[].id |
| nous | `/v1/models` | Bearer token | Returns data[].id |
| opencode_zen | `/v1/models` | Bearer token | OpenCode Zen API |
| opencode_go | `/v1/models` | Bearer token | OpenCode Go API |
| unsloth | `/v1/models` | Bearer token | Unsloth API |

### Model fetch in Settings:

1. User opens Settings → 🤖 AI Providers tab
2. Click "Fetch Models" for a provider
3. `ModelFetchThread` runs in background (non-blocking)
4. Progress shown in status bar
5. Models populated in dropdown on success
6. Error shown in status bar on failure

## Settings Persistence

```python
# config/settings.json structure
{
    "theme": "midnight",
    "accent_color": "#3b82f6",
    "font_size": 14,
    "animations_enabled": true,
    "default_provider": "openai",
    "providers": {
        "openai": {"api_key": "...", "base_url": "https://api.openai.com/v1"},
        "anthropic": {"api_key": "...", "base_url": "https://api.anthropic.com/v1"}
    },
    "editor": {"tab_size": 2, "word_wrap": true, "line_numbers": true},
    "export": {"format": "html", "minify": true, "inline_css": true}
}
```

## Opening Settings from Main Window

```python
def open_settings(self):
    try:
        from webbuilder.gui.settings_window import SettingsWindow
        dialog = SettingsWindow(self)
        dialog.exec_()
    except Exception as e:
        logger.error(f"Settings dialog failed: {e}")
```

## Settings Window Creation

```python
class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setMinimumSize(750, 550)
        self._settings = SettingsManager()  # loads config/settings.json
        self._setup_ui()
        self._load_current_settings()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(AppearanceTab(), "🎨 Appearance")
        self.tab_widget.addTab(AIProvidersTab(), "🤖 AI Providers")
        self.tab_widget.addTab(EditorTab(), "📝 Editor")
        self.tab_widget.addTab(ExportTab(), "📤 Export")
        self.tab_widget.addTab(PluginsTab(), "🔌 Plugins")
        self.tab_widget.addTab(AboutTab(), "ℹ About")
        layout.addWidget(self.tab_widget)

        btn_layout = QHBoxLayout()
        save_btn = QPushButton("💾 Save")
        save_btn.clicked.connect(self._save_all)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addStretch()
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

    def _save_all(self):
        self._settings.save(self._collect_all_settings())
        self.accept()
```

## Pitfalls

1. **Settings embedded in Properties = rejected**. User explicitly wants a separate Settings button with Settings Window. Properties is for document/project properties; Settings is for application configuration. Never merge them.
2. **PyInstaller caches old .py files**. After rewriting settings modules, kill ALL processes and rebuild clean. Stale cache causes settings changes to not appear.
3. **Model fetch must be async**. Synchronous API calls block the Qt event loop, making the UI freeze. Use QThread with signals for model fetching.
4. **API keys must be persisted securely**. Store in config/settings.json with the API key field. Never hardcode or use placeholder values.
5. **Settings must apply immediately**. Theme changes apply on save; provider changes apply on next chat session. Show a confirmation that settings were saved.
6. **Qt offscreen platform segfault**. Running the GUI in offscreen mode (QT_QPA_PLATFORM=offscreen) causes segfault during WebBuilderWindow creation. This is pre-existing and only affects Linux testing. The Windows .exe is unaffected.
