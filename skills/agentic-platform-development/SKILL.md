---
name: agentic-platform-development
description: Build web platforms where AI agents are first-class via MCP.
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [agentic, mcp, monorepo, code-generation, visual-editor, web-builder]
---

# Agentic Platform Development

Build web platforms where AI agents (Hermes, Claude, Codex) are first-class citizens — not bolted-on assistants. Covers monorepo architecture, MCP server integration, code generation pipelines, and visual editor construction.

## Trigger

Use when the user wants to build:
- A platform where AI agents can create/edit/deploy web projects via MCP
- MCP server implementations that expose tools to agents
- Code generation pipelines that convert structured specs into working projects
- Visual editors (browser-based drag-and-drop) for web page building
- Multi-agent orchestration systems for web development

## Architecture

The canonical structure for an agentic web platform:

```
platform/
├── packages/
│   ├── core/           ← All engines (intent, context, component, design, logic, deploy)
│   ├── mcp-server/     ← MCP protocol bridge (tools, resources, prompts)
│   ├── agents/         ← Specialized AI agents + orchestrator
│   ├── components/     ← Reusable UI component library
│   ├── cli/            ← Developer command-line interface
│   ├── plugins/        ← Extensibility SDK + marketplace
│   ├── testing/        ← Test generation + execution
│   └── ai/             ← Model management + prompt templates
├── apps/
│   ├── web/            ← Visual editor + dashboard
│   └── playground/     ← Live demo
└── examples/           ← Starter templates
```

## Monorepo Setup (pnpm + turbo + TypeScript)

### Root package.json

```json
{
  "name": "platform-name",
  "private": true,
  "workspaces": ["apps/*", "packages/*"],
  "devDependencies": { "turbo": "^2.0.0", "typescript": "^5.4.0" },
  "packageManager": "pnpm@9.0.0"
}
```

### pnpm-workspace.yaml

```yaml
packages:
  - 'apps/*'
  - 'packages/*'
```

### turbo.json (v2 uses `tasks`, NOT `pipeline`)

```json
{
  "$schema": "https://turbo.build/schema.json",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**", "!.next/cache/**"]
    },
    "dev": { "cache": false, "persistent": true },
    "test": { "dependsOn": ["build"] },
    "typecheck": {},
    "clean": { "cache": false }
  }
}
```

**PITFALL:** turbo v2 renamed `pipeline` to `tasks`. Using `pipeline` causes: `Found pipeline field instead of tasks. Rename pipeline field to tasks.`

### Package exports pattern

```json
{
  "main": "./dist/index.js",
  "module": "./dist/index.mjs",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "import": "./dist/index.mjs",
      "require": "./dist/index.js",
      "types": "./dist/index.d.ts"
    }
  }
}
```

Build: `tsup src/index.ts --format cjs,esm --dts`

### TypeScript path aliases (root tsconfig.json)

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@scope/core": ["packages/core/src"],
      "@scope/core/*": ["packages/core/src/*"]
    }
  }
}
```

## Iterative Build Error Fixing

The dominant pattern in platform development: run build → read errors → patch → repeat.

**Workflow:**
1. `pnpm --filter @scope/package build`
2. Read first error (usually TypeScript type mismatch)
3. `patch` tool to fix specific line
4. Re-run build
5. Repeat until clean

**Common error patterns:**

| Error | Fix |
|-------|-----|
| `Module './x.js' has no exported member 'Y'` | Change to `import { default as Y } from './x.js'` or fix export |
| `Type 'string' is not assignable to type 'number'` | Interface may need `Record<string, string>` not `Record<string, number>` |
| `'mobile' does not exist in type` | Use `Record<string, string>` for flexible keys |
| `Duplicate identifier 'X'` | Remove re-export when using `export *` |
| `Cannot find module 'nanoid'` | Add to dependencies, `pnpm install` |
| `Expected 2-3 arguments, but got 4` | Check function signature — subagent code often wrong arg count |

**PITFALL:** Mixing `export * from './x.js'` with explicit `export { X } from './x.js'` causes duplicate identifier errors. Use one or the other.

## PyQt5 Desktop App Development (From Scratch)

When building a native web builder app (not wrapping), use PyQt5 with pure Qt widgets.

### Architecture

```python
class WebBuilderWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._scaling = get_scaling_engine()
        self._scaling.initialize()
        self.setup_ui()
        self.setup_menu()

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        
        # Three-panel layout
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.create_sidebar())   # Fixed min/max
        splitter.addWidget(self.create_canvas())     # Expanding
        splitter.addWidget(self.create_properties())
        splitter.setSizes([220, 900, 280])
        layout.addWidget(splitter)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._scaling.on_window_resize(event.size().width(), event.size().height())

    def moveEvent(self, event):
        super().moveEvent(event)
        screen = QApplication.screenAt(event.pos())
        if screen and screen != QApplication.primaryScreen():
            self._scaling.on_screen_changed()
