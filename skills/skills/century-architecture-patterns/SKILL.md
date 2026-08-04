---
name: century-architecture-patterns
description: "Use when building systems designed to last 100+ years."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [architecture, longevity, schema-versioning, self-healing, plugin-systems, atomic-writes, forward-compat]
    related_skills: [system-design-patterns, software-design-patterns, hexagonal-architecture, domain-driven-design-tactical]
---

# Century Architecture Patterns

Building systems designed to operate without code changes for 100+ years.
Not a metaphor — concrete architectural patterns that survive technology
churn, schema evolution, platform migration, and developer turnover.

## When to Use

- Designing systems that must outlive their original framework
- Building tool platforms intended for external contribution
- Creating stateful systems where data longevity matters
- Architecting agent tool systems meant for multi-framework consumption
- Any system where the cost of migration exceeds the cost of foresight

## Core Principles

### 1. Zero Hardcoded Values

Every configurable value loads from external config files — never embedded in code.
New plugins, ecosystems, or patterns = new config file, not new code.

```python
# ❌ Brittle: hardcoded patterns
ECOSYSTEMS = {"kubernetes": {"patterns": ["pod", "deployment"]}}

# ✅ 100-year: loaded from config/ JSON files
config_dir = os.path.join(APP_DIR, 'config')
for fname in os.listdir(config_dir):
    if fname.endswith('.json'):
        ecosystems[fname.replace('.json','')] = json.load(open(os.path.join(config_dir, fname)))
```

**Why:** In year 47 when quantum kubernetes replaces container kubernetes, adding a new config file requires zero code changes.

### 2. Schema Versioning

Every state file carries a `schema_version` field. On load, auto-migrate from any older version. Unknown fields preserved — never dropped.

```python
STATE_SCHEMA = {"schema_version": "2.0.0", "created_at": None}

def load_state(path):
    try:
        data = json.load(open(path))
        v = data.get("schema_version", "1.0.0")
        if v != CURRENT_VERSION:
            data = migrate(data, v, CURRENT_VERSION)
        # Forward compat: preserve unknown keys
        for k, default in STATE_SCHEMA.items():
            data.setdefault(k, default)
        return data
    except (json.JSONDecodeError, FileNotFoundError):
        return repair_from_backup(path)

def migrate(data, from_v, to_v):
    chain = {
        "1.0.0": lambda d: {**d, "schema_version": "2.0.0", "errors_recovered": 0},
        "2.0.0": lambda d: {**d, "schema_version": "3.0.0", "tools_used": {}},
    }
    cursor = from_v
    while cursor in chain:
        data = chain[cursor](data)
        cursor = data.get("schema_version", cursor)
    return data
```

**Why:** In year 23 when someone upgrades the schema format, all existing state files automatically migrate. Old data is never lost — every migration is a function in the chain.

### 3. Self-Healing State

Detect corruption, repair from backup, or recreate from defaults automatically.
Never crash with a corrupt state file — always heal.

```python
def load_or_repair(path):
    if not os.path.exists(path):
        return create_fresh_state()
    try:
        return json.load(open(path))
    except (json.JSONDecodeError, KeyError):
        backup = path + ".bak"
        if os.path.exists(backup):
            try: return json.load(open(backup))
            except: pass
        return create_fresh_state()
```

**Why:** In year 14 when a cosmic ray flips a bit in the state file, the system doesn't die — it heals and logs the event.

### 4. Atomic Writes

Write to `.tmp`, then `os.replace()` — never half-written state, even on power failure.

```python
def save_state(path, data):
    tmp = path + ".tmp"
    with open(tmp, 'w') as f:
        json.dump(data, f)
    if os.path.exists(path):
        shutil.copy2(path, path + ".bak")  # Keep previous backup
    os.replace(tmp, path)  # Atomic on same filesystem
```

**Why:** In year 62 when the datacenter loses power mid-write, the state file is either the complete previous version or the complete new version — never a corrupted partial write.

### 5. Plugin-Based Architecture

New capabilities come as plugins (config files, scripts, modules) — not code changes to the core.

```
plugin-based-ecosystem/
├── core/              # Never changes
├── plugins/
│   ├── ecosystem-a/   # Added in year 3
│   ├── ecosystem-b/   # Added in year 15
│   └── quantum-x/     # Added in year 47 — no core changes
└── config/
    ├── ecosystems/
    │   ├── default.json    # Shipped with v1.0
    │   └── custom.json     # User added in year 22
```

### 6. Forward Compatibility

Never drop unknown fields. Preserve everything you don't understand.
A system from year 1 must still work with data written by year 50's version.

```python
class ForwardCompatibleConfig:
    def __init__(self, data):
        self.known = self._extract_known(data)
        self.unknown = {k: v for k, v in data.items() 
                       if k not in self.known}
    
    def serialize(self):
        return {**self.known, **self.unknown}
```

### 7. Graceful Degradation

Each subsystem fails independently. If one component is corrupt, others still work.

```python
class SkillGenesisModel:
    def discover(self, ecosystems):
        try:
            return self.gap_detector.find_gaps(ecosystems)
        except Exception as e:
            self.memory.record_error("discover", str(e))
            return []  # Return empty, don't crash
```

## Reference Implementation

See `references/genesis-model-architecture.md` for the complete reference
implementation — the Skill Genesis Model v3.0 built entirely on these principles.

## Common Pitfalls

1. **Over-engineering** — not every system needs 100-year architecture. Apply where data longevity matters (state files, user data, configuration registries). Don't use for ephemeral computation.

2. **Migration chain breaks** — if a migration function has a bug, all subsequent migrations fail. Test every migration path. Keep old migration functions even after they're superseded.

3. **No rollback plan** — migration should have a rollback path. Keep the `.bak` file from before migration. Test rollback as rigorously as migration.

4. **Silent data loss** — preserving unknown fields means bugs in unknown fields persist. Log the presence of unknown fields during migration so operators know they exist.

5. **Backup pollution** — every atomic write creates a `.bak` file. Implement retention policy (keep last 3-5 backups, oldest weekly backup).

## Verification Checklist

- [ ] Every configurable value loads from external files, not code
- [ ] State files carry schema_version with auto-migration chain
- [ ] Corrupt state self-heals from backup or defaults
- [ ] All state writes use atomic .tmp + replace pattern
- [ ] New capabilities require config changes, not code changes
- [ ] Unknown fields preserved during load/save cycles
- [ ] Subsystems fail independently (try/except each component)
- [ ] Migration chain tested for every version jump
- [ ] Backup retention policy implemented
- [ ] Graceful degradation: partial results > no results

## See Also

- `system-design-patterns` — general distributed system patterns
- `software-design-patterns` — classic GoF patterns
- `hexagonal-architecture` — port/adapter separation
- `domain-driven-design-tactical` — bounded contexts and aggregates
