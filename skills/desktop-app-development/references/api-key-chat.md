# API Key Management & Agent Chat

Secure API key storage, provider configuration, and in-app agent chat interface for desktop applications.

## ConfigManager

Centralized configuration with secure key storage:

```python
from pathlib import Path
import json

class Config:
    CONFIG_DIR = Path.home() / ".webbuilder"
    CONFIG_FILE = CONFIG_DIR / "config.json"
    
    PROVIDERS = {
        'openai': {
            'name': 'OpenAI',
            'icon': '🟢',
            'models_endpoint': 'https://api.openai.com/v1/models',
            'key_prefix': 'sk-',
            'supports_vision': True,
            'supports_tools': True,
            'max_tokens': 128000,
        },
        'anthropic': {
            'name': 'Anthropic',
            'icon': '🟣',
            'models_endpoint': 'https://api.anthropic.com/v1/messages',
            'key_prefix': 'sk-ant-',
            'supports_vision': True,
            'supports_tools': True,
            'max_tokens': 200000,
        },
        'google': {
            'name': 'Google AI',
            'icon': '🔵',
            'models_endpoint': 'https://generativelanguage.googleapis.com/v1beta/models',
            'key_prefix': 'AIza',
            'supports_vision': True,
            'supports_tools': True,
            'max_tokens': 1000000,
        },
        'azure': {
            'name': 'Azure OpenAI',
            'icon': '🔷',
            'models_endpoint': None,
            'key_prefix': '',
            'supports_vision': True,
            'supports_tools': True,
            'max_tokens': 128000,
        },
        'custom': {
            'name': 'Custom Provider',
            'icon': '⚙️',
            'models_endpoint': None,
            'key_prefix': '',
            'supports_vision': False,
            'supports_tools': False,
            'max_tokens': 4096,
        }
    }

class ConfigManager:
    def __init__(self):
        self.config_dir = Config.CONFIG_DIR
        self.config_file = Config.CONFIG_FILE
        self.keys = {}
        self.settings = {}
        self.ensure_config_dir()
        self.load()
    
    def ensure_config_dir(self):
        self.config_dir.mkdir(parents=True, exist_ok=True)
    
    def load(self):
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    self.settings = data.get('settings', {})
                    self.keys = data.get('keys', {})
            except:
                self.settings = self.get_default_settings()
                self.keys = {}
        else:
            self.settings = self.get_default_settings()
            self.keys = {}
    
    def save(self):
        data = {'settings': self.settings, 'keys': self.keys}
        with open(self.config_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_default_settings(self):
        return {
            'theme': 'dark',
            'font_size': 14,
            'auto_save': True,
            'auto_save_interval': 30,
            'default_provider': 'openai',
            'default_model': 'gpt-4o',
            'streaming': True,
            'max_tokens': 4096,
            'temperature': 0.7,
        }
    
    def get_setting(self, key, default=None):
        return self.settings.get(key, default)
    
    def set_setting(self, key, value):
        self.settings[key] = value
        self.save()
    
    def get_api_key(self, provider):
        return self.keys.get(provider, '')
    
    def set_api_key(self, provider, key):
        self.keys[provider] = key
        self.save()
    
    def remove_api_key(self, provider):
        if provider in self.keys:
            del self.keys[provider]
            self.save()
    
    def get_providers_with_keys(self):
        return [p for p in self.keys if self.keys[p]]
```

## API Key Setup Dialog

Tabbed dialog for configuring multiple providers:

