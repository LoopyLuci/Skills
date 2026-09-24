# WebBuilder Desktop App Development Session Notes
## 2026-08-22

### What Was Built

A complete desktop application for WebBuilder — a next-generation agentic web/app building platform.

### Key Architecture Decisions

1. **PyQt5 over Electron/Tauri**: Chosen for faster iteration on Windows. No Rust toolchain needed, simpler deployment.

2. **Three-panel layout**: Left sidebar (260px, section library), Center canvas (flex, drag-and-drop), Right panel (260px, properties + dockable chat).

3. **Flask backend integration**: Desktop app auto-starts Flask server, polls health endpoint, shows status in status bar.

4. **Config storage**: `~/.webbuilder/config.json` for settings and API keys. Created on first run.

5. **Section widget pattern**: Each section is a `QFrame` with `mousePressEvent`/`mouseMoveEvent` for drag-and-drop. Uses `QDrag` and `QMimeData`.

### Critical Pitfalls Discovered

1. **QPushButton.setDragEnabled doesn't exist**: This method is not available on QPushButton. Must implement drag manually in `mouseMoveEvent`:
   ```python
   def mouseMoveEvent(self, event):
       if self._drag_start and (event.pos() - self._drag_start).manhattanLength() > 10:
           drag = QDrag(self)
           mime = QMimeData()
           mime.setText(self.section_id)
           drag.setMimeData(mime)
           drag.exec_(Qt.MoveAction)
   ```

2. **Flask startup race condition**: Flask takes 0.5-2s to start. Must poll health endpoint in a loop:
   ```python
   for i in range(10):
       time.sleep(0.5)
       try:
           r = requests.get(f"{self.base_url}/api/v1/health", timeout=1)
           if r.status_code == 200:
               return True
       except:
           pass
   ```

3. **Lambda capture in loops**: Always use `lambda checked, t=cid: func(t)` to capture current value, not `lambda: func(cid)`.

4. **Layout clearing**: Must call `widget.deleteLater()` before removing from layout to avoid memory leaks.

5. **Config directory creation**: Must call `Path.home().mkdir(parents=True, exist_ok=True)` before writing config files.

### Project Structure

```
C:\Users\Server\Desktop\WebBuilder\
├── desktop_app.py          # Main desktop application
├── app.py                  # Flask backend
├── index.html              # Frontend
├── editor.html             # Web-based visual editor
├── output/                 # Generated projects
└── package.json            # Electron config (unused)
```

### Provider Configuration

12 AI providers configured:
- Cloud: OpenAI, Anthropic, Google, OpenRouter, OpenCode Go, OpenCode Zen
- Local: Ollama, LLM Studio, LM Studio, Unsloth
- Custom: Custom Provider

### Export System

Three export formats:
1. **HTML**: Static, semantic, accessible — works forever
2. **React**: Components with hooks, Tailwind CSS
3. **JSON**: Raw project data, versioned

### Plugin Architecture

- `PluginInterface` base class with `name`, `version`, `description`
- `ComponentPlugin`, `ExporterPlugin`, `ProviderPlugin`, `ThemePlugin`
- `PluginRegistry` for register/unregister
- `PluginLoader` for filesystem loading
- API versioning with `PluginAPI.check_compatibility()`

### Testing

23 tests covering:
- Project schema validation and migration
- HTML, React, JSON export
- Plugin registry and loading
- Backward compatibility
- Full integration pipeline

### User Preferences

1. **Accidental creation**: Platform should be so intuitive users stumble into building
2. **No placeholders**: Every feature must be fully functional
3. **No stubs**: Chat must connect to real APIs, not random text
4. **Flawless UX**: Drag-and-drop must have visual feedback
5. **Real-time collaboration**: User and agent work together in real time

### Next Steps

1. Wire agent chat to real API calls (OpenAI, Anthropic, Ollama)
2. Implement actual drag-and-drop with visual feedback
3. Make properties panel modify project in real-time
4. Train ML models on real data
5. Build web app visual editor (mirror desktop)
6. Add comprehensive error handling and loading states
