# GitHub Release & Distribution — Reference

## Release Process

1. Verify all tests pass: `python -m pytest tests/unit/ -x -q`
2. Verify exe launches cleanly: `dist/WebBuilder.exe` — check logs/crashes/ for errors
3. Update version in SKILL.md if needed
4. Create LICENSE file (MIT)
5. Commit changes with release notes
6. Create annotated tag: `git tag -a v1.X -m "WebBuilder vX.X - ..."`
7. Push tag: `git push origin v1.X`
8. Create GitHub Release from the tag

## GitHub Release Notes Template

```markdown
## WebBuilder vX.X

### Features
- List key features

### Fixes
- List bug fixes

### Technical
- Test count, crash stages, components

### License
MIT
```

## License

MIT License — FOSS compliant, suitable for GitHub and F-Droid (if Android).

## F-Droid Note

WebBuilder is a **desktop PyQt5 application**, not an Android app. F-Droid only distributes Android apps. Desktop distribution is via GitHub Releases.

F-Droid does NOT apply to PyQt5 desktop apps. Do not attempt F-Droid distribution for desktop applications.

## Pitfalls

1. **PyInstaller caches old .py files** — kill ALL processes and rebuild clean after any change
2. **Tags must be annotated** — `git tag -a v1.X` not `git tag v1.X` for release tags
3. **LICENSE required** — GitHub won't show license info without a LICENSE file
4. **Desktop app ≠ Android** — F-Droid doesn't apply to PyQt5 desktop apps
5. **Installer/Updater** — `webbuilder/installer/__init__.py` provides Installer class with Inno/NSIS/ZIP creation, GitHub update checking, auto-update with rollback, progress tracking. Singleton: `get_installer()`. `webbuilder/update/__init__.py` provides UpdateManager with GitHub releases API, version comparison, download/install/rollback. Singleton: `get_update_manager()`.
6. **Qt platform for GUI visibility** — `os.environ['QT_QPA_PLATFORM'] = 'windows'` MUST be set BEFORE any PyQt import. Without this, Qt defaults to offscreen/minimal platform and GUI is invisible on Windows.
7. **SQLite timeout on Windows** — Always use `timeout=30, check_same_thread=False` in `sqlite3.connect()` to avoid PermissionError when multiple processes access the same DB file.
8. **TTL=0 cache bug** — `ttl or default` treats 0 as falsy and uses default. Use `ttl if ttl is not None else default` instead.
9. **Event ID uniqueness** — Analytics events need UUID suffix in IDs to avoid UNIQUE constraint failures when multiple events are tracked in the same second.
