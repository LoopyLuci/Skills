# WebBuilder Build & Integration Lessons

Real-world lessons from building the WebBuilder agentic platform (MCP-first, 10 packages, 52+ components).

## Build Hygiene

### Duplicate Compiled Files in `src/`
**Symptom**: `Duplicate page detected. pages/index.js and pages/index.tsx resolve to /` or build errors referencing stale exports.
**Cause**: tsup/esbuild emits `.js`/`.d.ts`/`.js.map`/`.d.ts.map` files alongside `.ts` sources on first build. These persist and cause conflicts on subsequent builds.
**Fix**: Always exclude compiled files from `src/` in `.gitignore` and clean before major rebuilds:
```bash
find packages apps -path "*/src/*.js" -o -path "*/src/*.d.ts" -o -path "*/src/*.js.map" -o -path "*/src/*.d.ts.map" | grep -v node_modules | xargs rm -f
```

### Circular Dependencies in ESM Build
**Symptom**: `Class extends value undefined is not a constructor or null` at runtime, even though TypeScript compiles fine.
**Cause**: When a file both exports a base class AND imports subclasses that extend it (for a factory function), ESM evaluation order can cause the base class to be undefined when the subclass is evaluated.
**Fix**: Split base class and factory into separate files:
- `Deployer.ts` — exports `abstract class Deployer`
- `factory.ts` — imports `Deployer` + subclasses, exports `createDeployer()`
- `DeployEngine.ts` — imports `createDeployer` from `./factory.js`

### Stale Build Cache
**Symptom**: Build errors reference code that no longer exists in source files.
**Cause**: esbuild caches `.js` files in `src/` from previous builds.
**Fix**: `rm -rf dist && pnpm build` after significant structural changes.

## MCP Server Integration

### Registration Requires Restart
Adding MCP servers to `~/.hermes/config.yaml` does NOT hot-reload. Hermes must be restarted to discover new servers.

### Direct Function Testing > JSON-RPC for Rapid Iteration
Testing MCP tools via `require('./dist/index.js')` and calling functions directly is faster and more reliable than JSON-RPC stdio testing. Build a comprehensive Node.js test harness:

```javascript
const core = require('./packages/core/dist/index.js');
const result = core.parseIntent('Build a landing page');
const generated = core.generateCode(result.spec);
// Assert on results
```

### Tool Naming Convention
MCP tools registered with Hermes follow: `mcp_{server_name}_{tool_name}` (hyphens/dots → underscores).

### Stdio Transport
MCP servers communicate via stdin/stdout JSON-RPC 2.0. Log to **stderr** only — stdout is reserved for protocol messages.

## Platform Architecture Patterns

### Intent Parsing
Natural language → structured spec works well for project scaffolding. The parser extracts goals, constraints, pages, design preferences, and features from descriptions like "Build a landing page for my SaaS with hero, features, pricing."

### Code Generation Pipeline
```
Description → parseIntent() → ProjectSpec → generateCode() → FileChange[] → write to disk
```

### Generated Project Output
A complete Next.js project with:
- `package.json`, `tsconfig.json`, `next.config.js`, `tailwind.config.js`
- `src/app/layout.tsx`, `src/app/globals.css`
- `src/pages/index.tsx`
- `src/components/{HeroDefault,FeaturesDefault,PricingDefault,...}.tsx`
- `src/styles/tokens.json`

### MCP Tool Catalog
| Category | Tools |
|----------|-------|
| Project | create, list, get, delete |
| CodeGen | generate |
| Component | search, add |
| Design | generate, apply-theme |
| Deploy | preview, production |
| Testing | generate, run |
| Optimize | performance, accessibility, seo |
| Android | create, components, devices |

### Android Project Generation
Uses `AndroidProjectGenerator` with config: name, packageName, SDK versions, activities, permissions. Generates Gradle build files, AndroidManifest.xml, Kotlin sources, Compose UI.

### Multi-Framework Support
Framework adapters (Vue, Svelte, iOS/SwiftUI, Flutter) convert WebBuilder specs to framework-specific code. Each adapter accepts a `ProjectSpec` and generates appropriate component code.

## Testing Strategy

### 45 Tests Across 11 Groups
1. Project Creation (parseIntent)
2. Code Generation (generateCode)
3. Project Management (CRUD)
4. Design Engine (tokens, color, typography)
5. Deploy Engine (config, validation)
6. Android Tools (components, devices)
7. Content Generation (pages, navigation)
8. Logic Engine
9. Observability Engine
10. Component Engine
11. Context Manager

### E2E Pipeline Test
Full workflow: intent → project → code generation → file output → verification.

## Common User Preferences (from session)

- **Exhaustive scope**: User consistently asks for "all" features and "complete" implementation
- **Working artifacts over plans**: User demands compiled APKs, passing tests, real tool output
- **Honest assessment**: User values honest "current state vs. flawless" evaluation over false confidence
- **Regular next-step recommendations**: User asks "what are optimal next steps?" with codebase-grounded reasoning
