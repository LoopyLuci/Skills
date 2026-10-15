# AgenticBotPlatform extension development

ABP extensions are the zero-core-edit integration seam: an extension folder with an
`api.add_*` hook registry, loaded at runtime via `ABP_PRIVATE_DIR`. Everything an
integration needs can be registered without touching ABP's core.

## Extension folder layout

```
integrations/abp/extensions/<name>/
├── <name>_extension.toml          # metadata: name, version, label
├── <name>/
│   ├── __init__.py                # the package; register(api) is the entry point
│   ├── routes.py                  # optional: dashboard API routes
│   ├── panel.js                   # optional: dashboard panel script
│   ├── config/
│   │   └── backends.yaml         # optional: config overlay (deep-merged)
│   └── tests/
│       └── test_<name>.py         # unit tests (registered via add_test_dir)
└── config/
    └── backends.yaml             # alternative: overlay at the integration root
```

## The `add_*` hook registry

All hooks are called on the `api` object inside `register(api)`:

| Hook | Signature | What it registers |
|---|---|---|
| `add_backend_class` | `(kind, factory, *, family, label, ready)` | A new backend kind. `factory(settings, model) -> Backend`. `ready() -> (bool, str)` is the pre-flight check. |
| `add_routes` | `(register)` | Dashboard API routes. `register(app, read_auth, write_auth)` is called like an ABP route module. |
| `add_panel` | `(panel_id, title, *, description, script, icon)` | A UI panel. `script` is served from `/extensions/<name>/<script>`. |
| `add_memory_source` | `(kind, *, required, read, item_kind, complete, label)` | A memory-fabric source kind. `read(source) -> Iterator[(item_id, title, text, ts, tags)]`. |
| `add_task` | `(coro_fn)` | A background async task. Runs until the extension is unloaded. |
| `add_integration_scope` | `(name, rules)` | An API-key scope: `[(method, path_regex), ...]`. |
| `add_integration_preset` | `(name, *, label, scopes, note)` | A named set of scopes offered when minting a key. |
| `add_lab_importer` | `(kind, *, label, run, list_items)` | A Neural Lab importer. `run(body) -> spec`. |
| `add_mcp_tool` | `(func, name)` | An MCP tool on the extension's server. |
| `add_cli_command` | `(name, run, *, help)` | A CLI command. |
| `add_module` | `(entry)` | A module entry (hot-reloadable). |

## Config overlay

`<ABP_PRIVATE_DIR>/config/<name>.yaml` deep-merges over ABP's tracked
`config/<name>.yaml`. This is how an extension ships per-instance settings
(personas, addresses, intervals) without editing ABP's config files.

## Route auth: the Depends wrapping rule

Extensions receive `read_auth` and `write_auth` as **plain callables** (not
`Depends` objects). FastAPI's `dependencies=` parameter requires a list of
`Depends` objects. The correct pattern:

```python
# WRONG — FastAPI raises "'function' object is not iterable"
@app.post("/api/thing", dependencies=write_auth)

# CORRECT
@app.post("/api/thing", dependencies=[Depends(write_auth)])
```

## Backend settings

A backend's `settings` dict comes from `config['backends'][name]` in ABP's
merged config. The router caches backend instances by name + model override +
hermes_home — a config reload alone does NOT rebuild them. Restart ABP after
changing backend settings.

## The scoped-key pattern (H1)

For any integration that needs API access, register a scope + preset so the
integration can hold a scoped key rather than the god-mode dashboard token:

```python
api.add_integration_scope("myintegration", [
    ("POST", r"/api/thing/ask"),
    ("POST", r"/api/thing/other"),
])
api.add_integration_preset(
    "myintegration",
    label="My Integration",
    scopes=["myintegration"],
    note="Exactly what it needs, nothing else",
)
```

Mint a key with `POST /api/integrations/keys` using the preset. The key is
restricted to the scoped routes; a leaked key cannot reconfigure the fleet.

## Testing

Register tests via `api.add_test_dir("tests")` — ABP's pipeline picks them up.
Each test file can also be self-contained (pytest-style functions + a
standalone `__main__` runner with a minimal monkeypatch shim) for environments
without pytest:

```python
# Dual-mode: works under pytest AND standalone
class _MonkeyPatch:
    def __init__(self): self._undo = []
    def setattr(self, target, name, value):
        self._undo.append((target, name, getattr(target, name, None)))
        setattr(target, name, value)
    def undo(self):
        for t, n, v in reversed(self._undo): setattr(t, n, v)
        self._undo = []

if __name__ == "__main__":
    import inspect, sys
    for name, fn in sorted(vars().items()):
        if not (name.startswith("test_") and callable(fn)): continue
        mp = _MonkeyPatch()
        kw = {"monkeypatch": mp} if "monkeypatch" in inspect.signature(fn).parameters else {}
        try: fn(**kw)
        except Exception as e: print(f"FAIL {name}: {e}")
        finally: mp.undo()
```
