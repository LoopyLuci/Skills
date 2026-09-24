# WebBuilder Module Ecosystem — September 2026

Complete reference for all 141 modules built during the September 2026 sessions, covering visual editing, AI/ML, business operations, and distribution.

## Scale

| Metric | Value |
|--------|-------|
| Total Python modules | 155+ |
| Lines of code | 25,000+ |
| Unit tests | 203 (all passing) |
| Build size | 120MB |
| Git commits | 100+ |

## GUI Integration Status

All backend modules are wired into the GUI through:

| Panel | Access | Modules |
|-------|--------|---------|
| Unified Modules Panel | Tools → All Modules | Forms, A/B, Assets, History, Responsive, CSS, AI Code |
| Command Palette | Ctrl+Shift+P | All registered commands |
| Settings Window | Ctrl+, | Appearance, AI, Editor, Export, Plugins, About |
| Form Builder Dialog | Tools → Form Builder | Visual drag-and-drop form designer |
| SEO Dashboard | Tools → SEO Dashboard | Meta tags, sitemap, robots.txt |
| Analytics Dashboard | Tools → Analytics Dashboard | Page views, conversions, funnels |
| Hardware Info | View → Hardware Info | CPU/GPU/memory detection |
| Theme System | View → Theme | 6 themes with semantic design tokens |
| ML Training Dashboard | 🤖 ML Training tab | 7 NumPy models, train/evaluate/predict |
| Terminal CLI | Terminal tab | Shell commands + WebBuilder commands |
| Activity Log | Activity tab | Filter, search, copy, save, JSON export |
| Racing Game | 📚 Examples → 🎮 Games | Native Qt racing widget |

## Module Inventory

### Visual Editing & Design
| Module | Path | Purpose |
|--------|------|--------|
| CSS Editor | `webbuilder/css/editor.py` | Box model visualizer, Flexbox/Grid configs, CSS variables, animations |
| Responsive Studio | `webbuilder/responsive/studio.py` | 11 device presets, breakpoints, network throttling, touch simulation |
| Form Builder | `webbuilder/forms/builder.py` | 26 field types, conditional logic, validation, submissions analytics |
| Command Palette | `webbuilder/command/palette.py` | Ctrl+Shift+P, fuzzy search, recent commands |
| Design Tokens | `webbuilder/design/tokens.py` | Semantic color/spacing/typography/shadow/radius tokens, QSS generation |

### AI & Machine Learning
| Module | Path | Purpose |
|--------|------|--------|
| AI Providers | `webbuilder/ai/__init__.py` | 9 providers, live model discovery (807 lines) |
| GPU Accelerator | `webbuilder/ai/gpu_accelerator.py` | CUDA/ROCm/Metal inference, ONNX, TensorRT, quantization |
| Cache | `webbuilder/ai/cache.py` | LRU memory + SQLite disk cache, cost tracking |
| Parallel Inference | `webbuilder/ai/parallel_inference.py` | Multi-provider concurrent, speculative decoding |
| AI Features | `webbuilder/ai/features.py` | Content writer, code reviewer, SEO analyzer, accessibility auditor |
| Code Generator | `webbuilder/ai/codegen.py` | Template library, natural language to code, context-aware suggestions |

### Business & Marketing
| Module | Path | Purpose |
|--------|------|--------|
| E-Commerce | `webbuilder/ecommerce/engine.py` | Catalog, cart, orders, tax, shipping, discounts |
| SEO Marketing | `webbuilder/seo/marketing.py` | Meta tags, sitemap, robots.txt, Schema.org, Lighthouse |
| A/B Testing | `webbuilder/testing/ab.py` | Split tests, Z-test significance, winner auto-selection |
| Analytics | `webbuilder/analytics/dashboard.py` | Page views, conversions, funnels, dashboards |

### Security
| Module | Path | Purpose |
|--------|------|--------|
| Post-Quantum Crypto | `webbuilder/security/post_quantum.py` | Kyber KEM, Dilithium signatures, hybrid crypto, CryptoEngine |
| Trait System | `webbuilder/abi.py` | Trait registry, factory, composition, validator |
| Trait Integration | `webbuilder/integrations/traits.py` | Register AI/ML/crypto/UI as traits |
| Compliance | `webbuilder/security/compliance.py` | CSP, headers, CSRF, XSS protection |

