# Property Inspector Pattern for PyQt5

## Problem
Sections have different property schemas. A static editor can't handle dynamic types.

## Solution
Build a `PropertyInspector` QWidget that generates editors based on property value types.

## Implementation

```python
class PropertyInspector(QWidget):
    property_changed = pyqtSignal()

    def set_section(self, section):
        self.section = section
        self._clear_properties()
        if not section:
            self.hide()
            return
        self._build_properties()

    def _build_properties(self):
        for key, value in self.section.props.items():
            if isinstance(value, bool):
                self._add_bool_editor(key, value)
            elif isinstance(value, int):
                self._add_int_editor(key, value)
            elif isinstance(value, float):
                self._add_float_editor(key, value)
            elif isinstance(value, str):
                if key in ('color', 'backgroundColor', 'textColor'):
                    self._add_color_editor(key, value)
                elif len(value) > 50:
                    self._add_text_editor(key, value)
                else:
                    self._add_string_editor(key, value)
            elif isinstance(value, list):
                self._add_list_editor(key, value)
            elif isinstance(value, dict):
                self._add_dict_editor(key, value)
```

## Color Picker Editor

```python
def _add_color_editor(self, key, value):
    row = QHBoxLayout()
    color_preview = QFrame()
    color_preview.setFixedSize(32, 32)
    color_preview.setStyleSheet(f'background: {value}; border-radius: 6px;')
    row.addWidget(color_preview)

    color_input = QLineEdit(value)
    row.addWidget(color_input)

    pick_btn = QPushButton('🎨')
    pick_btn.clicked.connect(lambda: self._pick_color(key, color_preview, color_input))
    row.addWidget(pick_btn)

    self.props_layout.addRow(f'{key}:', container)

def _pick_color(self, key, preview, input_field):
    color = QColorDialog.getColor(QColor(input_field.text()), self, 'Choose Color')
    if color.isValid():
        hex_color = color.name()
        input_field.setText(hex_color)
        preview.setStyleSheet(f'background: {hex_color}; border-radius: 6px;')
        self._on_property_changed(key, hex_color)
```

## List Editor with Add/Remove

```python
def _add_list_editor(self, key, value):
    list_widget = QListWidget()
    for item in value:
        list_widget.addItem(str(item))

    btn_row = QHBoxLayout()
    add_btn = QPushButton('+')
    add_btn.clicked.connect(lambda: self._add_list_item(list_widget))
    remove_btn = QPushButton('-')
    remove_btn.clicked.connect(lambda: self._remove_list_item(list_widget))
    btn_row.addWidget(add_btn)
    btn_row.addWidget(remove_btn)

    container = QWidget()
    layout = QVBoxLayout(container)
    layout.addWidget(list_widget)
    layout.addLayout(btn_row)
    self.props_layout.addRow(f'{key}:', container)
```

## Key Patterns

1. **Type-based dispatch** — Use `isinstance()` to choose the right editor
2. **Color preview** — QFrame with background style that updates on change
3. **List editing** — QListWidget with add/remove buttons, sync back to property on change
4. **Signal emission** — `property_changed` signal triggers live preview update
5. **Layout clearing** — Always `takeAt()` + `deleteLater()` when rebuilding
