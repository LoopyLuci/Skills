# Package Migration Patterns

## When to Use
When moving or merging Python packages (e.g., consolidating `src/vm_mcp/` into `src/vm_harness/`).

## Gradual Migration Workflow

1. **Survey consumers** — `grep -rn "from vm_mcp\|import vm_mcp" . --include="*.py" | grep -v __pycache__`
2. **Classify** — Group consumers by module type (GUI, tests, scripts, src)
3. **Move one module at a time** — `mv src/vm_mcp/config.py src/vm_harness/config.py`
4. **Update imports** — Use `grep` to find all consumers, then `patch` each import
5. **Run tests** — `.venv/Scripts/python.exe -m unittest tests.test_integrations`
6. **Repeat** for next module
7. **Delete old package** only when zero consumers remain

## Verifying Zero Consumers
```bash
# Final check before deleting old package
grep -rn "from vm_mcp\|import vm_mcp" . --include="*.py" | grep -v __pycache__ | grep -v dist/
```
If this returns 0 results, the old package can be safely deleted.

## PyInstaller Hidden Import Updates
After migration, update the PyInstaller command:
- Old: `--hidden-import vm_mcp --hidden-import vm_mcp.config`
- New: `--hidden-import vm_harness --hidden-import vm_harness.config`

## Common Failure Mode
Deleting a package with active consumers breaks imports **silently** in PyInstaller-frozen exes. The exe exits with code 1 and NO error message. Always grep for consumers before deleting.