### AI/ML Self-Learning
| Module | Path | Purpose |
|--------|------|--------|
| Self-Learning Pipeline | `webbuilder/ml_engine/self_learning.py` | Online learning, interaction recording, retrain scheduling |
| ML Models | `webbuilder/ml_engine/models.py` | 7 NumPy models (MLP, LogisticRegression, KMeans, etc.) |
| Training Dashboard | `webbuilder/gui/training_dashboard.py` | Train/evaluate/predict with NumPy models |

### Infrastructure
| Module | Path | Purpose |
|--------|------|--------|
| Hardware HAL | `webbuilder/hardware/` | Multi-threading + multi-GPU with work-stealing |
| MCP Server | `webbuilder/mcp/server.py` | Model Context Protocol (14 tools) |
| Asset Manager | `webbuilder/assets/manager.py` | AI auto-tagging, compression, CDN integration |
| Asset Pipeline | `webbuilder/assets/pipeline.py` | WebP/AVIF, thumbnails, lazy loading |
| Update System | `webbuilder/update.py` | Auto-update checker/downloader |
| Installer | `webbuilder/installer.py` | ZIP distribution, Inno Setup, WiX config |

### Data & Content
| Module | Path | Purpose |
|--------|------|--------|
| Content Management | `webbuilder/content/management.py` | Rich text, media library, versioning, newsletters |
| SQLite Backend | `webbuilder/core/sqlite_backend.py` | ACID + zlib compression + full-text search |
| Version History | `webbuilder/history/version.py` | Branching, visual diff, rollback, change attribution |
| Components Library | `webbuilder/components/library.py` | Slider, modal, tabs, pricing table, FAQ |

### GUI Panels
| Module | Path | Purpose |
|--------|------|--------|
| Modules Panel | `webbuilder/gui/modules_panel.py` | Unified tabs for Forms, A/B, Assets, History, Responsive, CSS, AI Code |
| Settings Dialog | `webbuilder/gui/settings_dialog.py` | 6-tab settings window |
| Dashboards | `webbuilder/gui/dashboards.py` | SEO & Analytics dashboard dialogs |
| Form Builder Dialog | `webbuilder/gui/form_builder_dialog.py` | Visual drag-and-drop form designer |

## Key Pitfalls Discovered

### 1. Qt DPI Deprecation
`screen.logicalDotsInch()` was removed in Qt 5.14+. Use `screen.logicalDotsPerInch()` instead.

### 2. Duplicate Class Definitions After Extraction
When extracting a class from a monolith into its own module, remove ALL class body code from the monolith — keep only the import. Leftover class bodies cause import conflicts.

### 3. Missing Extracted Module
After removing a class from the monolith, you MUST create the new module file AND add it to `__init__.py` imports, or window launch fails with AttributeError.

### 4. PyInstaller PermissionError on Windows
Always `taskkill /F /IM WebBuilder.exe` before rebuilding — the running exe locks the file and causes `[WinError 5] Access is denied`.

### 5. Form Builder Submit Validation
`submit_form()` must call `form.validate(data)` BEFORE sanitizing, so invalid submissions return errors instead of silently succeeding.

### 6. Backward-Compatibility Aliases
When refactoring, create alias classes in `__init__.py` files pointing to the new location. Tests depend on old names.

