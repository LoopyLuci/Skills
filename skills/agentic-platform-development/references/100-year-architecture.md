# 100-Year Architecture for Agentic Web Platforms

## The Core Insight

The greatest web building platform is not the one with the most features. It is the one with the **right foundations** that allow it to evolve for 100 years without becoming obsolete.

**The problem with feature-heavy platforms:**
- They accumulate technical debt
- They become bloated and slow
- They depend on external services that disappear
- They cannot adapt to new paradigms
- They die when the company behind them dies

**The 100-year platform:**
- Has a tiny, perfect core
- Everything else is a plugin
- Uses open, human-readable formats
- Can run offline forever
- Can be maintained by anyone
- Can evolve without breaking

## The 7 Principles

### Principle 1: Zero Dependencies in the Core

The core of the platform should depend on **nothing** but the language standard library.

**Why:**
- External libraries disappear, break, change licenses
- Standard library is guaranteed to exist for decades
- Fewer dependencies = fewer failure points
- The core should be able to run on any interpreter

**Rule:** Core modules import nothing from package managers. Nothing.

### Principle 2: Everything is a Plugin

Every feature beyond the core should be a plugin that can be added, removed, or replaced.

**Why:**
- Features come and go
- Users have different needs
- Plugins can be community-maintained
- The core stays small and stable

**Plugin categories:**
- Storage plugins: filesystem, SQLite, Git, S3, IPFS
- AI plugins: OpenAI, Anthropic, Ollama, custom
- Export plugins: HTML, React, Vue, Svelte, Angular
- Theme plugins: Bootstrap, Tailwind, Bulma, custom
- Form plugins: Contact, Survey, Payment, custom
- Media plugins: Image, Video, Audio, SVG
- E-commerce plugins: Stripe, PayPal, Crypto
- Publishing plugins: Vercel, Netlify, Cloudflare, FTP
- Collaboration plugins: Git, CRDT, WebSocket
- Analytics plugins: Google, Plausible, Matomo

### Principle 3: Open, Human-Readable Native Formats

The native storage format should be open, human-readable, and editable without the platform.

**Why:**
- Users should never be locked in
- Files should be editable with any text editor
- Formats should be documented and stable
- Future tools should be able to read them

**Native formats:**
- Project: `.webbuilder/project.json` (JSON)
- Page: `.webbuilder/pages/{id}.json` (JSON)
- Section: `.webbuilder/sections/{id}.json` (JSON)
- Asset: `.webbuilder/assets/{id}.{ext}` (binary)
- Theme: `.webbuilder/themes/{id}.json` (JSON)
- Plugin: `.webbuilder/plugins/{id}/plugin.json` (JSON)

**All JSON. All human-readable. All editable.**

### Principle 4: Self-Describing System

Every piece of data should describe itself — its type, version, schema, and meaning.

**Why:**
- Future versions can migrate old data
- External tools can understand the data
- No separate schema files that can get lost
- Data is self-documenting

**Example:**
```json
{
  "_schema": "webbuilder/project",
  "_version": "1.0.0",
  "_created": "2026-09-01T00:00:00Z",
  "id": "project-abc123",
  "name": "My Website",
  "pages": [
    {
      "_schema": "webbuilder/page",
      "_version": "1.0.0",
      "id": "page-def456",
      "name": "Home",
      "sections": [
        {
          "_schema": "webbuilder/section",
          "_version": "1.0.0",
          "id": "section-ghi789",
          "type": "Hero",
          "props": {
            "title": "Welcome",
            "subtitle": "Build something amazing"
          }
        }
      ]
    }
  ]
}
```

### Principle 5: Composability Over Monoliths

Small, focused tools that compose together rather than one giant tool.

**Why:**
- Each tool can be understood, tested, and replaced
- Tools can be combined in unexpected ways
- No single point of failure
- Easier to maintain

**The Unix philosophy applied to web building:**
- `webbuilder-create` — create projects
- `webbuilder-add` — add sections
- `webbuilder-export` — export to various formats
- `webbuilder-deploy` — deploy to various platforms
- `webbuilder-serve` — preview locally
- `webbuilder-import` — import from other tools
- `webbuilder-convert` — convert between formats

Each tool does one thing well. They compose via pipes and files.

### Principle 6: Deterministic Behavior

Given the same input, the platform should always produce the same output.

**Why:**
- Reproducible builds
- Testable behavior
- No surprises
- Version control friendly