```

### Adaptive Scaling Engine

DPI-aware scaling that adapts to any screen:

```python
class ScalingEngine:
    def detect_screen(self) -> ScreenInfo:
        screen = QApplication.primaryScreen()
        dpi = 96
        for method in ('logicalDotsPerInch', 'physicalDotsPerInch'):
            try:
                dpi = int(getattr(screen, method)())
                break
            except: continue
        return ScreenInfo(dpi=dpi, ...)
    
    def calculate_metrics(self, w, h) -> LayoutMetrics:
        sf = self._scale_factor
        return LayoutMetrics(
            font_size=int(13 * sf),
            sidebar_width=max(180, int(w * 0.18)),
            right_panel_width=max(240, int(w * 0.20)),
            spacing=int(8 * sf),
        )
```

**PITFALL:** `screen.logicalDotsPerInch()` fails on headless/offscreen sessions. Wrap in try/except with fallback to 96.

### PyInstaller Packaging

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

**PITFALL:** `PermissionError: Access is denied` on exe rebuild — previous process still running. Kill with `taskkill /F /IM WebBuilder.exe` before rebuilding.

**PITFALL:** Import caching causes stale modules in exe. Delete `dist/` and `build/` directories before rebuilding after major module changes.

**PITFALL:** exe size starts at 130MB+. Reduce with `--exclude-module` for unused stdlib modules (matplotlib, numpy, pandas, scipy, tkinter, unittest, pytest, setuptools, pip, wheel). Target: <50MB.

### Hardware Abstraction Layer

Multi-threading + multi-GPU support:

```python
class HardwareDetector:
    def detect(self):
        info = HardwareInfo()
        info.cpu = self._detect_cpu()
        info.memory = self._detect_memory()
        info.gpus = self._detect_gpus()  # NVIDIA/AMD/Intel/Apple
        return info

class TaskScheduler:
    def __init__(self):
        info = get_hardware_info()
        self._thread_pool = ThreadPoolExecutor(
            max_workers=info.cpu.optimal_thread_count
        )
        self._gpu_manager = GPUManager()
