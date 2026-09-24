# WebBuilder Session Lessons

Lessons learned from building the WebBuilder platform — a next-generation agentic web/app builder.

## File Location

**All WebBuilder files live in `C:\Projects\WebBuilder`, NOT on the Desktop.** The Desktop app (`WebBuilder.exe`) is built from that location. Never leave source files on the Desktop — the Desktop is transient and gets cleaned. If files appear on Desktop, move them to `C:\Projects\WebBuilder` immediately.

**Lesson:** The Desktop is not a project folder. It's a transient location for short-lived files. Project source code belongs in the project folder (`C:\Projects\WebBuilder`). Moving files to the Desktop causes them to be lost when the Desktop is cleaned or the session ends.

## Type System Architecture

The core `types/index.ts` file must define ALL interfaces used across subsystems. Key insight: different subsystems use different subsets of fields, so make fields optional (`field?: type`) unless truly universal. This prevents cascading type errors when one module expects a field another doesn't provide.

**Anti-pattern**: Defining duplicate interfaces in multiple files (e.g., `TypographySystem` in both `types/index.ts` and `generators/typography.ts`). TS2308 errors result. Solution: define once, import everywhere.

**Anti-pattern**: Strict type shapes that don't account for different usage contexts. The `intent/index.ts` generates richer objects than `context/index.ts` expects. Solution: use optional fields extensively.

## AI System Integration

When wiring neural networks to a GUI:
- Training must happen on a background thread or via QTimer callbacks to avoid blocking the UI
- Visual feedback (loss curves, weight distributions) should update after each epoch
- All AI operations need a visual representation — users expect to "see" the AI working

## Desktop App Structure

The three-panel layout (sidebar/canvas/properties) is the standard for builders. Key additions for AI-powered builders:
- Training tab with real-time metrics
- Generator tab with procedural + neural options
- Asset library with search and one-click insert

## Project Generation Pattern

The "Generate Full Project" flow:
1. User describes project in natural language
2. Parse description → extract company name, type, style
3. Look up section list for project type
4. Generate content for each section using ContentGenerator
5. Apply color theme
6. Load all sections into canvas

This pattern enables "accidental creation" — users can generate complete projects with one click.

## Key Technical Decisions

1. **Native AI/ML**: Built from scratch with NumPy — no TensorFlow, PyTorch, or external APIs. Deterministic, reproducible, offline-capable.
2. **FOSS Compliance**: No proprietary dependencies — required by user for F-Droid distribution.
3. **Monorepo**: pnpm workspaces + Turborepo for build orchestration.
4. **Desktop-first**: PyQt5 over Electron for native Windows performance (no browser engine overhead).
5. **Deterministic tools**: All procedural generation accepts seed parameters.

## Build System Pitfalls

- **npm on Windows**: `npm install electron` may fail silently. Download zip manually if needed.
- **MSYS path translation**: Native Windows tools need `C:/Users/...` forward-slash paths, not MSYS `/c/Users/...`.
- **TypeScript barrel exports**: `export * from './module.js'` causes TS2308 when multiple modules export same name. Use explicit exports or rename.
