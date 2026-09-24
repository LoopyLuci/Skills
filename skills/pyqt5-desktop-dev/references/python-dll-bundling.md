# Python DLL Bundling for PyInstaller on Windows

## python311.dll Must Be Explicitly Bundled

**Symptom:** Frozen EXE fails to launch with a Windows error dialog:

```
Failed to load Python DLL
'C:\Projects\<project>\dist_internal\python311.dll'
LoadLibrary: The specified module could not be found.
```

**Root cause:** PyInstaller's `--onefile` bootloader on Windows needs `python311.dll` to run the embedded Python runtime. When the build uses a venv Python (e.g. Hermes's venv at `C:\Users\Server\AppData\Local\hermes\hermes-agent\venv\`), PyInstaller may not auto-detect and bundle the DLL, unlike a system Python install where it is found automatically.

**Fix — two steps:**

### Step 1: Ensure python311.dll is present in the venv

The Hermes venv may not include `python311.dll` by default. Copy it from the system Python install:

```bash
cp "/c/Users/Server/AppData/Local/Programs/Python/Python311/python311.dll" \
   "/c/Users/Server/AppData/Local/hermes/hermes-agent/venv/python311.dll"
```

Verify it is present:
```bash
ls -lh "$VIRTUAL_ENV/python311.dll"
```

### Step 2: Pass it to PyInstaller via `binaries=` in the spec

In the build script's `Analysis` call, add the DLL to the `binaries` list:

```python
from pathlib import Path

# Locate python311.dll
dll_path = Path(sys.prefix) / "python311.dll"
if not dll_path.exists():
    # Fallback: system Python install
    dll_path = Path("/c/Users/Server/AppData/Local/Programs/Python/Python311/python311.dll")

binaries = [(dll_path, "python311.dll")] if dll_path.exists() else []

a = Analysis(
    ...
    binaries=binaries,   # <-- pass here
    datas=...,
    hiddenimports=...,
    ...
)
```

**Mechanism:** PyInstaller's `--onefile` bootloader extracts bundled binaries to a temporary `_MEIxxxxx` directory at runtime and adds that directory to the DLL search path. Without `python311.dll` in `binaries`, the bootloader cannot find the Python runtime and the EXE fails to start.

### Step 3: Clean rebuild with `--clean`

After adding the DLL to `binaries`, rebuild with the `--clean` flag to remove cached build artifacts:

```bash
python scripts/build_pyinstaller.py --clean
```

**Why `--clean` matters:** PyInstaller caches collected binaries and module graphs between builds. Without `--clean`, the old spec (without the DLL) may be reused, and the new EXE still lacks the DLL.

### Verification

After rebuild, launch the EXE from the `dist/` directory:

```bash
cd /c/Projects/<project>
python -c "
import subprocess, time
proc = subprocess.Popen(['dist/<app>.exe'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
time.sleep(3)
if proc.poll() is None:
    print('EXE RUNNING — PID:', proc.pid)
else:
    print('FAILED RC:', proc.returncode)
"
```

**Expected:** EXE stays alive (poll returns None). If it still fails, check that:
1. `python311.dll` exists in the venv
2. The build script passes it via `binaries=`
3. The rebuild used `--clean`
4. The EXE was rebuilt (check timestamps: `ls -la dist/<app>.exe`)

## Related

- [Headless/offscreen mode](headless-testing.md) — for testing without a display
- [Distribution checklist](distribution-packaging.md) — full packaging workflow