### 7. Native ML Models
Use `numpy` (not pip install numpy — it's excluded from PyInstaller build). Models use Dense, Dropout, BatchNorm from `webbuilder.ml_engine`.

### 8. f-string Backslash in CSS
Cannot use `\n` inside f-string expressions. Build the string separately or use string concatenation.

### 9. computer_use GUI Automation
Coordinate-based clicks are unreliable for menu navigation. Prefer direct function calls or `os.startfile()` for launching.

### 10. Test Fixture Key Pattern
When testing form submissions, use `field.id` as the dictionary key, not `field.label`. Tests that use labels as keys fail silently.

### 11. Qt Window Flags for Command Palette
Use `Qt.Dialog | Qt.FramelessWindowHint` (not `Qt.Popup`) for command palette — Popup can cause focus issues on Windows.

### 12. Form Builder API Shape
Tests expect `FormBuilder.add_field(form_id, field_type, label, options=..., required=...)` — not a FormField object passed in.

### 13. Import Order for __init__.py
New modules must be added to both the package `__init__.py` AND imported in `gui/__init__.py` — missing either causes ImportError at launch.

### 14. Pass Stub Elimination Policy
ALL `pass` statements in method bodies must be replaced with proper implementations:
1. **Exception handlers**: Replace `except Exception: pass` with `except Exception as e: logger.warning(f"Context: {e}")`
2. **Method stubs**: Replace `pass` with either a proper implementation or `raise NotImplementedError`
3. **Abstract methods**: Keep `pass` ONLY in `@abstractmethod` definitions (these are intentional interfaces)
4. **Fallback class definitions**: `pass` in `except ImportError` fallback classes is acceptable

**Pitfall**: The user has a zero-tolerance policy for placeholders, stubs, and silent exception swallowing. This is a standing policy, not a one-time request.

### 15. Dilithium Sign/Verify Key Derivation
`dilithium_sign` and `dilithium_verify` must use consistent public key derivation. The private key must include the seed (format: `seed + sk`), and `dilithium_sign` must derive the public key from the seed using the same derivation as `dilithium_keygen`.

**Pitfall**: If `dilithium_sign` derives the public key differently than `dilithium_keygen`, the commitment in the signature won't match the verification computation, causing all signatures to fail verification.

### 16. CryptoEngine.generate_keypair Return Format
`CryptoEngine.generate_keypair()` returns `(pub, priv)` bytes, NOT nested tuples. For PQ algorithms, it returns the Dilithium key pair. For classical algorithms, it returns `(pub, priv)` where `pub = hashlib.sha256(priv).digest()`.

**Pitfall**: If you unpack the return value as `pub, priv, extra = engine.generate_keypair()`, you'll get a ValueError for too many values to unpack. The return is always a 2-tuple.

### 17. Mutation.type Is a String
`Mutation.type` is a string, not an enum. Use `mutation.type.upper()` not `mutation.type.value.upper()`. Using `.value` causes `AttributeError`.

### 18. Post-Quantum Crypto Key Sizes
Kyber-768 public key is 512 bytes, private key is 576 bytes. Dilithium public key is 32 bytes, private key is 64 bytes (includes 32-byte seed + 32-byte signing key). Signature is 128 bytes (32-byte pk + 64-byte sig + 32-byte commitment).

**Pitfall**: Don't assume key sizes match the NIST parameter names. Kyber-768 has 512-byte public keys, not 768 bytes. Dilithium signatures are 128 bytes, not 64 bytes (the 64-byte sig is prefixed with 32-byte pk and suffixed with 32-byte commitment).

## Build Command

```bash
# MUST kill running exe first
taskkill /F /IM WebBuilder.exe 2>/dev/null
sleep 5

# Build with heavy module exclusions
pyinstaller --name "WebBuilder" --onefile --windowed \
  --exclude-module matplotlib --exclude-module numpy \
  --exclude-module pandas --exclude-module scipy \
  --exclude-module tkinter --exclude-module unittest \
  --exclude-module pytest --exclude-module setuptools \
  --exclude-module pip --exclude-module wheel \
  --add-data "webbuilder;webbuilder" \
  webbuilder_desktop.py
```

## Test Suite

```bash
cd /c/Users/Server/Desktop/WebBuilder
python -m pytest tests/unit/ -q --tb=no
```

Test structure:
```
tests/
├── conftest.py
├── fixtures/
├── unit/
│   ├── test_core.py
│   ├── test_features.py
│   ├── test_edge_cases.py
│   ├── test_ml_engine.py
│   └── test_ai_export_plugins.py
└── integration/
    └── test_all.py
```
