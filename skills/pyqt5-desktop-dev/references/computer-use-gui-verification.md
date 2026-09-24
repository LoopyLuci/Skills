# Computer-Use MCP GUI Verification Workflow

## Overview
Verify PyQt5 GUI rendering through MCP `computer_use` tool — capture screenshots, click elements, verify state changes.

## Workflow

### 1. Launch App as Background Process
```bash
cd "/c/Users/Server/Desktop/WebBuilder" && python desktop_app.py 2>&1
```

### 2. Wait for Window to Appear
```bash
sleep 5 && ps -p <PID> -o pid,cmd 2>/dev/null || echo "not found"
```

### 3. Capture via MCP
```
computer_use(action="capture", app="Python 3.13 (64-bit)", mode="vision")
```

**Note:** On Windows, the app name is the Python executable name, not the script name. Use `list_apps` to discover available app names.

### 4. Verify GUI Elements
The vision analysis returns a structured description of visible elements:
- Menu bar items
- Toolbar buttons
- Tab bar state
- Sidebar content
- Canvas area
- Status bar

### 5. Interact with Elements
```
# Click by coordinate (native desktop coordinates, not screenshot pixels)
computer_use(action="click", coordinate=[x, y])

# Re-capture to verify state change
computer_use(action="capture", app="Python 3.13 (64-bit)", mode="vision")
```

### 6. Test Tab Switching
Click Style tab → verify theme list appears → click Apply Theme → verify preview updates.

## Key Findings

| Element | Native Coord | Notes |
|---------|-------------|-------|
| Editor tab | ~[54, 129] | First tab |
| Style tab | ~[166, 129] | Second tab |
| Preview tab | ~[276, 130] | Third tab |
| Generate button | ~[580, 832] | Bottom action bar |
| Add Section button | ~[710, 831] | Bottom action bar |

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `no on-screen window matched app='WebBuilder'` | App name is Python exe, not script | Use `app="Python 3.13 (64-bit)"` |
| `0 interactable element(s)` | Window not ready or wrong app | Wait longer, check `list_apps` |
| `Invalid window handle` | Window closed or PID changed | Re-launch app, re-capture |
| `effect: unverifiable` | Click delivered but not confirmed | Re-capture to verify state change |

## Qt + MCP Clicking Limitation (IMPORTANT)

**Background clicks via `computer_use` do NOT reliably reach Qt widgets.**

This is a fundamental limitation: Qt's event loop doesn't process synthetic background input the way native Windows apps do. You will see:
- `effect: unverifiable` on clicks
- Clicks landing on the wrong element or no element
- `Invalid window handle` errors after a few attempts

**Workaround:** Verify GUI *logic* via integration tests (Python-level testing of generate/add/export workflows), not through MCP clicking. Use MCP `capture` for *visual verification only* — confirming the GUI renders correctly.

## Launching PyQt5 Apps on Windows

Use `pythonw.exe` to avoid the console window:
```bash
pythonw desktop_app.py 2>&1
```

**Note:** `pythonw.exe` processes appear under `pythonw.exe` in `list_apps`, not `python.exe`. Use `app="pythonw.exe"` for capture.

## Process Cleanup

Multiple test launches create zombie Python processes that clutter `list_apps`. Kill stale instances between test runs:
```bash
pkill -9 -f "python.*desktop_app" 2>/dev/null
```

## Verification Checklist

1. ✅ App launches without errors
2. ✅ Window title visible: "WebBuilder Desktop — Professional Web Builder"
3. ✅ Menu bar: File, Edit, Build, Tools, Help
4. ✅ Toolbar: Generate, Preview, +Sections, Export, Settings
5. ✅ Tabs: Editor, Style, Preview
6. ✅ Sidebar: 16 section components with icons
7. ✅ Canvas: White rounded rectangle on dark background
8. ✅ Bottom bar: "Ready to build?" + Generate Project + Add Section
9. ✅ Tab switching works (Style tab shows theme presets)
10. ✅ Theme Apply button functional
11. ✅ Integration tests pass (15/15) — verifies GUI logic since MCP clicks are unreliable on Qt
