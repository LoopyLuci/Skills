# Parallel Codebase Buildout

When the user asks for comprehensive or multi-component implementation ("proceed with all", "build everything optimally"), use `delegate_task` to spawn N parallel subagents for independent code streams.

## When to use

- Building 3+ independent packages/modules simultaneously
- User demands exhaustive scope in a single session
- Components have clear boundaries (e.g., networking, hypervisors, containers, API, mobile)
- Each stream can be implemented without reading another stream's output

## Workflow

1. **Plan**: Identify independent streams and their file paths before spawning
2. **Spawn**: One subagent per stream with:
   - Clear goal listing exact file paths to create
   - Self-contained context (don't rely on other streams' output)
   - `output_schema` requiring `files_created` and `total_lines`
   - Import verification built into the subagent's verification step
3. **Wait**: All subagents run in parallel; collect results when they return
4. **Verify**: Run import checks on ALL packages after all subagents complete
5. **Fix cross-cutting concerns**:
   - Missing type aliases between base ABC and implementations
   - Empty `__init__.py` files that should export symbols
   - Missing dependencies subagents couldn't install
6. **Integrate**: Wire everything together in main entry points

## Subagent template

```
goal: "Build the X package. Create C:/path/to/x/ with: a.py (A class), b.py (~N lines). ~M lines total."
context: "Project at C:/path. Python 3.11, pydantic, asyncio. Existing code at Y."
output_schema: {"properties": {"files_created": {"items": {"type": "string"}, "type": "array"}, "total_lines": {"type": "integer"}}, "required": ["files_created", "total_lines"], "type": "object"}
```

## Pitfalls

### Subagent write failures despite reported success
A subagent may report files created but `write_file` actually refused because the file existed without that task having read it first (the read-before-write guard). Files end up missing or empty.

**Fix:** After parallel generation, scan for empty `__init__.py` files and missing files with `search_files`. Use `read_file` + `patch` to fix any that didn't land.

### Missing type aliases across backends
When N backend implementations import a type from a base ABC module, ensure the base exports it with the EXACT name. If base defines `DisplayType(str, Enum)` but backends import `VMDisplayType`, add an alias: `VMDisplayType = DisplayType`.

**Mechanism:** Subagents independently decide import names. If all choose `VMDisplayType` but the base defines `DisplayType`, import fails for every backend.

**Fix:** After parallel generation, run import checks on all packages. Any `ImportError: cannot import name 'X'` means the base module needs to export X or add an alias.

### Cross-subagent shared types
Subagents can't see each other's output. If stream A defines a type that stream B needs, the name must be standardized upfront or fixed after.

**Fix:** Define shared interface names in the spawn context, or verify and add aliases in the fix step.

### Post-buildout mass rename pitfall
After parallel generation, you may need to rename a product string across all files (e.g., `QEMU-MCP` → `VM-Harness`). Using `sed` with the same quote delimiter as the string content breaks string escaping:

```bash
# BROKEN: the closing " in the replacement is consumed as the sed command terminator
sed -i 's/"QEMU-MCP"/"VM-Harness/g' file.kt
# Result: text = "VM-Harness,   ← unclosed string, compile error
```

The `s/pattern/replacement/g` parser sees the replacement as `"VM-Harness` (the `"` before `g` is interpreted as escaping the `g`, or the quote is consumed as the delimiter close), leaving the Kotlin string unclosed.

**Fix:** Use a delimiter that does NOT appear in the pattern or replacement:
```bash
sed -s 's|"QEMU-MCP"|"VM-HARNESS"|g' file.kt   # pipe delimiter — safe
```
Or use `grep -rl | xargs sed` with single-token replacements (no quotes in pattern). **Best:** reserve `sed` for comments/docstrings/logs; use `patch` on known-good unique strings for code literals, and always run the build after bulk renames to catch broken string escaping.

### Android app rebranding: preserve internal identifiers
When renaming an Android app, the package ID (`applicationId`), deep link scheme, and `EncryptedSharedPreferences` name MUST stay the same — changing them breaks the installed app's ability to receive updates, clears paired state, and breaks Hilt DI. Only rename:
- `app_name` string resource → display name
- Theme name (if user-visible)
- Launcher icon (adaptive icon XML + mipmap PNGs)
- User-facing UI strings (dashboard title, subtitle, error messages)
- Log tags

Keep unchanged: `namespace`, `applicationId`, deep link scheme (`qmcmcp://`), shared prefs filenames, package directory paths, Hilt module names, API client class names.

## Verification checklist

After all subagents complete:
- [ ] All expected files exist (search for `*.py` in each package)
- [ ] No empty `__init__.py` files
- [ ] All packages import without error (`python -c 'import pkg'`)
- [ ] Line counts match subagent reports
- [ ] Cross-package imports resolve (base ABC exports all names backends use)
