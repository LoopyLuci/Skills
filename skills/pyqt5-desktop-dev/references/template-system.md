# Template System with Pre-built Templates

## Pattern

Use a `TemplateManager` class that loads built-in templates and converts them to `Project` instances. Templates share the same `Section`/`Page`/`Design` dataclasses as projects.

## Architecture

```python
@dataclass
class Template:
    id: str
    name: str
    description: str
    category: str
    thumbnail: str
    sections: list[Section]
    design: Design
    tags: list[str]

    def to_project(self, project_id: str, name: str) -> Project:
        # Convert template sections to project sections
        # Deep-copy props to avoid mutation
        ...

class TemplateManager:
    def __init__(self):
        self.templates: dict[str, Template] = {}
        self._load_builtin_templates()

    def get_template(self, id: str) -> Optional[Template]: ...
    def get_all_templates(self) -> list[Template]: ...
    def get_templates_by_category(self, category: str) -> list[Template]: ...
    def search_templates(self, query: str) -> list[Template]: ...
    def create_project_from_template(self, template_id: str, project_id: str, name: str) -> Optional[Project]: ...
```

## GUI Integration

```python
class TemplateBrowserDialog(QDialog):
    # Search bar + category filter
    # Grid of template cards (thumbnail, name, description, category)
    # Click to select, "Use Template" button
    def _create_template_card(self, template: Template) -> QWidget:
        card = QFrame()
        # ... layout with thumbnail, name, description, category
        card.mousePressEvent = lambda e, t=template: self._select_template(t)
        return card

# In WebBuilderWindow.menu:
template_action = QAction("New from Template...", self)
template_action.setShortcut("Ctrl+Shift+N")
template_action.triggered.connect(self.new_from_template)

# In WebBuilderWindow.new_from_template:
def new_from_template(self):
    dialog = TemplateBrowserDialog(self)
    if dialog.exec_() == QDialog.Accepted:
        template = dialog.get_selected_template()
        if template:
            project = template.to_project(project_id, f"New {template.name}")
            self.current_project = project
            self.canvas.sections = list(project.pages[0].sections)
            self._update_preview()
```

## Template Categories

- Business (SaaS Landing, Digital Agency)
- Creative (Portfolio)
- E-commerce (Online Store)
- Food & Drink (Restaurant)
- Content (Blog & Magazine)

## Key Decisions

1. **Templates use same dataclasses** — No separate TemplateSection; reuse `Section` directly
2. **Deep-copy props** — `s.props.copy()` prevents template mutation
3. **Categories + tags** — Categories for broad filtering, tags for search
4. **Thumbnail as emoji** — Simple, no external assets needed
5. **Project ID generation** — Use timestamp: `f"project-{datetime.now().strftime('%Y%m%d%H%M%S')}"`
