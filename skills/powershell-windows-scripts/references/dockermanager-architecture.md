# DockerManager Architecture Reference

A production-grade interactive PowerShell script (1800 lines, 100 KB) for
Docker management and removal on Windows.

## Two Versions

| File | Lines | Size | Features |
|---|---|---|---|
| DockerManager.ps1 | 1,313 | 70 KB | Core management + cleanup |
| DockerManager-Ultra.ps1 | 1,800 | 100 KB | Restore points, env sanitizer, smart analysis |

## Key Architecture Decisions

### Data Directories (auto-created)

```
%LOCALAPPDATA%\DockerManager-Ultra\
Logs/          # Plain text + JSONL structured logs
Backups/       # Auto-backups before destructive ops
Reports/       # Generated system reports
RestorePoints/ # Snapshots for rollback (max 5 retained)
Plans/         # Exported cleanup plans as JSON
config.json    # Persistent user preferences
state.json     # Runtime state cache
```

### Function Organization (16 groups)

1. Configuration - paths, colors, version constants
2. Core Utility - logging, admin check, file init
3. UI Framework - banner, menus, tables, progress bars, colored output
4. Docker Detection - installation scanning across disk and PATH
5. File System Scanning - parallel (ThreadJob) or sequential; cached hourly; categorized
6. Docker Engine Operations - containers, images, volumes, networks, disk usage
7. WSL2 Management - list, start, stop, export, import, unregister
8. Cleanup and Removal - plan generation, execution, 7-phase full removal
9. Restore Point Engine - snapshot of files/registry/WSL2/services/env; rollback restores all
10. Environment Sanitizer - removes Docker from User/System PATH + DOCKER_* vars
11. Windows Feature Manager - containers, VirtualMachinePlatform toggle
12. Export/Import Plans - JSON serialization of cleanup plans
13. Report Generation - comprehensive system reports (TXT)
14. Interactive Screens - menu callbacks for each feature
15. Main Menu - event loop with 16 options + navigation

### Unique Ultra Features

- Smart Analysis: classifies files into SafeToDelete, NeedsBackup, LockedFiles, LargeFiles
- Restore Points: file hashes, registry exports (.reg), WSL2 .tar backups, service state, env vars
- Health Dashboard: live multi-pane view of engine, objects, WSL2, registry, services, env
- Scan Caching: hourly cache avoids repeated full scans
- Config Persistence: user prefs saved to JSON (DryRunByDefault, AutoBackup, etc.)
- Parallel Scanning: ThreadJob runspaces for multi-core file scans

### Pitfalls Encountered During Development

1. #Requires -RunAsAdministrator: silent exit on non-admin; replaced with runtime check
2. UTF-8 without BOM: PS 5.1 corrupts Unicode chars; fixed by saving with utf-8-sig BOM
3. $var: in string interpolation: parse error on colon; use ${var}: syntax
4. "$var: $_" in catch blocks: same colon-scope parse error; use -f format operator
5. Batch file without -NoExit: window closes immediately on error; always add -NoExit
6. Read-Host in non-interactive context: script hangs; wrap in try/catch with default