```python
class APIKeySetupDialog(QDialog):
    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config = config_manager
        self.setWindowTitle("API Key Setup")
        self.setFixedSize(500, 400)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        header = QLabel("🔑 API Key Configuration")
        header.setFont(QFont("Inter", 14, QFont.Bold))
        layout.addWidget(header)
        
        desc = QLabel("Configure your API keys to enable AI features.")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        tabs = QTabWidget()
        tabs.setDocumentMode(True)
        
        for provider_id, provider_info in Config.PROVIDERS.items():
            widget = QWidget()
            form = QFormLayout(widget)
            
            # Provider name with icon
            name_label = QLabel(f"{provider_info['icon']} {provider_info['name']}")
            name_label.setFont(QFont("Inter", 12, QFont.Bold))
            form.addRow(name_label)
            
            # API key input
            key_input = QLineEdit()
            key_input.setPlaceholderText(f"Enter your {provider_info['name']} API key...")
            key_input.setEchoMode(QLineEdit.Password)
            key_input.setText(self.config.get_api_key(provider_id))
            form.addRow("API Key:", key_input)
            
            # Show/hide key
            show_check = QCheckBox("Show key")
            show_check.stateChanged.connect(
                lambda state, inp=key_input: inp.setEchoMode(QLineEdit.Normal if state else QLineEdit.Password)
            )
            form.addRow("", show_check)
            
            # Test connection button
            test_btn = QPushButton("Test Connection")
            test_btn.clicked.connect(
                lambda checked, p=provider_id, k=key_input: self.test_connection(p, k.text())
            )
            form.addRow("", test_btn)
            
            # Save button
            save_btn = QPushButton("Save Key")
            save_btn.clicked.connect(
                lambda checked, p=provider_id, k=key_input: self.save_key(p, k.text())
            )
            form.addRow("", save_btn)
            
            tabs.addTab(widget, f"{provider_info['icon']} {provider_info['name']}")
        
        layout.addWidget(tabs)
    
    def save_key(self, provider, key):
        if key:
            self.config.set_api_key(provider, key)
            QMessageBox.information(self, "Success", f"API key for {Config.PROVIDERS[provider]['name']} saved!")
        else:
            self.config.remove_api_key(provider)
            QMessageBox.information(self, "Removed", f"API key removed.")
    
    def test_connection(self, provider, key):
        if not key:
            QMessageBox.warning(self, "Error", "Please enter an API key first.")
            return
        # In production, make actual API call
        QMessageBox.information(self, "Test", f"Connection test for {Config.PROVIDERS[provider]['name']} would be performed here.")
```

## Agent Chat Widget

Full chat interface with provider/model selection:

