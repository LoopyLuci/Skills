---
name: frontend-bootstrap
description: "React+Vite+TS from spec. Alias, store, OS gotchas."
category: software-development
tags: [react, typescript, vite, zustand, frontend, windows]
---

# Frontend Application Bootstrap

Turn a design/spec document into a working React+TypeScript+Vite application
that serves correctly in the Hermes preview pane.

## Trigger

Use when:
- A user asks you to build a React frontend from a design doc or spec
- You need to get a Vite + React app running, not just write source files
- TypeScript compilation errors block the dev server
- You're working on a Windows host with MSYS2/bash

## Workflow

### Phase 1: Scaffold

```
mkdir -p web/src/{components/{layout,player,search},store,hooks,utils,styles}
```

Required files:

| Path | Purpose |
|---|---|
| `web/package.json` | react, react-dom, zustand, clsx, tailwind-merge |
| `web/vite.config.ts` | `resolve.alias` for `@/`, server config |
| `web/tsconfig.json` | `paths` must mirror vite config's `resolve.alias` |
| `web/index.html` | Entry point -> `/src/main.tsx` |
| `web/src/main.tsx` | React root render |
| `web/src/App.tsx` | Main app component |
| `web/src/index.css` | Tailwind directives + design tokens |
| `web/src/store/index.ts` | Zustand store(s) |
| `web/src/utils/index.ts` | Utility functions (cn, formatDuration) |

### Phase 2: Alias Configuration

Both files MUST define the same `@/` path mapping. Without both,
`tsc --noEmit` errors with `Cannot find module '@/...'`.

**`vite.config.ts`**
```ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
export default defineConfig({
  plugins: [react()],
  resolve: { alias: { '@': '/src' } },
  server: { port: 3001, host: true },
})
```

**`tsconfig.json`**
```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": { "@/*": ["./src/*"] }
  }
}
```

### Phase 3: Zustand Multi-Interface Store

When one store extends multiple interfaces, shared property names cause
TS1117 ("duplicate property in object literal").

**Fix**: Keep ONE instance of each property name in the initial value,
even if multiple interfaces define it. One `isLoading` serves all:

```ts
// TS1117
{ isLoading: false, /* search */, isLoading: false, /* library */ }

// Works
{ isLoading: false, /* all state */ }
```

Same for functions: if two interfaces define `setLoading`, write it once.

### Phase 4: Install + Launch

```bash
cd web
npm install --prefer-offline --no-audit
npx vite --host 0.0.0.0 --port 3001
```

**npm hangs on Windows**: Kill hung npm, check registry, use a mirror:
```bash
npm config set registry https://registry.npmmirror.com
```

**Port in use**: Vite auto-increments. Read the log for the actual port:
```
VITE v5.x.x  ready in XXX ms
  Local:   http://localhost:3002/
```

### Phase 5: Show Live

```bash
# Check the log for the actual port, then:
open_preview(url="http://localhost:NNNN")

# Verify:
curl -s http://localhost:NNNN/ | grep "<title>"
curl -s -o /dev/null -w "%{http_code}" http://localhost:NNNN/src/App.tsx

# Final check:
npx tsc --noEmit   # must return 0 errors
```

## Windows / MSYS2 Path Translation

MSYS2 translates `/d/...` to `D:\...` when passing to native Windows
executables. This double-translates in Python script paths:

| Symptom | Cause | Fix |
|---|---|---|
| `python3: can't open 'D:\d\...'` | Double translation | Use `D:/forward/slash/paths` |
| `curl: (6) resolution failure` | MSYS2 vs localhost | Use `http://127.0.0.1:NNNN/` |
| `npm ERR! enoent` spawned | Wrong PATH | `cd` before running |

**Rule**: For Python `-c` args use `$PYROOT` set to `D:/path`. For native
CLI args, let bash translate `$ROOT`. When in doubt, `D:/` everywhere.

## CSS Design Token / Theme Systems

Build a complete design token system as CSS custom properties. Import from
`src/index.css` so available to all components:

```
web/src/styles/
├── tokens.css              # Base design tokens (colors, spacing, typography)
├── retro-punk-theme.css    # Full theme with animations, glassmorphism, CRT effects
└── globals.css             # Component-level CSS (or Tailwind)
```

### Token categories

```css
:root {
  /* Primitive colors */
  --punk-pink: #ff6b9d;
  --punk-purple: #c084fc;
  --punk-green: #4ade80;

  /* Semantic surfaces */
  --punk-bg-deep: #0f0a1a;
  --punk-bg-surface: #1a1028;
  --punk-text-primary: #f0e6ff;

  /* Hover / glow variants */
  --punk-pink-hover: #ff8bb0;
  --punk-pink-subtle: rgba(255, 107, 157, 0.12);
  --punk-pink-glow: rgba(255, 107, 157, 0.4);

  /* Gradients */
  --punk-gradient-primary: linear-gradient(135deg, #ff6b9d, #c084fc);
  --punk-gradient-accent: linear-gradient(135deg, #c084fc, #4ade80);
}
```

### Animated frequency bars

