# Desktop App Wrapping for Visual Editors

When the user wants a native desktop app (not browser), wrap the web editor in a native shell.

## Three Approaches (Ranked by Reliability)

### 1. PyQt5 (Python — MOST RELIABLE)

When Electron/Tauri fail, PyQt5 is the most reliable cross-platform desktop approach.

```bash
pip install PyQt5 PyQtWebEngine
```

**Advantages:**
- No build tools needed (no Visual Studio, no Rust toolchain)
- Single `python main.py` to run
- Native Qt widgets + WebEngine for web content
- Works on Windows, macOS, Linux

**Hybrid approach** — Use Qt widgets for the shell (toolbar, sidebar, properties) and a `QWebEngineView` for the canvas preview. This gives native performance + web rendering.

**Pure-Qt approach** — Build the entire UI with Qt widgets (no webview). More work but fully native.

```python
from PyQt5.QtWidgets import QApplication, QMainWindow, QSplitter, QFrame, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt

class WebBuilderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('WebBuilder')
        self.resize(1600, 1000)
        
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.create_sidebar())   # 220px
        splitter.addWidget(self.create_canvas())     # flex
        splitter.addWidget(self.create_properties()) # 280px
        splitter.setSizes([220, 900, 280])
        self.setCentralWidget(splitter)
```

### 2. Electron (HTML/CSS/JS)

```bash
# Create standalone project (outside pnpm workspace to avoid workspace protocol conflicts)
mkdir -p ~/Desktop/App && cd ~/Desktop/App
npm init -y
npm install electron
```

**PITFALL (Windows):** `npm install electron` inside a pnpm workspace fails with `Unsupported URL Type "workspace:*"`. Create the desktop app OUTSIDE the workspace, or use a `.npmrc` with `link-workspace-packages=false`.

**PITFALL (Windows):** Electron postinstall may fail with `install-scripts blocked`. Run:
```bash
npm install-scripts approve electron
# or
npm config set ignore-scripts false
```

**main.js structure:**
```javascript
const { app, BrowserWindow } = require('electron');
// Disable GPU sandbox issues
app.commandLine.appendSwitch('no-sandbox');
app.commandLine.appendSwitch('disable-gpu-sandbox');

function createWindow() {
  const win = new BrowserWindow({
    width: 1600, height: 1000,
    minWidth: 1200, minHeight: 700,
    backgroundColor: '#0f172a',
    show: false,  // Prevent flash
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: false
    }
  });
  win.once('ready-to-show', () => win.show());
  win.loadFile('index.html');  // or loadURL('http://localhost:3001')
}
```

**preload.js** — use `contextBridge.exposeInMainWorld` for secure IPC.

### 3. Tauri v2 (Rust + Webview)

```bash
cargo install tauri-cli
cargo tauri init
```

**PITFALL:** Requires Visual Studio C++ build tools on Windows. Install via:
```bash
winget install Microsoft.VisualStudio.2022.BuildTools
```
If `cargo build` fails with `could not compile serde_core` → missing build tools.

**tauri.conf.json** — set `frontendDist` to `./src-tauri` for static HTML, or use `beforeDevCommand` + `devUrl` for dev server.

## Desktop App Architecture (Three-Panel)

```
┌─────────────────────────────────────────────────────┐
│ Top Bar: Logo | Project Name | Undo | Preview | Deploy │
├──────────┬────────────────────────┬─────────────────┤
│ Sidebar  │ Canvas (white page)    │ Properties      │
│          │                        │ Panel           │
│ Components│ ┌──────────────────┐  │                 │
│ - Hero   │ │  Section 1       │  │ Type: Hero      │
│ - Features│ │  Section 2       │  │ Title: [____]   │
│ - Pricing│ │  Section 3       │  │ Subtitle:[___]  │
│ - CTA    │ └──────────────────┘  │ Color: [____]   │
│          │                        │ [Delete]        │
├──────────┴────────────────────────┴─────────────────┤
│ Status Bar: Ready | Desktop (1200px) | 3 sections   │
└─────────────────────────────────────────────────────┘
```

**Key UX rules:**
- Canvas = white rounded rectangle with shadow (page preview)
- Click section to select → show blue ring + controls
- Properties panel updates in real-time as you edit
- Viewport switcher (Mobile/Tablet/Desktop) resizes canvas
- Status bar shows live feedback (action performed, viewport, section count)

## User Feedback Signals

- **"It is completely broken and nothing works"** → UI is not rendering correctly. Common causes: missing CSS, broken JavaScript syntax, missing component imports.
- **"Ensure everything is properly designed"** → User expects complete, polished UI with no placeholders or stubs.
- **"Properly designed, developed, built up, built out"** → User wants full feature coverage, not just the basics.
- **"no placeholders, stubs, bugs, errors or gaps"** → Ship only when fully working.
- **"I do not want the browser tested, I want the Tauri Desktop app"** → User specifically wants a native desktop application, not a web app.