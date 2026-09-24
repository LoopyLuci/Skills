# 100-Year Architecture & Simplification Workflow

This reference covers the architecture principles and simplification workflow that emerged from refactoring a large PyQt5 codebase for long-term durability.

## The Core Insight

The greatest software platforms are not feature-rich — they are **foundationally correct**. Platforms that last (Unix, SQL, HTTP, HTML) have small, perfect cores with everything else as plugins.

## 7 Principles for 100-Year Software

1. **Zero Dependencies in Core** — Core depends only on language stdlib
2. **Everything is a Plugin** — Features beyond core are addable/removable
3. **Open, Human-Readable Formats** — Native storage is editable without the app
4. **Self-Describing System** — Every object has `_schema` and `_version`
5. **Composability Over Monoliths** — Small, focused tools that compose
6. **Deterministic Behavior** — Same input → same output, always
7. **Community Governance** — Community controls direction, not single entity

## Simplification Workflow

When a codebase grows too large, follow this pattern:

### Step 1: Test Core Workflow
Verify the fundamental path works: Create → Edit → Export → Verify.

```python
def test_full_workflow():
    pm = ProjectManager()
    p = pm.create_new("Test")
    p.pages[0].sections.append(Section(id="s1", type="Hero", props={"title": "Hi"}))
    pm.save(p)
    loaded = pm.load(p.id)
    assert loaded.pages[0].sections[0].props["title"] == "Hi"
    html = HTMLExporter().generate(loaded)
    assert "<!DOCTYPE html>" in html
```

### Step 2: Identify Core vs Contrib

**Keep in core:**
- Data models (Project, Page, Section, Design)
- Storage backend (JSON files)
- Export (HTML at minimum)
- GUI framework
- Config

**Move to contrib/:**
- CMS, E-Commerce, Publishing
- Plugin system, Collaboration
- Analytics, Search, Feedback
- Performance monitoring, Migrations
- Agentic building infrastructure

### Step 3: Update All Import Paths

Use `search_files` to find all `from webbuilder.X` references:

```python
# Before
from webbuilder.feedback import FeedbackCollector

# After
from webbuilder.contrib.feedback import FeedbackCollector
```

### Step 4: Fix Missing Methods

After reorganization, `AttributeError` often means a method was in a moved module. Either:
- Re-add the method to the core class
- Update the call site to use the contrib version

### Step 5: Add Self-Describing Schema

```python
@dataclass
class Project:
    id: str
    name: str
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "_schema": "webbuilder/project",
            "_version": "1.0.0",
            "id": self.id,
            "name": self.name,
        }
```

### Step 6: Verify GUI Launches

```bash
python webbuilder_desktop.py
```

Fix import errors one by one until the GUI launches cleanly.

## Module Reorganization Pattern

```
# Move module to contrib
import shutil
shutil.copytree("webbuilder/feedback", "webbuilder/contrib/feedback")
shutil.rmtree("webbuilder/feedback")

# Update all imports
# Search: from webbuilder.feedback
# Replace: from webbuilder.contrib.feedback
```

## Config with Complex Objects

When Config needs complex objects (like Provider with Model list), use `__post_init__`:

```python
@dataclass
class AppConfig:
    providers: dict = field(default_factory=dict)
    
    def __post_init__(self):
        """Initialize providers after creation."""
        from webbuilder.core import Provider, Model
        self.providers = {
            "openai": Provider(id="openai", name="OpenAI", models=[
                Model(id="gpt-4o", name="GPT-4o", is_free=False),
            ]),
        }
```

## Key Metrics

| Metric | Before | After |
|--------|--------|-------|
| Core dependencies | Several | 0 |
| Core LOC | ~1500 | ~500 |
| Modules in core | 30+ | 15 |
| Test pass rate | Unknown | 9/9 (100%) |
| GUI launches | Yes | Yes |

## Pitfall: Import Path Updates

When moving modules, you MUST update ALL import paths. Missing one causes `ModuleNotFoundError` at runtime. Use `search_files` with pattern `^from webbuilder\.` to find all imports.

## Pitfall: Missing Methods After Move

After moving a module, callers may fail with `AttributeError`. Example:
- `Config` had `get_models_for_dropdown()` method
- After reorganization, the method was missing
- Fix: Re-add the method or update call site

## Pitfall: Circular Imports with New Classes

When adding new classes to `core/__init__.py` (like `Model`, `Provider`), ensure they're defined BEFORE classes that reference them. Use `__post_init__` for complex initialization.