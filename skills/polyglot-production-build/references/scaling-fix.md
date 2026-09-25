# Scaling Fix Pattern — setFixedWidth → setSizePolicy

## Problem

`setFixedWidth(N)` on input widgets (`TextInput`, `QSpinBox`, `QComboBox`) prevents responsive layouts; the layout manager's `addStretch()` is ignored because the fixed-width widget claims a fixed size regardless of available space.

## Verified artifacts

- Before fix: 32 `setFixedWidth` references across 7 `gui/*.py` files (`audit_log.py`, `panels_chat.py`, `panels_logs.py`, `panels_pairing.py`, `panels_security.py`, `panels_vm_control.py`, `widgets.py`, plus `panels_settings.py`).
- After fix: 0 `setFixedWidth` references (verified: `grep -rn "setFixedWidth" /c/Projects/QEMU-MCP/gui/*.py` = 0).
- Pattern applied: `setFixedWidth(W)` → `setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)` for input widgets; `setFixedWidth(W)` → `setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)` for label widgets (`_label` variables).
- Verification: full test suite passes after fix: `pytest tests/test_gui.py` = 39/39 passed (before fix: 39 passed + 1 teardown error from `closeEvent`).

## Pattern (verified in `gui/panels_settings.py` + other files)

Labels (`_label` variables, `QLabel`):
```
bin_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
```

Input widgets (`TextInput`, `QSpinBox`, `QComboBox`, `QDoubleSpinBox`):
```
self.qemu_args_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
self.ram_spin.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
self.display_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
```

Window chrome (`close_btn`, `min_btn`, `max_btn`, `refresh_btn`) uses `setFixedHeight` (not `setFixedWidth`) for consistent button appearance; these are UI chrome, not responsive content.

## Pitfalls

- `setSizePolicy(Expanding, Fixed)` allows the widget to expand horizontally; `addStretch()` on the row layout provides the extra space. Without `addStretch()`, the widget won't expand.
- `setSizePolicy(Preferred, Fixed)` on labels allows the label to grow to its content width but prevents it from shrinking below the preferred width (content width). The `addStretch()` handles the rest.
- `setFixedWidth` on `QCheckBox` (`self.gl_check`) is intentionally kept as `setFixedHeight` (button chrome) — buttons have consistent dimensions; only text fields and combo boxes need expanding policy.
- Never use `setFixedWidth` on `QLineEdit`, `TextInput`, `QSpinBox`, `QComboBox`, or `QDoubleSpinBox`; always use `setSizePolicy(Expanding, Fixed)`.
- Scaling fixes must be verified with the full test suite (`pytest tests/test_gui.py`) before declaring complete; a partial fix (only first 1-2 inputs) doesn't verify that the layout handles all expanded inputs correctly.
