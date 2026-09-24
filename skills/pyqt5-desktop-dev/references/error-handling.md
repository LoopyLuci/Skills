# Centralized Exception Handling

## ErrorLogger

Records errors with context, maintains history, persists critical errors.

```python
from webbuilder.gui.error_handler import ErrorLogger, get_error_logger

logger = get_error_logger()

# Log an error
try:
    raise ValueError("Invalid input")
except ValueError as e:
    record = logger.log_error(
        component="FormBuilder",
        error=e,
        context={"field": "email"},
        recoverable=True,
    )

# Get recent errors
errors = logger.get_recent_errors(count=10)
stats = logger.get_error_summary()
```

## SafeExecutor

Wraps dangerous operations with fallback defaults.

```python
from webbuilder.gui.error_handler import get_safe_executor

executor = get_safe_executor()

# Synchronous
result = executor.execute(
    lambda: int(user_input),
    component="InputValidation",
    default=0,
)

# Asynchronous
def on_error(e):
    print(f"Async failed: {e}")

executor.execute_async(
    lambda: fetch_data(),
    component="API",
    on_error=on_error,
)
```

## GlobalExceptionHook

Catches uncaught exceptions via `sys.excepthook`.

```python
from webbuilder.gui.error_handler import install_exception_hook

# Install in main window __init__
install_exception_hook(self)
```

## safe_slot Decorator

Wraps Qt slots with error handling.

```python
from webbuilder.gui.error_handler import safe_slot

class MyWidget(QWidget):
    @safe_slot
    def on_button_clicked(self):
        # If this raises, the error is logged and a message box is shown
        raise ValueError("Something went wrong")
```

## ErrorDialog

Shows detailed error information with copy-to-clipboard.

```python
from webbuilder.gui.error_handler import ErrorDialog

dialog = ErrorDialog(record, parent=self)
dialog.exec_()
```

## Pitfall: Circular Imports

The `error_handler.py` imports from `PyQt5` only — no webbuilder modules. This prevents circular imports when adding error handling to low-level modules. Always keep error handlers at the leaf level of the import graph.