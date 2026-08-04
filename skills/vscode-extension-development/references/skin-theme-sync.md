# Skin/Theme Sync → Webview CSS Custom Properties

Syncing an app-owned skin/theme engine (e.g. Hermes CLI's YAML skins, TUI palettes)
onto an extension webview via a CSS-custom-property **override layer**, so the
extension renders with the exact same palette as the rest of the product, from one
source of truth. Verified against the Hermes skin engine (`hermes_cli/skin_engine.py`)
on Windows, VS Code 1.131, July 2026.

## Resolution model (mirror upstream, don't re-derive)
1. **Active skin name** comes from the app's own config: `config.yaml` → `display.skin`
   (default `'default'`). There is no separate extension copy — read the product config.
2. **Built-in presets** (`default`, plus alternatives such as `ares`/`mono`/`slate`/`daylight`)
   are compiled into the module as `Record<string, BuiltinSkin>` where a `BuiltinSkin =
   { name, description, colors, light_colors? }`. Compiling avoids parsing the upstream
   language-specific engine source at runtime.
3. **User skins** live in `<app-home>/skins/*.yaml`. Merge order = start from the DEFAULT
   preset, then apply the matched user skin's `colors`/`light_colors` over it. Unset keys
   fall back to the built-in. Parse YAML with a real dep (`js-yaml`) + a tiny regex fallback
   parser for hosts where it's unavailable.
4. **Polarity**: `colors` is the dark-authored block, `light_colors` the optional light
   variant. Pick by the host's active theme:
   `vscode.window.activeColorTheme.kind === ColorThemeKind.Light`.

```ts
export interface BuiltinSkin {
  name: string;
  description: string;
  colors: Record<string, string>;
  light_colors?: Record<string, string>;
}

function pickPalette(skin, light) {
  const base = { ...skin.colors };
  if (light && skin.light_colors) return { ...base, ...skin.light_colors };
  return base;
}
```

## Map skin semantics → your UI's CSS vars
`paletteToCssVars(palette, dark)` returns the webview's `:root` override set. Derive full
surface ladders and alpha variants from a single source color rather than hardcoding every
shade:
- `shade(hex, factor)` — scale RGB by 0.88–1.32 to build `--bg-secondary/tertiary/elevated`.
- `withAlpha(hex, a)` — to `rgba(...)` for `--accent-muted`, `--border-*`, `--shadow-accent`.

Typical mapping:
| skin key | css var |
|---|---|
| `ui_accent` | `--accent`, `--accent-hover` |
| `banner_title` | `--accent-light` |
| `status_bar_bg` | `--bg-primary` (+ derived ladders) |
| `banner_text`/`prompt` | `--text-primary` |
| `session_label`/`status_bar_strong` | `--text-secondary` |
| `banner_dim` | `--text-muted` |
| `ui_ok`/`ui_error`/`ui_warn` | `--success`/`--error`/`--warning` |
| `shell_dollar` | `--info` |
| `response_border` | `--border-*` |

## Apply in the webview (override, not rewrite)
Webview handler writes each var on `document.documentElement` via `style.setProperty`.
Structural design is preserved; only colors are themed. Request once on init
(`vscode.postMessage({ type: 'getSkin' })`).

```js
function applySkin(cssVars) {
  const root = document.documentElement;
  for (const [name, value] of Object.entries(cssVars)) {
    if (typeof value === 'string' && value) root.style.setProperty(name, value);
  }
  document.body.classList.add('hermes-skin-applied');
}
```

## Live sync
- **Config changes**: upstream already emits `onConfigChanged` when `config.yaml` changes —
  on that event, re-resolve the skin name and re-push (handles `display.skin` edits).
- **Skin-file changes**: `fs.watch(<home>/skins, cb)`; re-resolve+emit on any `*.yaml` change.
- **Polarity changes**: `vscode.window.onDidChangeActiveColorTheme` → re-resolve+emit.

## Pitfalls
- **`import * as vscode` at top level breaks pure-Node unit tests.** Use a lazy accessor and
  guard the polarity lookup in try/catch. It keeps the module importable outside the host:
  ```ts
  function getVscode() { try { return require('vscode'); } catch { return null; } }
  ```
- **Constructor injection, not assignable getter, for tests.** A read-only
  `get skinsDir()` that you then "assign over" in a test silently does nothing.
  Accept `constructor(homeOverride?)` so tests can point at a temp `<home>/skins/`.
- **The `skins/` dir may not exist yet** — `fs.mkdirSync(recursive)` before watching, and
  make the watcher best-effort (`null` on failure; resolution still works on demand).
- **Unknown/typo skin name** → fall back to `default`, never throw.
- **`fs.watch` on a dir can be flaky** — still rely on `resolve()` being callable on demand.
- **Test checklist**: all built-ins resolve with full var set; dark≠light palettes; user YAML
  overrides `colors` but falls back to built-in for unset keys; unknown→default; module imports
  in pure Node.