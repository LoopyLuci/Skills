# Export System & Plugin Architecture
## 2026-08-22

### Export System

Three export formats ensure 100-year survival:

1. **HTML Exporter**: Static, semantic, accessible HTML/CSS/JS. Works forever, any browser.
2. **React Exporter**: Components with hooks, Tailwind CSS. Industry standard.
3. **JSON Exporter**: Raw project data, versioned. For backup/restore.

```python
class HTMLExporter:
    def generate_html(self) -> str:
        sections = self.project['pages'][0]['sections']
        html = '<!DOCTYPE html><html><head>...</head><body>'
        for section in sections:
            html += self.render_section(section)
        html += '</body></html>'
        return html
    
    def render_section(self, section: Dict) -> str:
        renderers = {
            'hero-centered': self._render_hero_centered,
            'features-grid-3': self._render_features_grid,
            'pricing-3-tiers': self._render_pricing,
        }
        renderer = renderers.get(section['type'], self._render_placeholder)
        return renderer(section.get('props', {}))
```

### Plugin Architecture

Stable API for extensibility:

```python
class PluginInterface(ABC):
    @property
    @abstractmethod
    def name(self) -> str: pass
    
    @abstractmethod
    def initialize(self, config: Dict) -> bool: pass

class ComponentPlugin(PluginInterface):
    @abstractmethod
    def render(self, props: Dict) -> str: pass

class ExporterPlugin(PluginInterface):
    @abstractmethod
    def export(self, project: Dict, output_path: str) -> str: pass

class PluginRegistry:
    def register(self, plugin: PluginInterface): ...
    def get_component(self, name: str) -> Optional[ComponentPlugin]: ...

class PluginLoader:
    def load_all(self):
        for plugin_path in self.plugin_dir.iterdir():
            self._load_plugin(plugin_path)
```

### Project Schema Versioning

```python
class ProjectSchema:
    VERSION = "2.0.0"
    
    @staticmethod
    def validate(project: Dict) -> bool:
        return all(k in project for k in ['id', 'name', 'pages', 'design'])
    
    @staticmethod
    def migrate(project: Dict) -> Dict:
        version = project.get('version', '1.0.0')
        if version == '1.0.0':
            project['design'] = {
                'colors': project.pop('colors'),
                'fonts': project.pop('fonts')
            }
        return project
```

### Test Suite

23 tests covering:
- Schema validation and migration
- HTML, React, JSON export
- Plugin registry and loading
- Backward compatibility
- Full integration pipeline

Run with: `python -m pytest test_suite.py -v`
