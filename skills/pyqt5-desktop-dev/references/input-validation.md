# Input Validation Framework

## FormValidator

Validates entire forms with per-field rules.

```python
from webbuilder.gui.validation import FormValidator, ValidationRule, Validators

fv = FormValidator()

# Add field with rules
fv.add_field("project_name", [
    ValidationRule("required", Validators.required, "Project name is required"),
    ValidationRule("min_length", Validators.min_length(3), "At least 3 characters"),
    ValidationRule("pattern", Validators.project_name, "Only letters, numbers, spaces, hyphens"),
])

fv.add_field("email", [
    ValidationRule("email", Validators.email, "Invalid email format"),
])

# Validate
valid, errors = fv.validate_form({"project_name": "My Project", "email": "test@example.com"})
if not valid:
    print(errors)  # {"field": "message"}
```

## Validators Class

Common validators:

- `Validators.required(value)` — Not empty
- `Validators.email(value)` — Email format
- `Validators.url(value)` — URL format
- `Validators.min_length(n)` — String length >= n
- `Validators.max_length(n)` — String length <= n
- `Validators.range(min, max)` — Numeric range
- `Validators.hex_color(value)` — #RRGGBB or #RGB
- `Validators.classname(value)` — CSS class name
- `Validators.id_name(value)` — HTML ID
- `Validators.filename(value)` — Safe filename

## ValidatedLineEdit

Line edit with built-in validation and visual feedback.

```python
from webbuilder.gui.validation import ValidatedLineEdit

edit = ValidatedLineEdit(validator_func=Validators.project_name)
# Shows red border when invalid
# Call edit.is_valid() before submitting
```

## Standalone Functions

```python
from webbuilder.gui.validation import (
    validate_project_name, validate_email, validate_url, validate_number
)

valid, msg = validate_project_name("My Project")
valid, msg = validate_email("test@example.com")
valid, msg = validate_url("https://example.com")
valid, msg = validate_number("42", 0, 100)
```

## Pitfall: Chain Imports

The `validation.py` module imports from PyQt5 only. It is safe to import from any module without circular import risk. Import at module level, not inside methods.
