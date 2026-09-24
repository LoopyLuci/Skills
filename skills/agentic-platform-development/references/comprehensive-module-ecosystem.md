# Comprehensive Module Ecosystem Pattern

For production-grade web builder platforms, a 50+ module architecture that covers all aspects of web development.

## Architecture Overview

```
webbuilder/
├── hardware/          # Multi-threading + multi-GPU HAL
├── mcp/               # Model Context Protocol (14 tools)
├── ai/                # 9 providers, GPU accelerator, cache, features
├── core/              # SQLite backend, project management
├── assets/            # Image pipeline, lazy loading
├── plugins/           # Plugin system v2 with hot-reload
├── gui/               # Adaptive main window, all dialogs
├── design/            # Color, typography, animation, tokens
├── ecommerce/         # Catalog, cart, orders, tax, shipping
├── seo/               # Meta tags, sitemap, robots.txt, Schema.org
├── content/           # Rich text, media library, newsletters
├── security/          # CSP, headers, CSRF, GDPR, scanner
├── devtools/          # Git, API tester, DB builder, profiler
├── performance/       # CSS/JS minifier, service worker, PWA
├── validation.py      # XSS, path traversal, API key
├── accessibility.py   # WCAG, screen reader, high contrast
├── i18n.py            # 6+ locales, RTL support
├── search.py          # Full-text + fuzzy search
├── sync.py            # Cloud sync, operational transform
├── autosave.py        # Crash recovery
└── contrib/
    └── performance.py # Auto-save, memory monitor, timer
```

## Module Categories

### 1. Design Studio (`design/studio.py`)
- Color with WCAG contrast checking
- Typography scale with modular ratios
- Animation keyframe system
- Design token manager for theming

### 2. AI Features (`ai/features.py`)
- Content writer with SEO optimization
- Code reviewer (XSS, SQL injection, secrets)
- SEO analyzer (title, meta, headings, images)
- Accessibility auditor (alt text, labels, semantics)

### 3. E-Commerce (`ecommerce/engine.py`)
- Product catalog with categories/tags
- Shopping cart with tax calculation
- Shipping calculator with weight-based rates
- Discount/coupon engine
- Order management with status tracking

### 4. SEO Marketing (`seo/marketing.py`)
- Meta tag generator (Open Graph, Twitter Card)
- XML sitemap generator
- Robots.txt generator
- Schema.org structured data builder
- Lighthouse-style performance audit

### 5. Content Management (`content/management.py`)
- Rich text editor with markdown
- Media library with tagging
- Content version history
- Newsletter builder
- RSS feed generator

### 6. Security (`security/compliance.py`)
- Content Security Policy builder
- Security headers configurator
- CSRF token generation/validation
- GDPR consent banner generator
- Vulnerability scanner

### 7. Developer Tools (`devtools/suite.py`)
- Git integration (status, commit, log, diff)
- API tester (GET, POST, PUT, DELETE)
- Database query builder
- Performance profiler

### 8. Performance (`performance/optimization.py`)
- CSS/JS minifier
- Critical CSS extractor
- Service worker generator
- PWA manifest generator

## Integration Patterns

### Each module provides:
1. **Data classes** for type-safe objects
2. **Manager classes** with business logic
3. **Singleton accessor** (`get_*()` function)
4. **State serialization** (`to_dict()` / `from_dict()`)

### Example pattern:
```python
@dataclass
class Product:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    price: Decimal = Decimal("0.00")

class ProductCatalog:
    def add_product(self, product: Product) -> None: ...
    def search(self, query: str) -> list[Product]: ...

_catalog: Optional[ProductCatalog] = None

def get_product_catalog() -> ProductCatalog:
    global _catalog
    if _catalog is None:
        _catalog = ProductCatalog()
    return _catalog
```

## Module Communication

Modules communicate through:
1. **Direct imports** for tight coupling (e.g., validation used everywhere)
2. **Events/hooks** for loose coupling (plugin system)
3. **Database** for persistent state (SQLite backend)
4. **File system** for assets and exports

## Testing Strategy

```python
# tests/integration/test_all.py
class TestModuleIntegration(unittest.TestCase):
    def test_product_to_order_flow(self):
        product = Product(name="Test", price=Decimal("29.99"))
        cart = ShoppingCart()
        cart.add_item(product, quantity=2)
        order = Order(cart_id=cart.id, items=cart.items)
        self.assertEqual(order.subtotal, Decimal("59.98"))
    
    def test_seo_audit_on_generated_html(self):
        html = generate_page(section)
        results = SEOAnalyzer().analyze(html)
        self.assertGreater(results["score"], 80)
```

## Pitfalls

1. **field(default_factory=list)**: The parentheses matter. `list` is the callable, `list()` is an empty list (wrong).
2. **Stale __pycache__**: Delete `__pycache__` directories when modules fail to import correctly.
3. **Circular imports**: Modules that depend on each other should use lazy imports or event systems.
4. **Missing package __init__.py**: New packages need `__init__.py` with exports to be importable.
5. **PermissionError on rebuild**: Kill running exe processes before rebuilding with PyInstaller.
6. **DPI detection failures**: Wrap `screen.logicalDotsPerInch()` in try/except with 96 DPI fallback.
7. **Multi-monitor scaling**: Detect screen changes via `moveEvent` and reapply stylesheet.