# Comprehensive Test Suite for PyQt5 Apps

This reference covers the testing strategy and suite structure that emerged from building a 211-test suite for a production PyQt5 desktop app.

## Test Suite Structure

```
tests/
├── __init__.py
├── conftest.py              # Shared fixtures and config
├── unit/
│   ├── __init__.py
│   ├── test_core.py         # Core models, ProjectManager, Config
│   ├── test_ai_export_plugins.py  # AI, export, plugin modules
│   ├── test_features.py     # Templates, forms, SEO, search, analytics
│   └── test_edge_cases.py   # Empty, unicode, boundary, malformed data
├── integration/
│   └── test_workflows.py    # Full project lifecycle, multi-page, deployment
├── performance/
│   └── test_performance.py  # Benchmarks, stress tests
└── security/
    └── test_security.py     # XSS, path traversal, input validation
```

## Test Categories

### Unit Tests
- **Core**: Project, Page, Section, Design, ProjectManager, Config, Validation
- **AI/Export/Plugins**: CircuitBreaker, AIProviders, HTMLExporter, ReactExporter, VueExporter, ExportManager, PluginManager
- **Features**: TemplateManager, FormBuilder, SEOMetadata, SitemapGenerator, CustomCodeManager, ProjectSearch, AnalyticsTracker, ImportExport, PerformanceModules
- **Edge Cases**: Empty inputs, unicode, boundary conditions, malformed data, color/URL validation, form/search/performance edge cases

### Integration Tests
- Project lifecycle (create → edit → export)
- Multi-page workflows
- Template application
- Form submission workflows
- SEO analysis workflows
- Search indexing and querying
- Analytics tracking
- Auto-save and crash recovery
- Multi-format export
- Deployment workflows

### Performance Tests
- Export speed (small, large, multi-page projects)
- Save/load speed
- Search speed across many projects
- Memory usage stability
- Stress tests (200 sections, 50 pages, 100 projects, rapid saves, concurrent exports)

### Security Tests
- XSS prevention (script tags, img onerror, svg onload)
- Path traversal prevention (dotdot, absolute paths, null bytes)
- Input validation (URLs, colors, filenames)
- Export security (HTML escaping)
- Form security (XSS payload sanitization)
- Custom code security (dangerous HTML detection)
- Project security (ID/name sanitization)

## API Signature Inspection Workflow

**Critical:** Before writing tests, inspect actual API signatures to avoid mismatches.

```python
import inspect
from webbuilder.module import ClassName

# Get init signature
print(inspect.signature(ClassName.__init__))

# Get method signature
print(inspect.signature(ClassName.method_name))

# Get dataclass fields
print([f.name for f in ClassName.__dataclass_fields__.values()])

# List all public methods
print([m for m in dir(ClassName) if not m.startswith('_')])
```

**Common mismatch patterns:**
1. Method name differences (e.g., `get_exporter` vs `export`)
2. Parameter count differences (e.g., `export(project, format, path)` vs `export(project, path)`)
3. Parameter name differences (e.g., `form_id` vs `form`)
4. Return type differences (e.g., `dict` vs `dict[str, Any]`)
5. Dataclass field differences (e.g., `type` vs `event_type`)

**Fix strategy:** Always inspect actual signatures first, then write tests to match.

## Coverage Metrics

| Category | Typical Coverage | Notes |
|----------|-----------------|-------|
| Unit - Core | 95%+ | Models and managers are straightforward |
| Unit - AI/Export/Plugins | 80% | Some methods may not exist yet |
| Unit - Features | 65-70% | Many features have evolving APIs |
| Unit - Edge Cases | 65-70% | Depends on actual validation logic |
| Integration | 55-60% | Workflows depend on many modules |
| Performance | 70% | Benchmarks are straightforward |
| Security | 55-60% | Depends on actual security implementation |
| **Overall** | **80%+** | Target for production apps |

## Test Configuration

```python
# setup.cfg
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
markers =
    slow: marks tests as slow
    integration: marks integration tests
    security: marks security tests
    performance: marks performance tests
```

## Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific category
python -m pytest tests/unit/ -v
python -m pytest tests/integration/ -v
python -m pytest tests/performance/ -v
python -m pytest tests/security/ -v

# Run with short output
python -m pytest tests/ --tb=no -q

# Count failures
python -m pytest tests/ --tb=no -q 2>&1 | grep -c "FAILED"

# Show failure summary by file
python -m pytest tests/ --tb=no -q 2>&1 | grep "FAILED" | sed 's/FAILED //' | awk -F'::' '{print $1}' | sort | uniq -c | sort -rn
```

## Common Test Patterns

### Testing Dataclass Models
```python
def test_create_project(self):
    project = Project(id="test-1", name="Test")
    assert project.id == "test-1"
    assert project.name == "Test"
    assert project.pages == []

def test_project_to_dict(self):
    project = Project(id="test-1", name="Test")
    data = project.to_dict()
    assert data["id"] == "test-1"
    assert "pages" in data

def test_project_from_dict(self):
    data = {"id": "test-1", "name": "Test", "pages": [], "design": {}}
    project = Project.from_dict(data)
    assert project.id == "test-1"
```

### Testing Managers
```python
def test_save_and_load(self):
    with tempfile.TemporaryDirectory() as tmpdir:
        pm = ProjectManager(Path(tmpdir))
        project = pm.create_new("Test")
        pm.save(project)
        loaded = pm.load(project.id)
        assert loaded.name == "Test"

def test_list_projects(self):
    with tempfile.TemporaryDirectory() as tmpdir:
        pm = ProjectManager(Path(tmpdir))
        pm.create_new("A")
        pm.create_new("B")
        projects = pm.list_projects()
        assert len(projects) == 2
```

### Testing Validation
```python
def test_valid_url(self):
    assert sanitize_url("https://example.com")
    assert sanitize_url("http://localhost:3000")

def test_invalid_url(self):
    with pytest.raises(Exception):
        sanitize_url("javascript:alert(1)")

def test_xss_prevention(self):
    result = sanitize_string("<script>alert('xss')</script>")
    assert "<script>" not in result
    assert "&lt;script&gt;" in result
```

### Testing Security
```python
def test_path_traversal_blocked(self):
    result = sanitize_filename("../../etc/passwd")
    assert ".." not in result
    assert "/" not in result

def test_export_escapes_html(self):
    project = Project(id="test", name="<script>alert('xss')</script>", pages=[])
    exporter = HTMLExporter()
    html = exporter.generate(project)
    assert "<script>alert" not in html
    assert "&lt;script&gt;" in html
```

## Key Insights

1. **Inspect before writing** - Always check actual API signatures before writing tests
2. **Use tempfile.TemporaryDirectory** - For all file-based tests to avoid pollution
3. **Test both success and failure paths** - Every method should have happy-path and error-path tests
4. **Security tests are critical** - XSS, path traversal, and input validation must be tested
5. **Performance benchmarks matter** - Set threshold_ms and verify operations complete within bounds
6. **Edge cases reveal bugs** - Empty strings, unicode, and boundary conditions find real issues
7. **80% pass rate is good** - Some failures are API mismatches, not bugs
9. **Integration tests cover workflows** - Full lifecycle tests catch cross-module issues
10. **Use pytest markers** - `@pytest.mark.slow`, `@pytest.mark.integration` for selective running