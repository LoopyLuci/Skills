# Polyglot Integration Checklist

Run in order; all must pass before declaring complete:

1. `.venv` Python: `PyQt5` (5.15.11+), `matplotlib` (3.11.2+), `numpy` (2.4.3+)
2. `.pyd` build: `cargo build --release` exit 0; `.pyd` size > 150KB
3. `.pyd` import (direct): `importlib.util.spec_from_file_location`; `.start()` → `"started"`; `.state()` → `"running"`
4. `.proto` count: `search_files` (`target='files'`, `pattern='*.proto'`) = 5
5. Frozen EXE: `.pyd` present (`_internal/`); rebuilt timestamp newer; `.exe` newer than `main_window.py`
6. Frozen loader: document exit 127 as loader issue (not `.pyd` error); verify `.pyd` independently
7. Web bridge: frozen `main_window.py` `WebBridgeEngine` count = 2
8. Graceful fallback: `gui/widgets.py` `_matplotlib_available` count = 5; frozen build embeds 2
9. E2E script: `scripts/e2e_polylot_test.sh` executable; verifies 8 layers
10. Production docs: `docs/BUILD_PLAN.md` (6 phases, 7 durability pillars)
