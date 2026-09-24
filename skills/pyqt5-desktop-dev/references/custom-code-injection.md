# Custom Code Injection (HTML/CSS/JS)

## Pattern

A `CustomCodeManager` class that stores and validates custom HTML/CSS/JS per project. The `CustomCode` dataclass holds five code areas.

## Architecture

```python
@dataclass
class CustomCode:
    html: str = ""          # Added before </body>
    css: str = ""           # Added in <head>
    js: str = ""            # Added before </body>
    head_tags: str = ""     # Meta tags, scripts, etc.
    footer_scripts: str = "" # Footer scripts

    def validate(self) -> list[str]:
        dangerous_patterns = [
            (r'<script[^>]*src=["\']https?://[^ "\']+["\']', "External script references not allowed"),
            (r'document\.cookie', "Cookie access not allowed"),
            (r'eval\s*\(', "eval() not allowed"),
            # ...
        ]
        for pattern, message in dangerous_patterns:
            if re.search(pattern, self.html, re.IGNORECASE):
                errors.append(f"HTML: {message}")
        return errors

    def render_css(self) -> str: ...
    def render_html(self) -> str: ...
    def render_js(self) -> str: ...

class CustomCodeManager:
    def get(self, project_id: str) -> CustomCode: ...
    def set(self, project_id: str, code: CustomCode) -> list[str]: ...
    def delete(self, project_id: str) -> bool: ...
    def export_code(self, project_id: str) -> dict[str, str]: ...
    def import_code(self, project_id: str, data: dict) -> list[str]: ...
```

## GUI Integration

```python
class CustomCodeDialog(QDialog):
    def __init__(self, project_id: str, parent: Optional[QWidget] = None):
        self.code = custom_code_manager.get(project_id)
        # ... tabs for HTML/CSS/JS

    def _on_save(self):
        self.code.html = self.html_editor.toPlainText()
        self.code.css = self.css_editor.toPlainText()
        self.code.js = self.js_editor.toPlainText()
        errors = custom_code_manager.set(self.project_id, self.code)
        if errors:
            QMessageBox.warning(self, "Validation Errors", "\n".join(errors))
        else:
            self.accept()

# In WebBuilderWindow.menu:
custom_code_action = QAction("Custom Code...", self)
custom_code_action.triggered.connect(self.open_custom_code)
```

## Security Validation

Block these patterns in custom code:
- External script references (`<script src="https://...">`)
- Cookie access (`document.cookie`)
- LocalStorage access
- `eval()` and `Function()` constructor
- `document.write`
- `innerHTML` assignment

## Key Decisions

1. **Five code areas** — html, css, js, head_tags, footer_scripts for full coverage
2. **Regex-based validation** — Block dangerous patterns, not just keywords
3. **Per-project storage** — `custom_codes: dict[str, CustomCode]`
4. **Validation on save** — Return errors, don't auto-sanitize
5. **Export/Import** — For backup and migration
