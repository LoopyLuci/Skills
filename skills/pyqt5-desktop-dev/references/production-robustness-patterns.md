# Production Robustness Patterns for PyQt5 + Flask Apps

This reference covers the production-grade robustness patterns that emerged from building a full-featured PyQt5 desktop app with Flask backend.

## 1. Structured Logging

```python
# webbuilder/logging_config.py
import logging
import logging.handlers
from pathlib import Path

def setup_logging(name="webbuilder", level=logging.INFO, log_dir=None):
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d | %(message)s"
    )

    # Console
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)

    # Rotating file (10MB, 5 backups)
    file_handler = logging.handlers.RotatingFileHandler(
        log_dir / f"{name}.log", maxBytes=10*1024*1024, backupCount=5
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Error-only file
    error_handler = logging.handlers.RotatingFileHandler(
        log_dir / f"{name}.error.log", maxBytes=10*1024*1024, backupCount=5
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)

    return logger
```

**Usage in every module:**
```python
from webbuilder.logging_config import get_logger
logger = get_logger("module_name")
```

## 2. Custom Exception Hierarchy

```python
# webbuilder/exceptions.py
class WebBuilderError(Exception):
    def __init__(self, message, details=None):
        super().__init__(message)
        self.message = message
        self.details = details or {}

# Domain-specific exceptions
class ProjectNotFoundError(WebBuilderError): ...
class ProjectValidationError(WebBuilderError): ...
class ProjectPersistenceError(WebBuilderError): ...
class AssetNotFoundError(WebBuilderError): ...
class AssetValidationError(WebBuilderError): ...
class PathTraversalError(WebBuilderError): ...
class AIAPIError(WebBuilderError): ...
class AIRateLimitError(WebBuilderError): ...
class DeploymentPlatformNotSupportedError(WebBuilderError): ...
```

**Key principle:** Every exception carries a `details` dict for programmatic error handling.

## 3. Circuit Breaker Pattern (AI APIs)

```python
class CircuitBreaker:
    def __init__(self, threshold=5, timeout=60):
        self.threshold = threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = 0.0
        self.state = "closed"  # closed, open, half-open

    def can_execute(self) -> bool:
        if self.state == "closed":
            return True
        if self.state == "open":
            if time.time() - self.last_failure_time >= self.timeout:
                self.state = "half-open"
                return True
            return False
        return True  # half-open

    def record_success(self):
        self.failure_count = 0
        self.state = "closed"

    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.threshold:
            self.state = "open"
```

## 4. Retry with Exponential Backoff

```python
for attempt in range(config.ai_max_retries):
    try:
        # API call
        self.circuit_breaker.record_success()
        return
    except AIRateLimitError as e:
        wait_time = e.details.get("retry_after_seconds", 60)
        await asyncio.sleep(wait_time)
    except AIAPIError as e:
        self.circuit_breaker.record_failure()
        wait_time = config.ai_retry_delay * (config.ai_retry_backoff ** attempt)
        await asyncio.sleep(wait_time)
```

## 5. Atomic File Saves

```python
def save(self, project):
    # Write to temp file first
    temp_path = path.with_suffix(".tmp")
    with open(temp_path, "w") as f:
        json.dump(project.to_dict(), f)
    # Atomic rename
    temp_path.replace(path)
```

## 6. Input Validation & Sanitization

```python
# webbuilder/validation.py
def sanitize_string(value, max_length=10000):
    value = value.strip()
    if len(value) > max_length:
        value = value[:max_length]
    return html.escape(value)

def sanitize_filename(filename):
    filename = os.path.basename(filename)
    filename = re.sub(r'[^\w\-.]', '_', filename)
    return filename

def sanitize_path(path, base_path):
    resolved = (base_path / path).resolve()
    if not str(resolved).startswith(str(base_path.resolve())):
        raise PathTraversalError(path)
    return resolved
```

## 7. Flask Error Handling Middleware

```python
@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f"Internal error: {error}\n{traceback.format_exc()}")
    db.session.rollback()
    return jsonify({"error": "Internal server error"}), 500

@app.before_request
def log_request():
    g.start_time = datetime.utcnow()

@app.after_request
def log_response(response):
    duration = (datetime.utcnow() - g.start_time).total_seconds()
    app.logger.info(f"{request.method} {request.path} {response.status_code} ({duration:.3f}s)")
    return response
```

## 8. Environment-Based Configuration

```python
# webbuilder/config.py
@dataclass
class AppConfig:
    storage_path: Path = field(default_factory=lambda: Path.home() / ".webbuilder" / "projects")
    log_level: str = "INFO"
    ai_max_retries: int = 3
    ai_retry_delay: float = 1.0
    ai_circuit_breaker_threshold: int = 5
    
    @classmethod
    def from_env(cls) -> "AppConfig":
        config = cls()
        config.log_level = os.environ.get("WB_LOG_LEVEL", config.log_level)
        if val := os.environ.get("WB_AI_MAX_RETRIES"):
            config.ai_max_retries = int(val)
        return config
```

## 9. Global Exception Handler (GUI)

```python
def setup_exception_handler(app):
    def exc_hook(exctype, value, tb):
        error_msg = ''.join(traceback.format_exception(exctype, value, tb))
        logger.error(f"Uncaught exception:\n{error_msg}")
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("An unexpected error occurred")
        msg.setInformativeText(str(value))
        msg.setDetailedText(error_msg)
        msg.exec_()
        sys._excepthook(exctype, value, tb)
    
    sys._excepthook = sys.excepthook
    sys.excepthook = exc_hook
```

## 10. GUI Method Error Wrapping Pattern

Every public method in the main window should follow this pattern:

```python
def save_project(self):
    try:
        if not self.current_project:
            return
        self.current_project.pages[0].sections = self.canvas.sections
        self.project_manager.save(self.current_project)
        self.project_status.setText(f"  💾 {self.current_project.name}")
        logger.info(f"Project saved: {self.current_project.name}")
    except Exception as e:
        logger.error(f"Failed to save project: {e}")
        QMessageBox.warning(self, "Error", f"Failed to save project: {e}")
```

**Critical:** Never let exceptions propagate uncaught in GUI methods — they crash the app silently.