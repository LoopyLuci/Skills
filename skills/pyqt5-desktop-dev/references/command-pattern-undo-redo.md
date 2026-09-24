# Command Pattern for Undo/Redo in PyQt5

## Problem
JSON-snapshot undo (appending full project state) is memory-heavy and doesn't support descriptive undo messages or granular property edits.

## Solution
Implement the Command pattern with `execute()` and `undo()` methods.

## Implementation

```python
class Command:
    def execute(self) -> None: raise NotImplementedError
    def undo(self) -> None: raise NotImplementedError
    @property
    def description(self) -> str: return "Command"

class AddSectionCommand(Command):
    def __init__(self, canvas, section, index=-1):
        self.canvas = canvas
        self.section = section
        self.index = index

    def execute(self):
        if self.index < 0:
            self.canvas._sections.append(self.section)
        else:
            self.canvas._sections.insert(self.index, self.section)
        self.canvas._refresh()

    def undo(self):
        if self.section in self.canvas._sections:
            self.canvas._sections.remove(self.section)
            self.canvas._refresh()

    @property
    def description(self):
        return f"Add {self.section.type}"

class RemoveSectionCommand(Command):
    def __init__(self, canvas, section):
        self.canvas = canvas
        self.section = section
        self.index = canvas._sections.index(section) if section in canvas._sections else -1

    def execute(self):
        if self.section in self.canvas._sections:
            self.canvas._sections.remove(self.section)
            self.canvas._refresh()

    def undo(self):
        if self.index >= 0:
            self.canvas._sections.insert(self.index, self.section)
            self.canvas._refresh()

class MoveSectionCommand(Command):
    def __init__(self, canvas, section, direction):
        self.canvas = canvas
        self.section = section
        self.direction = direction  # -1 up, +1 down
        self.old_index = canvas._sections.index(section)
        self.new_index = max(0, min(len(canvas._sections) - 1, self.old_index + direction))

    def execute(self):
        self.canvas._sections.pop(self.old_index)
        self.canvas._sections.insert(self.new_index, self.section)
        self.canvas._refresh()

    def undo(self):
        self.canvas._sections.pop(self.new_index)
        self.canvas._sections.insert(self.old_index, self.section)
        self.canvas._refresh()

class EditPropertyCommand(Command):
    def __init__(self, section, key, old_value, new_value):
        self.section = section
        self.key = key
        self.old_value = old_value
        self.new_value = new_value

    def execute(self):
        self.section.props[self.key] = self.new_value

    def undo(self):
        self.section.props[self.key] = self.old_value

class CommandHistory:
    def __init__(self, max_history=100):
        self.undo_stack = []
        self.redo_stack = []
        self.max_history = max_history

    def execute(self, command):
        command.execute()
        self.undo_stack.append(command)
        self.redo_stack.clear()
        if len(self.undo_stack) > self.max_history:
            self.undo_stack.pop(0)

    def undo(self):
        if not self.undo_stack: return None
        cmd = self.undo_stack.pop()
        cmd.undo()
        self.redo_stack.append(cmd)
        return cmd.description

    def redo(self):
        if not self.redo_stack: return None
        cmd = self.redo_stack.pop()
        cmd.execute()
        self.undo_stack.append(cmd)
        return cmd.description
```

## Usage in Canvas

```python
class Canvas(QWidget):
    def __init__(self):
        self._sections = []
        self.command_history = CommandHistory()

    def add_section(self, section):
        cmd = AddSectionCommand(self, section)
        self.command_history.execute(cmd)

    def undo(self):
        desc = self.command_history.undo()
        if desc:
            self.project_status.setText(f"  ↩ {desc}")
```

## Benefits
- Descriptive undo messages ("Add Hero", "Move Footer Up")
- Memory-efficient (only stores commands, not full state)
- Supports granular property edits
- Easy to extend with new command types
