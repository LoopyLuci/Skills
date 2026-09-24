# MCP Tool Name Pitfall

**Problem:** Tool names like `webbuilder/project/create` trigger validation warnings and may be rejected by some MCP clients.

**Root cause:** The MCP SDK validates tool names against `A-Z, a-z, 0-9, underscore (_), dash (-), and dot (.)`. The `/` character is technically allowed by the spec but generates warnings:
```
Tool name validation warning for "webbuilder/project/create":
  - Tool name contains invalid characters: "/"
  - Allowed characters are: A-Z, a-z, 0-9, underscore (_), dash (-), and dot (.)
```

**Fix:** Replace `/` with `_` in tool names:
- `webbuilder/project/create` → `webbuilder_project_create`
- `webbuilder/codegen/generate` → `webbuilder_codegen_generate`
- `webbuilder/design/generate` → `webbuilder_design_generate`

**Discovery path in this session:**
1. Built MCP server with `/` separated names
2. Verified tools registered and functioned correctly
3. Saw validation warnings in stderr
4. Initially dismissed as non-fatal
5. User chose to fix proactively
6. Renamed all 18 tools to use underscores
7. Rebuilt — zero warnings, same functionality

**Lesson:** Validation warnings are signals of potential compatibility issues. Fix them early rather than shipping with warnings.

## Related Pitfalls

### Circular Dependency in Deploy Package
When `DeployEngine.ts` and `Deployer.ts` both import from each other (via `factory.ts`), the build fails with "No matching export" errors. Fix: extract factory to separate file, import from there.

### Duplicate JS Files in Next.js Pages
When TypeScript compilation outputs `.js` files alongside `.tsx` source (e.g., `pages/index.js` + `pages/index.tsx`), Next.js warns about duplicate routes. Fix: remove `.js` and `.d.ts` files from `src/` after build.
