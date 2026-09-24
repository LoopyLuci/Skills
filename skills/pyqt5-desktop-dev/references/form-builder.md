# Form Builder with Interactive Forms

## Pattern

A `FormBuilder` class that manages form definitions and generates HTML for embedding in exported projects. Forms support 10 field types with validation.

## Architecture

```python
@dataclass
class FormField:
    id: str
    type: str  # text, email, phone, textarea, select, checkbox, radio, number, date, file
    label: str
    placeholder: str = ""
    required: bool = False
    options: list[str] = field(default_factory=list)  # for select/radio
    validation: dict[str, Any] = field(default_factory=dict)
    order: int = 0

@dataclass
class Form:
    id: str
    name: str
    fields: list[FormField]
    submit_text: str = "Submit"
    success_message: str = "Thank you for your submission!"
    redirect_url: str = ""
    email_notifications: list[str] = field(default_factory=list)

class FormBuilder:
    FIELD_TYPES = {
        "text": {"label": "Text Input", "icon": "✏️"},
        "email": {"label": "Email Input", "icon": "📧"},
        "phone": {"label": "Phone Input", "icon": "📞"},
        "textarea": {"label": "Text Area", "icon": "📝"},
        "select": {"label": "Dropdown", "icon": "📋"},
        "checkbox": {"label": "Checkbox", "icon": "☑️"},
        "radio": {"label": "Radio Buttons", "icon": "🔘"},
        "number": {"label": "Number Input", "icon": "🔢"},
        "date": {"label": "Date Picker", "icon": "📅"},
        "file": {"label": "File Upload", "icon": "📎"},
    }

    def create_form(self, name: str) -> Form: ...
    def add_field(self, form_id: str, field_type: str, label: str, **kwargs) -> Optional[FormField]: ...
    def remove_field(self, form_id: str, field_id: str) -> bool: ...
    def validate_submission(self, form_id: str, data: dict) -> list[str]: ...
    def submit_form(self, form_id: str, data: dict) -> dict[str, Any]: ...
    def get_submissions(self, form_id: str) -> list[dict]: ...
    def to_html(self, form: Form) -> str: ...
```

## Field Type Rendering

Each field type maps to an HTML input type:

| Field Type | HTML Input | Validation |
|-----------|------------|------------|
| text | `<input type="text">` | min/max length |
| email | `<input type="email">` | regex pattern |
| phone | `<input type="tel">` | regex pattern |
| textarea | `<textarea>` | min/max length |
| select | `<option>` items | - |
| checkbox | `<input type="checkbox">` | - |
| radio | `<input type="radio">` items | - |
| number | `<input type="number">` | numeric parse |
| date | `<input type="date">` | ISO format |
| file | `<input type="file">` | - |

## Validation Pattern

```python
def validate_submission(self, form_id: str, data: dict) -> list[str]:
    errors = []
    for field in form.fields:
        value = data.get(field.id, "")

        # Required check
        if field.required and not value:
            errors.append(f"{field.label} is required")
            continue

        # Type-specific validation
        if field.type == "email" and value:
            if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", value):
                errors.append(f"{field.label} must be a valid email")

        # Custom validation rules
        if "min_length" in field.validation and len(str(value)) < field.validation["min_length"]:
            errors.append(f"{field.label} must be at least {field.validation['min_length']} characters")
```

## Key Decisions

1. **10 field types** — Covers most common form use cases
2. **Validation rules dict** — Extensible: `{"min_length": 5, "max_length": 100, "pattern": r"..."}`
3. **HTML export** — `to_html()` generates embeddable form HTML for export
4. **Submission storage** — In-memory list with export capability
5. **Global singleton** — `form_builder = FormBuilder()` at module level
