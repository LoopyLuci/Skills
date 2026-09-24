# Desktop App Development - Session Reference

## PyQt5 Patterns

### Component Library Pattern

```python
COMPONENTS = {
    'hero': {
        'name': 'Hero Section',
        'icon': '🖼️',
        'category': 'Layout',
        'props': {
            'title': 'Welcome',
            'subtitle': 'Build something amazing',
            'ctaText': 'Get Started',
            'backgroundColor': '#1e293b'
        }
    },
    'features': {
        'name': 'Features Grid',
        'icon': '✨',
        'category': 'Content',
        'props': {
            'title': 'Features',
            'columns': 3
        }
    }
    # ... more components
}
```

### Template Library Pattern

```python
TEMPLATES = {
    'saas': {
        'name': 'SaaS Landing',
        'icon': '🚀',
        'sections': ['navbar', 'hero', 'features', 'pricing', 'cta', 'footer']
    }
}

def load_template(self, template_id):
    template = TEMPLATES[template_id]
    sections = []
    for i, section_type in enumerate(template['sections']):
        comp = COMPONENTS[section_type]
        section = {
            'id': f'section-{i}',
            'type': section_type,
            'props': json.loads(json.dumps(comp['props']))
        }
        sections.append(section)
    self.project['pages'][0]['sections'] = sections
    self.save_history()
    self.render_canvas()
    self.render_properties()
```

### Section Rendering

Each section type renders based on its props:

```python
def make_section_content(self, section):
    p = section['props']
    w = QFrame()
    
    if section['type'] == 'hero':
        w.setStyleSheet(f'background: {p["backgroundColor"]}; padding: 80px 40px;')
        l = QVBoxLayout(w)
        l.setAlignment(Qt.AlignCenter)
        t = QLabel(p['title'])
        t.setAlignment(Qt.AlignCenter)
        t.setStyleSheet('color: white; font-size: 32px; font-weight: bold;')
        l.addWidget(t)
        s = QLabel(p['subtitle'])
        s.setAlignment(Qt.AlignCenter)
        s.setStyleSheet('color: rgba(255,255,255,0.8); font-size: 18px; margin-top: 12px;')
        l.addWidget(s)
        b = QPushButton(p['ctaText'])
        b.setStyleSheet('background: white; color: #1e293b; padding: 12px 24px; border-radius: 8px; font-weight: 600; max-width: 200px;')
        l.addWidget(b, alignment=Qt.AlignCenter)
    
    return w
```

### Properties Panel

```python
def render_properties(self):
    for child in self.prop_content.children():
        if isinstance(child, QWidget):
            child.deleteLater()
    
    if not self.selected_section:
        empty = QLabel('Select a section to\nedit its properties')
        empty.setAlignment(Qt.AlignCenter)
        empty.setStyleSheet('color: #64748b; padding: 40px 0;')
        self.prop_layout.addWidget(empty)
        self.prop_layout.addStretch()
        return
    
    section = None
    for s in self.project['pages'][0]['sections']:
        if s['id'] == self.selected_section:
            section = s
            break
    
    if not section:
        return
    
    comp = COMPONENTS[section['type']]
    title = QLabel(f"{comp['icon']} {comp['name']}")
    title.setStyleSheet('color: #f8fafc; font-weight: 600; padding: 4px 0;')
    self.prop_layout.addWidget(title)
    
    for key, value in section['props'].items():
        group = QGroupBox()
        group.setStyleSheet('QGroupBox { border: 1px solid #334155; border-radius: 6px; margin-top: 8px; padding-top: 16px; }')
        gl = QVBoxLayout(group)
        
        label = QLabel(key.replace('_', ' ').title())
        label.setStyleSheet('color: #94a3b8; font-size: 10px; font-weight: 600;')
        gl.addWidget(label)
        
        if isinstance(value, int):
            spin = QSpinBox()
            spin.setRange(0, 100)
            spin.setValue(value)
            spin.setStyleSheet('background: #0f172a; color: #f8fafc; border: 1px solid #475569; padding: 4px;')
            spin.valueChanged.connect(lambda v, k=key: self.update_prop(k, v))
            gl.addWidget(spin)
        else:
            edit = QLineEdit(str(value))
            edit.setStyleSheet('background: #0f172a; color: #f8fafc; border: 1px solid #475569; padding: 6px; border-radius: 4px;')
            edit.textChanged.connect(lambda v, k=key: self.update_prop(k, v))
            gl.addWidget(edit)
        
        self.prop_layout.addWidget(group)
    
    self.prop_layout.addStretch()
```

### History System

```python
def save_history(self):
    self.history = self.history[:self.history_index + 1]
    self.history.append(json.dumps(self.project))
    self.history_index = len(self.history) - 1

def undo(self):
    if self.history_index > 0:
        self.history_index -= 1
        self.project = json.loads(self.history[self.history_index])
        self.selected_section = None
        self.render_canvas()
        self.render_properties()

def redo(self):
    if self.history_index < len(self.history) - 1:
        self.history_index += 1
        self.project = json.loads(self.history[self.history_index])
        self.selected_section = None
        self.render_canvas()
        self.render_properties()
```

## Electron Patterns

### Installation on Windows

```bash
npm config set ignore-scripts false
npm install electron
```

Or manual:
```bash
curl -L -o electron.zip "https://github.com/electron/electron/releases/download/v32.3.3/electron-v32.3.3-win32-x64.zip"
unzip electron.zip -d node_modules/electron/dist
```

### Preload Script

```javascript
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
    getSystemInfo: () => ipcRenderer.invoke('get-system-info'),
    showSaveDialog: () => ipcRenderer.invoke('show-save-dialog'),
    onMenuAction: (callback) => {
        ipcRenderer.on('menu:new-project', () => callback('new-project'));
    }
});
```

### Native Menu

```javascript
function createMenu() {
    const template = [
        {
            label: 'File',
            submenu: [
                { label: 'New', accelerator: 'CmdOrCtrl+N', click: () => win.webContents.send('menu:new-project') },
                { type: 'separator' },
                { role: 'quit' }
            ]
        }
    ];
    Menu.setApplicationMenu(Menu.buildFromTemplate(template));
}
```

## Common Pitfalls

1. **Stale state**: Always call `render_canvas()` and `render_properties()` after state changes. Qt widgets don't auto-update.

2. **Memory leaks**: Call `child.deleteLater()` before clearing layouts to prevent memory leaks.

3. **Lambda capture**: In loops creating lambdas, use `lambda checked, t=cid: func(t)` to capture current value.

4. **Widget parenting**: Always set parent widget or layout. Orphaned widgets leak memory.

5. **JSON serialization**: Use `json.loads(json.dumps(obj))` for deep copies of nested objects.

6. **Electron install**: Windows npm may block postinstall scripts. Use `npm config set ignore-scripts false`.

7. **Theme consistency**: Use CSS variables via `setStyleSheet` consistently across all widgets.