```css
@keyframes freq-wave {
  0%, 100% { transform: scaleY(0.3); }
  25% { transform: scaleY(0.8); }
  50% { transform: scaleY(0.5); }
  75% { transform: scaleY(1); }
}
.freq-bar {
  width: 6px; border-radius: 3px;
  animation: freq-wave 1.2s ease-in-out infinite;
}
.freq-bar:nth-child(2n) { animation-delay: -0.2s; }   /* staggered stagger */
```

### Glassmorphism + retro accents

```css
.punk-card {
  background: rgba(42,25,70,0.6);           /* glass */
  backdrop-filter: blur(12px);               /* blur */
  border: 1px solid rgba(255,107,157,0.15);  /* pink border */
  border-radius: 16px;
  transition: all 0.3s cubic-bezier(0.34,1.56,0.64,1);
}
.punk-card:hover {
  border-color: #ff6b9d;
  box-shadow: 0 0 20px rgba(255,107,157,0.3);
}
```

### CRT scanline overlay

```css
.punk-scanlines::after {
  content: '';
  position: fixed; inset: 0;
  pointer-events: none; z-index: 9999;
  background: repeating-linear-gradient(
    0deg, transparent, transparent 2px,
    rgba(0,0,0,0.03) 2px, rgba(0,0,0,0.03) 4px
  );
}
```

## SVG Icon Pack as React Components

Build tree-shakeable icons as React components with `<defs>` + `<linearGradient>`.
No icon font library needed — only shipped icons are bundled.

### Architecture

```
src/assets/Icons.tsx
├── IconBase()             — common wrapper (svg, viewBox, size, children)
├── IconPlay()             — each icon is its own named export
├── IconPause()            — 28+ icons, each with unique gradient ID
└── Icons = { play: IconPlay, ... }  — export map for dynamic lookup
```

### Pattern

```tsx
// Base wrapper
function IconBase({ children, size = 24, viewBox = '0 0 24 24', ...props }) {
  return (
    <svg width={size} height={size} viewBox={viewBox} fill="none" {...props}>
      {children}
    </svg>
  );
}

// Each icon gets a unique gradient ID
export function IconPlay({ size }) {
  return (
    <IconBase size={size} viewBox="0 0 24 24">
      <circle cx="12" cy="12" r="10" stroke="url(#playGrad)" strokeWidth="1.5" />
      <path d="M9.5 7.5L17 12L9.5 16.5V7.5Z" fill="url(#playGrad)" />
      <path d="M18.5 8C19.5 9.2 20 10.5 20 12..." stroke="url(#playGrad)" />
      <defs>
        <linearGradient id="playGrad" x1="0" y1="0" x2="24" y2="24">
          <stop offset="0%" stopColor="#ff6b9d" />
          <stop offset="100%" stopColor="#c084fc" />
        </linearGradient>
      </defs>
    </IconBase>
  );
}
```

### Rules
1. Every icon fits an even `viewBox` (default 24×24) for consistent alignment.
2. Gradient IDs are unique per icon (`#playGrad`, `#pauseGrad`).
3. Sound icons get frequency-wave decorators (arcs, dashed rings, dots).
4. Always include `aria-hidden="true"` or `role="img"` + `aria-label`.

### Frequency-wave motif (add to any icon)

```tsx
<path d="M18 8C19.5 9.5 20 10.8 20 12" stroke="url(#g)" strokeWidth="1.5" strokeLinecap="round" />
<path d="M20 6C22 7.8 22.5 9.5 22.5 12" stroke="url(#g)" strokeWidth="1" opacity="0.5" />
<circle cx="12" cy="12" r="10" stroke="url(#g)" strokeWidth="0.8" strokeDasharray="2 3" />
```

## Adaptive UI Patterns (Command Palette + Search Overlay)

SovereignStream uses zero-click intelligence:

| Pattern | Trigger | Behavior |
|---|---|---|
| Command Palette | Ctrl+K or `/` | Full overlay: search all entities, commands, settings |
| Search Overlay | Click search bar or Ctrl+F | Tab-filtered search (All/Tracks/Albums/Artists/Videos) |
| Keyboard Nav | Arrow keys + Enter | `role="listbox"` + `role="option"` on results |

### Command palette wiring

```tsx
// Toggle via Ctrl+K
useEffect(() => {
  const handleKeyDown = (e: KeyboardEvent) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') { e.preventDefault(); toggle(); }
    if (e.key === 'Escape') setOpen(false);
  };
  window.addEventListener('keydown', handleKeyDown);
  return () => window.removeEventListener('keydown', handleKeyDown);
}, [isOpen]);
```

### Accessibility
- Dialog: `role="dialog"` + `aria-modal="true"`
- Results list: `role="listbox"` + `aria-label`
- Each item: `role="option"` + `aria-selected`
- Input: `autoComplete="off"`, `autoFocus` on mount

## Verification Gates

Before declaring success:
1. `npx tsc --noEmit` -> 0 errors
2. All component URLs return HTTP 200
3. `open_preview()` shows non-blank content
4. Ctrl+K opens and searches without console errors
