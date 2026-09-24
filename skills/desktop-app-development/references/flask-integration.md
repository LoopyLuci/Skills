# Flask Backend Integration Pattern

Integrate a Flask REST API backend with a PyQt5 desktop app for real-time data persistence, authentication, and server management.

## FlaskManager (QObject)

Runs Flask as a subprocess and communicates via HTTP:

```python
from PyQt5.QtCore import QObject, pyqtSignal, QTimer
import subprocess
import requests

class FlaskManager(QObject):
    status_changed = pyqtSignal(str, bool)
    
    def __init__(self, port=5000):
        super().__init__()
        self.process = None
        self.port = port
        self.base_url = f"httplocalhost:{port}"
    
    def start(self):
        if self.process and self.process.poll() is None:
            self.status_changed.emit("already_running", True)
            return
        try:
            app_path = Path(__file__).parent / "app.py"
            self.process = subprocess.Popen(
                [sys.executable, str(app_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
            )
            # Wait for server to start (poll health endpoint)
            import time
            for i in range(10):
                time.sleep(0.5)
                try:
                    r = requests.get(f"{self.base_url}/api/v1/health", timeout=1)
                    if r.status_code == 200:
                        self.status_changed.emit("running", True)
                        return
                except:
                    pass
            self.status_changed.emit("failed", False)
        except Exception as e:
            self.status_changed.emit(f"error: {e}", False)
    
    def stop(self):
        if self.process:
            self.process.terminate()
            self.process.wait(timeout=5)
            self.process = None
            self.status_changed.emit("stopped", False)
    
    def is_running(self):
        return self.process and self.process.poll() is None
    
    def api_get(self, endpoint):
        try:
            r = requests.get(f"{self.base_url}{endpoint}", timeout=5)
            return r.json()
        except:
            return None
    
    def api_post(self, endpoint, data=None):
        try:
            r = requests.post(f"{self.base_url}{endpoint}", json=data, timeout=5)
            return r.json()
        except:
            return None
```

## Status Indicator in StatusBar

```python
# In main window __init__:
self.flask = FlaskManager()
self.flask.status_changed.connect(self.on_flask_status)

# Add status indicator
self.flask_status = QLabel("⚪ Flask: Connecting...")
self.flask_status.setStyleSheet("color: #f59e0b; padding: 0 8px;")
self.statusBar().addPermanentWidget(self.flask_status)

def on_flask_status(self, status, running):
    if running:
        self.flask_status.setText("🟢 Flask: Running")
        self.flask_status.setStyleSheet("color: #10b981; padding: 0 8px;")
    else:
        self.flask_status.setText("🔴 Flask: Stopped")
        self.flask_status.setStyleSheet("color: #ef4444; padding: 0 8px;")
```

## Auto-start with Delay

```python
# In main window __init__:
QTimer.singleShot(1000, self.flask.start)
```

## Security Headers (Flask)

```python
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return response
```

## JWT Auth Flow

```python
# Flask side
class User(UserMixin, db.Model):
    def generate_token(self):
        payload = {
            'user_id': self.id,
            'exp': datetime.utcnow() + timedelta(hours=Config.JWT_EXPIRATION_HOURS),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')
    
    @staticmethod
    def verify_token(token):
        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            return User.query.get(payload['user_id'])
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token missing'}), 401
        token = token.replace('Bearer ', '')
        user = User.verify_token(token)
        if not user:
            return jsonify({'error': 'Invalid or expired token'}), 401
        return f(user, *args, **kwargs)
    return decorated
```

## Rate Limiting

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.route('/auth/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    # ...
```

## Pitfalls

1. **Process cleanup**: Always call `self.process.terminate()` and `wait()` to avoid zombie processes.
2. **Port conflicts**: Check if port is already in use before starting.
3. **Startup delay**: Flask takes ~2s to start; poll health endpoint rather than using fixed delay.
4. **Cross-thread signals**: Use `pyqtSignal` to communicate between FlaskManager thread and UI thread.
5. **CREATE_NO_WINDOW**: Use this flag on Windows to prevent console window from appearing.