**Rules:**
- No random IDs (use content hashes)
- No timestamps in output (unless explicitly requested)
- No network calls during build (unless explicitly requested)
- No floating-point calculations that vary by platform
- Sorted keys in all JSON output

### Principle 7: Community Governance

The platform should be governable by its community, not controlled by a single entity.

**Why:**
- Single entities fail, communities endure
- Users should have a say in the platform's direction
- No vendor lock-in
- No single point of failure

**Governance model:**
- Core: maintained by community, stable API
- Plugins: maintained by anyone, any license
- Formats: documented, versioned, backward-compatible
- Decisions: RFC process, community voting
- Funding: donations, grants, optional paid plugins

## Architecture Layers

### Layer 0: Core (Zero Dependencies)
```
core/
├── __init__.py      # Package init
├── project.py       # Project model (dataclass)
├── page.py          # Page model (dataclass)
├── section.py       # Section model (dataclass)
├── design.py        # Design model (dataclass)
├── storage.py       # Storage interface (abstract)
├── exporter.py      # Export interface (abstract)
├── validator.py     # Validation logic
├── serializer.py    # JSON serialization
└── migrator.py      # Schema migration
```

**Responsibilities:**
- Define data models
- Validate data
- Serialize/deserialize
- Migrate between schema versions

**No external dependencies. No GUI. No network. No AI.**

### Layer 1: Storage Plugins
```
storage/
├── json_files.py    # JSON files on disk (default)
├── sqlite.py        # SQLite database
├── git.py           # Git repository
├── s3.py            # AWS S3
├── ipfs.py          # IPFS distributed storage
└── memory.py        # In-memory (for testing)
```

### Layer 2: Export Plugins
```
export/
├── html.py          # Static HTML (default)
├── react.py         # React components
├── vue.py           # Vue components
├── svelte.py        # Svelte components
├── angular.py       # Angular components
├── json.py          # JSON data
├── markdown.py      # Markdown
├── pdf.py           # PDF output
└── zip.py           # ZIP archive
```

### Layer 3: AI Plugins
```
ai/
├── openai.py        # OpenAI integration
├── anthropic.py     # Anthropic integration
├── ollama.py        # Ollama local models
├── custom.py        # Custom provider
└── none.py          # No AI (default)
```

### Layer 4: GUI (Replaceable)
```
gui/
├── __init__.py      # GUI entry point
├── window.py        # Main window
├── canvas.py        # Visual canvas
├── code_editor.py   # Code editor
├── preview.py       # Preview panel
├── properties.py    # Property inspector
└── ...
```

**Can be replaced with:**
- Web interface (React, Vue, etc.)
- Terminal interface (TUI)
- Headless interface (API only)
- VR interface (future)

### Layer 5: Server (Optional)
```
server/
├── __init__.py      # Server entry point
├── api.py           # REST API
├── websocket.py     # WebSocket
└── cli.py           # CLI interface
```

**Optional. Only needed for:**
- Remote access
- API access
- Collaboration
- CI/CD integration

## Simplification Workflow

When the codebase grows too large:

1. **Identify core vs contrib**: Core = what's needed for Create → Edit → Export. Everything else = contrib.
2. **Move to contrib/**: Relocate non-core modules to a `contrib/` directory.
3. **Update imports**: Change `from webbuilder.module` to `from webbuilder.contrib.module`.
4. **Verify core still works**: Run integration tests after each move.
5. **Contrib modules remain accessible**: They're just not loaded by default.

## Verification Workflow

After every major change:

1. **Test core workflow end-to-end**: Create → Save → Load → Export → Verify output.
2. **Run integration tests**: Full workflow tests that verify the whole system works together.
3. **Verify GUI launches**: Check all tabs render, no import errors.
4. **Check for import errors**: Import all modules to catch missing dependencies.

## What This Enables

| Timeframe | What Happens |
|-----------|--------------|
| 10 years | Platform runs on new language versions. New AI providers are plugins. New export formats are plugins. The core is still the same. |
| 50 years | Language is still running. Core is still running. Plugins have been replaced many times. The formats are still readable. |
| 100 years | Platform can be reimplemented from the spec. The formats are still documented. The data is still readable. The community still maintains it. |

## The Promise

**The platform will outlive its creator.**

Not because it has the most features.
Not because it has the best GUI.
Not because it has the most users.

But because it has the right foundations:
- Zero dependencies in the core
- Everything is a plugin
- Open, human-readable formats
- Self-describing data
- Composable tools
- Deterministic behavior
- Community governance

**This is how you build a platform for 100 years.**