```python
class AgentChatWidget(QWidget):
    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config = config_manager
        self.conversation_history = []
        self.current_provider = None
        self.current_model = None
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header with provider/model selection
        header = QWidget()
        header.setFixedHeight(50)
        header.setStyleSheet("background: #1e293b; border-bottom: 1px solid #334155;")
        header_layout = QHBoxLayout(header)
        
        self.provider_combo = QComboBox()
        self.update_providers()
        self.provider_combo.currentTextChanged.connect(self.on_provider_changed)
        header_layout.addWidget(QLabel("Provider:"))
        header_layout.addWidget(self.provider_combo)
        
        self.model_combo = QComboBox()
        self.model_combo.setMinimumWidth(200)
        header_layout.addWidget(QLabel("Model:"))
        header_layout.addWidget(self.model_combo)
        
        refresh_btn = QPushButton("🔄")
        refresh_btn.clicked.connect(self.refresh_models)
        header_layout.addWidget(refresh_btn)
        
        header_layout.addStretch()
        
        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.clear_chat)
        header_layout.addWidget(clear_btn)
        
        layout.addWidget(header)
        
        # Chat messages area
        self.chat_area = QScrollArea()
        self.chat_area.setWidgetResizable(True)
        self.chat_area.setStyleSheet("background: #0f172a; border: none;")
        
        self.chat_content = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_content)
        self.chat_layout.setAlignment(Qt.AlignTop)
        self.chat_layout.setSpacing(8)
        self.chat_layout.setContentsMargins(16, 16, 16, 16)
        
        self.chat_area.setWidget(self.chat_content)
        layout.addWidget(self.chat_area)
        
        # Input area
        input_widget = QWidget()
        input_widget.setFixedHeight(80)
        input_widget.setStyleSheet("background: #1e293b; border-top: 1px solid #334155;")
        input_layout = QHBoxLayout(input_widget)
        
        self.message_input = QTextEdit()
        self.message_input.setPlaceholderText("Type your message... (Ctrl+Enter to send)")
        self.message_input.setFixedHeight(60)
        self.message_input.installEventFilter(self)
        input_layout.addWidget(self.message_input)
        
        send_btn = QPushButton("Send")
        send_btn.setFixedSize(60, 60)
        send_btn.clicked.connect(self.send_message)
        input_layout.addWidget(send_btn)
        
        layout.addWidget(input_widget)
        
        self.add_message("assistant", "Hello! I'm your AI assistant. How can I help you today?")
    
    def update_providers(self):
        self.provider_combo.clear()
        providers = self.config.get_providers_with_keys()
        for provider in providers:
            if provider in Config.PROVIDERS:
                self.provider_combo.addItem(f"{Config.PROVIDERS[provider]['icon']} {Config.PROVIDERS[provider]['name']}", provider)
        if not providers:
            self.provider_combo.addItem("⚙️ No API keys configured", None)
    
    def on_provider_changed(self, text):
        provider = self.provider_combo.currentData()
        if provider:
            self.current_provider = provider
            self.refresh_models()
    
    def refresh_models(self):
        self.model_combo.clear()
        provider = self.provider_combo.currentData()
        if not provider:
            return
        models = self.get_default_models(provider)
        for model in models:
            self.model_combo.addItem(model)
    
    def get_default_models(self, provider):
        models = {
            'openai': ['gpt-4o', 'gpt-4o-mini', 'gpt-4-turbo', 'gpt-3.5-turbo', 'o1-preview', 'o1-mini'],
            'anthropic': ['claude-3-5-sonnet-20241022', 'claude-3-5-haiku-20241022', 'claude-3-opus-20240229'],
            'google': ['gemini-1.5-pro', 'gemini-1.5-flash', 'gemini-1.0-pro'],
            'azure': ['gpt-4o', 'gpt-4-turbo', 'gpt-3.5-turbo'],
            'custom': ['custom-model'],
        }
        return models.get(provider, ['default'])
    
    def add_message(self, role, content):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        if role == "user":
            layout.addStretch()
            bubble = QLabel(content)
            bubble.setWordWrap(True)
            bubble.setMaximumWidth(500)
            bubble.setStyleSheet("background: #3b82f6; color: white; padding: 10px 14px; border-radius: 12px 12px 4px 12px;")
            layout.addWidget(bubble)
        else:
            bubble = QLabel(content)
            bubble.setWordWrap(True)
            bubble.setMaximumWidth(500)
            bubble.setStyleSheet("background: #334155; color: #f8fafc; padding: 10px 14px; border-radius: 12px 12px 12px 4px;")
            layout.addWidget(bubble)
            layout.addStretch()
        
        self.chat_layout.addWidget(widget)
        QTimer.singleShot(100, lambda: self.chat_area.verticalScrollBar().setValue(self.chat_area.verticalScrollBar().maximum()))
    
    def send_message(self):
        message = self.message_input.toPlainText().strip()
        if not message:
            return
        self.add_message("user", message)
        self.message_input.clear()
        self.conversation_history.append({"role": "user", "content": message})
        
        provider = self.provider_combo.currentData()
        if not provider:
            self.add_message("assistant", "Please configure an API key in Settings first.")
            return
        
        QTimer.singleShot(500, lambda: self.simulate_response(message))
    
    def simulate_response(self, user_message):
        responses = [
            f"I understand you want help with: '{user_message}'. Let me think about that...",
            f"Great question! Here's what I can tell you about '{user_message}'...",
        ]
        import random
        response = random.choice(responses)
        self.add_message("assistant", response)
        self.conversation_history.append({"role": "assistant", "content": response})
    
    def eventFilter(self, obj, event):
        if obj == self.message_input and event.type() == event.KeyPress:
            if event.key() == Qt.Key_Return and event.modifiers() == Qt.ControlModifier:
                self.send_message()
                return True
        return super().eventFilter(obj, event)
```

## Settings Dialog

Comprehensive settings with tabs:

```python
class SettingsDialog(QDialog):
    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config = config_manager
        self.setWindowTitle("Settings")
        self.setFixedSize(600, 500)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        header = QLabel("⚙️ Settings")
        header.setFont(QFont("Inter", 14, QFont.Bold))
        layout.addWidget(header)
        
        tabs = QTabWidget()
        tabs.setDocumentMode(True)
        
        # General tab
        general = QWidget()
        general_layout = QFormLayout(general)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(['dark', 'light', 'system'])
        self.theme_combo.setCurrentText(self.config.get_setting('theme', 'dark'))
        general_layout.addRow("Theme:", self.theme_combo)
        
        self.font_size = QSpinBox()
        self.font_size.setRange(10, 24)
        self.font_size.setValue(self.config.get_setting('font_size', 14))
        general_layout.addRow("Font Size:", self.font_size)
        
        self.auto_save = QCheckBox()
        self.auto_save.setChecked(self.config.get_setting('auto_save', True))
        general_layout.addRow("Auto Save:", self.auto_save)
        
        tabs.addTab(general, "General")
        
        # API tab
        api = QWidget()
        api_layout = QFormLayout(api)
        
        self.default_provider = QComboBox()
        self.default_provider.addItems(list(Config.PROVIDERS.keys()))
        self.default_provider.setCurrentText(self.config.get_setting('default_provider', 'openai'))
        api_layout.addRow("Default Provider:", self.default_provider)
        
        self.streaming = QCheckBox()
        self.streaming.setChecked(self.config.get_setting('streaming', True))
        api_layout.addRow("Enable Streaming:", self.streaming)
        
        self.max_tokens = QSpinBox()
        self.max_tokens.setRange(100, 100000)
        self.max_tokens.setValue(self.config.get_setting('max_tokens', 4096))
        api_layout.addRow("Max Tokens:", self.max_tokens)
        
        self.temperature = QDoubleSpinBox()
        self.temperature.setRange(0.0, 2.0)
        self.temperature.setSingleStep(0.1)
        self.temperature.setValue(self.config.get_setting('temperature', 0.7))
        api_layout.addRow("Temperature:", self.temperature)
        
        tabs.addTab(api, "API")
        
        # Server tab
        server = QWidget()
        server_layout = QFormLayout(server)
        
        self.server_port = QSpinBox()
        self.server_port.setRange(1024, 65535)
        self.server_port.setValue(self.config.get_setting('flask_port', 5000))
        server_layout.addRow("Server Port:", self.server_port)
        
        self.server_host = QLineEdit()
        self.server_host.setText(self.config.get_setting('flask_host', '0.0.0.0'))
        server_layout.addRow("Server Host:", self.server_host)
        
        tabs.addTab(server, "Server")
        
        layout.addWidget(tabs)
        
        # Buttons
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save Settings")
        save_btn.clicked.connect(self.save_settings)
        btn_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        layout.addLayout(btn_layout)
    
    def save_settings(self):
        self.config.set_setting('theme', self.theme_combo.currentText())
        self.config.set_setting('font_size', self.font_size.value())
        self.config.set_setting('auto_save', self.auto_save.isChecked())
        self.config.set_setting('default_provider', self.default_provider.currentText())
        self.config.set_setting('streaming', self.streaming.isChecked())
        self.config.set_setting('max_tokens', self.max_tokens.value())
        self.config.set_setting('temperature', self.temperature.value())
        self.config.set_setting('flask_port', self.server_port.value())
        self.config.set_setting('flask_host', self.server_host.text())
        QMessageBox.information(self, "Success", "Settings saved successfully!")
        self.accept()
```

## Model Recommendations by Task

```python
MODEL_RECOMMENDATIONS = {
    'code_generation': ['gpt-4o', 'claude-3-5-sonnet', 'gemini-pro'],
    'writing': ['gpt-4o', 'claude-3-opus', 'gemini-pro'],
    'analysis': ['gpt-4o', 'claude-3-5-sonnet', 'gemini-pro'],
    'creative': ['gpt-4o', 'claude-3-opus', 'gemini-pro'],
    'quick_task': ['gpt-3.5-turbo', 'claude-3-haiku', 'gemini-flash'],
    'vision': ['gpt-4o', 'claude-3-5-sonnet', 'gemini-pro-vision'],
}
```

## Pitfalls

1. **Key storage**: Never log API keys. Store in user home directory, not in project files.
2. **Provider validation**: Validate key format (prefix check) before saving.
3. **Model availability**: Models change frequently; cache with TTL rather than hardcoding.
4. **Chat history**: Limit history size to prevent memory issues in long sessions.
5. **Threading**: Run API calls in background threads to avoid blocking UI.