```

**PITFALL:** GPU detection via `pynvml` requires NVIDIA drivers. Gracefully fall back to CPU-only mode when no discrete GPU is found.

### Plugin System v2

Hot-reload plugins with sandboxed execution:

```python
class PluginManager:
    def load_plugin(self, plugin_id: str) -> bool:
        spec = importlib.util.spec_from_file_location(
            f"plugin_{plugin_id}", str(entry)
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        instance = plugin_class()
        instance.initialize(PluginAPI(self, plugin_id))
    
    def _check_watches(self):
        # Auto-reload on file change (every 2s)
        for plugin in self._plugins.values():
            if entry.stat().st_mtime > plugin.last_modified:
                self.reload_plugin(plugin.id)
```

### 50+ Module Ecosystem Pattern

For a production-grade web builder:

```
webbuilder/
├── hardware/          # Multi-threading + multi-GPU
├── mcp/               # Model Context Protocol
├── ai/                # Providers, GPU accelerator, cache, features
├── core/              # SQLite backend
├── assets/            # Image pipeline, lazy loading
├── plugins/           # Plugin system v2
├── gui/               # Adaptive main window, dialogs
├── design/            # Color, typography, animation, tokens
├── ecommerce/         # Catalog, cart, orders, tax, shipping
├── seo/               # Meta tags, sitemap, robots.txt, Schema.org
├── content/           # Rich text, media library, newsletters
├── security/          # CSP, headers, CSRF, GDPR, scanner
├── devtools/          # Git, API tester, DB builder, profiler
├── performance/       # CSS/JS minifier, service worker, PWA
├── validation.py      # XSS, path traversal, API key
├── accessibility.py   # WCAG, screen reader
├── i18n.py            # Internationalization
├── search.py          # Full-text + fuzzy search
└── sync.py            # Cloud sync, operational transform
```

**PITFALL:** `field(default_factory=list)` — the parentheses matter. `field(default_factory=list)` is correct (passes the list type as callable). `field(default_factory=list())` fails at module load with `'list' object is not callable` because `list()` returns an empty list, not a callable.

**PITFALL:** When adding many new modules, old `.pyc` files in `__pycache__` directories can cause stale imports. Delete `__pycache__` directories when modules fail to import correctly after refactoring.

## MCP Server Implementation

Use `@modelcontextprotocol/sdk` for the server, `zod` for input schemas.

```typescript
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';

const server = new McpServer({ name: 'my-server', version: '1.0.0' });

server.registerTool(
  'tool/name',
  {
    description: 'What this tool does',
    inputSchema: {
      param1: z.string().describe('Description'),
      param2: z.number().optional().describe('Optional'),
    },
  },
  async ({ param1, param2 }) => {
    return {
      content: [{ type: 'text' as const, text: JSON.stringify(result) }],
    };
  }
);

const transport = new StdioServerTransport();
await server.connect(transport);
```

**Key points:**
- Tool names MUST use underscores: `webbuilder_project_create` (NOT slashes)
  - Names with `/` trigger validation warnings: `Tool name contains invalid characters`
  - MCP naming standard allows: A-Z, a-z, 0-9, underscore, dash, dot
- Always return `{ content: [{ type: 'text', text: ... }] }`
- Use `z.enum(['a', 'b'])` for fixed options
- Wrap tool registration in private methods: `registerProjectTools()`, etc.
- Keep handler implementations lean — delegate to core package functions

## Code Generation Pipeline

Convert structured specs into working code files:

1. **Intent Parser** — Natural language → structured spec (goals, constraints, pages, design, features)
2. **Component Code Generator** — Spec sections → real React component files with JSX + Tailwind
3. **Content Generator** — Spec sections → realistic content (features, pricing, nav items)
4. **Project Scaffolder** — All files + configs (package.json, tsconfig, tailwind, postcss, gitignore)

**Pattern:** Each generator produces `FileChange[]`:

```typescript
interface FileChange {
  path: string;      // Relative path from project root
  content: string;   // File content
  action: 'create' | 'update' | 'delete';
}
```

Write to disk:

```typescript
for (const file of generated.files) {
  const filePath = join(targetDir, file.path);
  const dir = join(filePath, '..');
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
  writeFileSync(filePath, file.content);
}
```

## Visual Editor Architecture

Browser-based drag-and-drop editor:

```
editor/
├── index.tsx          ← EditorProvider context (state, selection, history)
├── Canvas/            ← Renders sections, click-to-select, responsive preview
├── Sidebar/           ← Component palette + page structure tree
├── Properties/        ← Edit selected component's props
├── Toolbar/           ← Viewport switcher, zoom, undo/redo, deploy
└── AI/                ← Chat interface for natural language editing
```

**State (use React Context, not just hooks):**

```typescript
interface EditorState {
  spec: ProjectSpec;
  selectedSectionId: string | null;
  viewport: 'desktop' | 'tablet' | 'mobile';
  zoom: number;
  history: ProjectSpec[];
  historyIndex: number;
}
```

**Rendering:** Each section type gets a renderer returning JSX with Tailwind. Click handlers set `selectedSectionId`. Selection shows ring + label + delete button.

### Drag-and-Drop with @dnd-kit

Install: `pnpm --filter @scope/web add @dnd-kit/core @dnd-kit/sortable @dnd-kit/utilities`

**Components:**

1. **DraggableComponent** — Sidebar items that can be dragged:
```typescript
import { useDraggable } from '@dnd-kit/core';
import { CSS } from '@dnd-kit/utilities';

const { attributes, listeners, setNodeRef, transform, isDragging } = useDraggable({
  id: 'unique-id',
  data: { type: 'hero', name: 'Hero Section' },
});

const style = { transform: CSS.Translate.toString(transform) };
```

2. **SortableSection** — Canvas items that can be reordered:
```typescript
import { useSortable } from '@dnd-kit/sortable';

const { attributes, listeners, setNodeRef, transform, transition, isDragging } = useSortable({ id: section.id });
```

3. **DropZone** — Visual feedback when dragging over canvas:
```typescript
import { useDroppable } from '@dnd-kit/core';

const { setNodeRef } = useDroppable({ id: 'canvas-dropzone' });
```

4. **DragOverlay** — Preview following cursor during drag

**Sensors:**
```typescript
import { PointerSensor, KeyboardSensor } from '@dnd-kit/core';
import { sortableKeyboardCoordinates } from '@dnd-kit/sortable';

const sensors = useSensors(
  useSensor(PointerSensor, { activationConstraint: { distance: 8 } }),
  useSensor(KeyboardSensor, { coordinateGetter: sortableKeyboardCoordinates })
);
```

**PITFALL:** Wrap canvas items in `<SortableContext items={sectionIds} strategy={verticalListSortingStrategy}>`. Without this, drag-to-reorder won't work.

### Toast Notification System

Use CustomEvent for cross-component toast notifications:

```typescript
// ToastContainer.tsx
export function showToast(type: 'success' | 'error' | 'info' | 'warning', message: string) {
  const event = new CustomEvent('webbuilder-toast', { detail: { type, message } });
  window.dispatchEvent(event);
}

export function ToastContainer() {
  const [toasts, setToasts] = useState<Toast[]>([]);

  useEffect(() => {
    const listener = (e: Event) => {
      const { type, message } = (e as CustomEvent).detail;
      const id = Date.now().toString(36);
      setToasts(prev => [...prev, { id, type, message }]);
      setTimeout(() => setToasts(prev => prev.filter(t => t.id !== id)), 3000);
    };
    window.addEventListener('webbuilder-toast', listener);
    return () => window.removeEventListener('webbuilder-toast', listener);
  }, []);

  return (
    <div className="fixed bottom-4 right-4 z-[100] flex flex-col gap-2" aria-live="polite">
      {toasts.map(toast => (
        <div key={toast.id} role="alert" className={`animate-slide-up ${/* type styles */}`}>
          {toast.message}
        </div>
      ))}
    </div>
  );
}
```

### Emulator Component Pattern

For building realistic device emulators:

```
emulator/
├── DeviceFrame.tsx    ← Phone hardware (notch, bezels, side buttons)
├── StatusBar.tsx      ← Live clock, battery, WiFi, signal
├── NavigationBar.tsx  ← Back, Home, Recent buttons
├── AppPreview.tsx     ← Shows generated app content
└── Emulator.tsx       ← Orchestrates all + controls (power, rotate, device select)
```

**DeviceFrame:** Use rounded corners (`rounded-[3rem]`), camera notch (absolute positioned div), side buttons (absolute positioned with `-left-1`, `-right-1`).

**StatusBar:** Live clock with `setInterval`, battery indicator with dynamic width.

**AppPreview:** Render different content based on `components` array prop — conditionally show buttons, text, cards, images, lists.

## GitHub SSH Setup (Windows)

1. `ssh-keygen -t ed25519` → `~/.ssh/id_ed25519` + `.pub`
2. `~/.ssh/config`:
   ```
   Host github.com
     HostName github.com
     User git
     IdentityFile ~/.ssh/id_ed25519
     IdentitiesOnly yes
   ```
3. `ssh-keyscan github.com >> ~/.ssh/known_hosts`
4. Add public key to GitHub → Settings → SSH and GPG keys
5. `ssh -T git@github.com` → "Hi username! You've successfully authenticated"

**PITFALL:** SSH connection hangs on Windows. Add `ssh-keyscan` to populate `known_hosts` first.

## .gitignore for Monorepo

```
node_modules
.next
dist
.turbo
*.log
.DS_Store
.env*.local
.vscode
.idea
*.tsbuildinfo
```

**PITFALL:** `git add -A` without `.gitignore` stages `node_modules` (causes "Filename too long" warnings on Windows). Create `.gitignore` BEFORE `git add`.

## 100-Year Architecture for Agentic Web Platforms

For platforms meant to evolve for decades:

1. **Zero dependencies in core**: The core package (`packages/core/` or `webbuilder/core/`) must depend ONLY on language standard library. External libraries disappear, break, change licenses. The core should run decades from now.

2. **Everything is a plugin**: Features beyond core are plugins. Plugins can be added, removed, or replaced without touching the core. The core stays small and stable.

3. **Open, human-readable formats**: Native storage uses open formats (JSON with schema versioning). Every object has `_schema` and `_version` fields for future migration and external tool interoperability.

4. **Self-describing data**: All models implement `to_dict()` and `from_dict()` with schema identifiers. No separate schema files that can get lost.

5. **Composability over monoliths**: Small, focused tools that compose. The Unix philosophy: each tool does one thing well.

6. **Deterministic behavior**: Same input → same output. No random IDs (use content hashes), no timestamps in output unless requested.

7. **Community governance**: The platform should be governable by its community, not controlled by a single entity.

## Simplification Workflow

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

## Pitfalls

1. **turbo v2 `tasks` vs `pipeline`**: Always use `tasks` in turbo.json v2+
2. **Duplicate exports**: Don't mix `export *` with explicit exports of same name
3. **Type strictness**: Use `Record<string, string>` for flexible prop objects
4. **Missing dependencies**: "Cannot find module 'X'" → add to package.json + `pnpm install`
5. **Subagent-generated code**: Often has wrong import paths or arg counts. Verify before building.
6. **Next.js module resolution**: Use `@/...` path aliases, not relative `../` in page imports
7. **SSH host key verification**: Run `ssh-keyscan github.com >> ~/.ssh/known_hosts` before first connection
8. **Windows line endings**: Git warns about LF→CRLF. Harmless, can be ignored.
9. **Duplicate component directories**: When using subagents, they may create components in `apps/web/components/ui/` while you manually create in `apps/web/src/components/ui/`. Consolidate to `src/components/ui/` and delete the other.
10. **Toast event listeners**: Use module-level listener array for cross-component toasts. Don't try to export/import state between ToastProvider and consuming components — use CustomEvent on `window`.
11. **Optional dependencies**: Wrap imports in try/except for packages that may not be installed (e.g., `paramiko`, `flask`). Set to `None` on import failure and check before use.
12. **Module relocation**: When moving modules to `contrib/`, update ALL import paths. Use `search_files` to find references before moving.
