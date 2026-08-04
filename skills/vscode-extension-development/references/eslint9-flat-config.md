# Hardening `npm run lint` for a TypeScript extension (ESLint 9 flat config)

Recipe for taking a repo whose `lint` script references an eslint binary that was never
installed (or an outdated config) to a **passing, meaningful lint gate**. Verified on the
Hermes Agent VS Code extension, July 2026: 89 problems → 0, zero behavior change.

## Setup
```bash
npm install --save-dev eslint@^9 @typescript-eslint/parser@^8 @typescript-eslint/eslint-plugin@^8
```
ESLint 9 uses **flat config** — the CLI is `eslint src` (no `--ext`; that flag was the
eslintrc-era CLI). Update the script:
```json
"lint": "eslint src",
"lint:fix": "eslint src --fix"
```

## Flat config (eslint.config.js, CommonJS)
```js
const tseslint = require('@typescript-eslint/eslint-plugin');
const tsParser = require('@typescript-eslint/parser');
module.exports = [
  { ignores: ['dist/**', 'dist-ts/**', 'node_modules/**', 'scripts/**', '**/*.map'] },
  {
    files: ['src/**/*.ts'],
    languageOptions: {
      parser: tsParser,
      parserOptions: { ecmaVersion: 2022, sourceType: 'module', project: './tsconfig.json' },
    },
    plugins: { '@typescript-eslint': tseslint },
    rules: {
      // Correctness
      '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_', varsIgnorePattern: '^_' }],
      '@typescript-eslint/no-floating-promises': 'error',
      '@typescript-eslint/await-thenable': 'error',
      'no-constant-condition': 'error',
      'no-duplicate-imports': 'error',
      'no-fallthrough': 'error',
      'no-var': 'error',
      'prefer-const': 'error',
      // Event-emitter code (stdin/http/webview callbacks) legitimately passes async
      // fns to void-returning listeners — keep the other misused-promise checks.
      '@typescript-eslint/no-misused-promises': ['error', { checksVoidReturn: false }],
      // Hygiene (off by design in extension code)
      '@typescript-eslint/no-explicit-any': 'off',        // newer VS Code APIs need `as any`
      '@typescript-eslint/no-var-requires': 'off',        // conditional runtime requires
    },
  },
];
```

## Rule-tuning rationale (document these in the config comments)
- **`@typescript-eslint/require-await: 'off'`** — tool registries require every tool handler
  to be `async` (they return Promises) even when some resolve synchronously. Enabling it
  floods the log with false positives on legitimate signatures.
- **`@typescript-eslint/no-misused-promises` with `checksVoidReturn: false`** — event-emitter
  code (`process.stdin.on('data', async ...)`, `http.createServer(async ...)`,
  `req.on('end', async ...)`) is the standard pattern; `checksVoidReturn:false` silences the
  noise while keeping the checks that catch real bugs (promises in conditions, non-void misuse).
- **`no-unnecessary-condition` / `prefer-optional-chain`: 'off'** — defensive `?.`/truthiness
  in config/optional paths is intentional when config shape varies across product versions.
- **No stylistic rules** (semicolons, quotes, spacing) — keep the gate about real issues.

## Dead-code cleanup workflow (89 → 0)
1. Run `npm run lint`, get per-file error groups with `grep -E "^D:|error"`.
2. Run `npm run lint:fix` once — it removes unused eslint-disable directives.
3. Remove genuinely unused imports/vars. **Verify each with grep before deleting** — an
   import listed as unused can still be referenced later in the file (lint reports only
   missed cases). Keep one `import { A, B, type C } from './mod'` to fix no-duplicate-imports.
4. For `catch (err)` where err is unused → `catch {` (ES2019 optional catch binding).
5. For dead assignment flags set-but-never-read (`allSucceeded`), remove the variable AND
   every assignment site — read the surrounding loop first to confirm the flag isn't read
   by behavior you'd break.
6. For API-callback params that must stay for signature compatibility, prefix `_` (the
   argsIgnorePattern allows them): `_messages`, `_token`, `_mcpServer`.
7. After each file: `npx tsc --noEmit` — dead-code removal must never change behavior.
8. Final gates: `npm run lint` exit 0 AND `npx tsc --noEmit` 0 errors AND bundle builds.

## Verification
- `npm run lint` → `exit 0`, no problems listed.
- tsc still clean (removed code was truly dead).
- Rebuild, repackage, reinstall, and grep the shipped bundle to confirm the gate is on new code.
- Quick `node --check` on any hand-edited vanilla JS (webview media) to catch syntax slips
  that tsc doesn't cover.