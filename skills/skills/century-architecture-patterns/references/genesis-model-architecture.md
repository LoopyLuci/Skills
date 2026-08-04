# Reference Implementation: Skill Genesis Model v3.0

The Skill Genesis Model at `mlops/skill-genesis-model/scripts/skill_genesis.py` is a
complete reference implementation of all 7 century-architecture principles.

## How Each Principle Is Realized

| Principle | Implementation |
|-----------|---------------|
| Zero hardcoded values | Ecosystems loaded from `config/ecosystems/*.json` |
| Schema versioning | `model_state.json` carries `schema_version`, auto-migrates via chain |
| Self-healing | `GenesisMemory._load_or_repair()` recovers from `.bak` or creates fresh |
| Atomic writes | `save()` writes `.tmp`, copies `.bak`, then `os.replace()` |
| Plugin-based | New ecosystem = new JSON in `config/ecosystems/`, no code changes |
| Forward compat | `setdefault()` preserves unknown keys during load |
| Graceful degradation | Each tool wrapped in try/except, errors logged not fatal |

## Architecture Diagram

```
skill-genesis-model/
├── SKILL.md                        # Loadable Hermes skill definition
├── config/ecosystems/
│   └── template.json               # Plugin ecosystem config (add new via JSON)
├── scripts/
│   └── skill_genesis.py            # The model — 7 tools, 1,032 skill awareness
├── state/
│   ├── model_state.json            # Schema-versioned, self-healing state
│   └── model_state.json.bak       # Auto-backup for recovery
└── references/
    └── strategic-blueprint.md      # 163 future improvements (43KB)
```

## Integration Layer (genesis-integration-layer/)

```
genesis-integration-layer/
├── SKILL.md
└── scripts/
    ├── mcp_server.py               # MCP — any MCP client
    ├── api_server.py               # REST + OpenAI function calling
    └── plugin_genesis.py           # Hermes Agent native plugin
```

## Key Design Decisions

1. **Single-file model** — all 7 tools in one script. Portable, deployable, auditable.
2. **Config-driven ecosystems** — patterns live in JSON, not Python. Add "quantum" by creating a config file.
3. **Self-contained MCP server** — the MCP server is its own file (mcp_server.py) that imports the model. No framework dependency beyond the `mcp` package.
4. **Two-way sync with state** — state auto-saves after every mutation. Backup before every write.
5. **Hermes-native plugin** — `plugin_genesis.py` registers tools via `GenesisPlugin` class. Loads model lazily on first tool call.

## Lessons Learned

- Schema migration chains must be tested backward (v3 → v2 → v1) to verify rollback works
- Atomic writes on Windows: `os.replace()` works across filesystems but not across drives. Keep state on same drive as app.
- Backup retention: unlimited `.bak` files consume disk. Implement retention (keep 3 most recent, oldest weekly).
- Plugin discovery: scanning `config/*.json` at startup is fast (<1ms for 50 files). Avoid `importlib` for plugins when config files suffice.
