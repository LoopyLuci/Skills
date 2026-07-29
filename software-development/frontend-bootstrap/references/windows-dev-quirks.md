# Windows / MSYS2 Dev Environment Quirks

Error transcripts and fixes encountered when building a React+Vite+TypeScript
app on Windows 10/11 from within MSYS2 bash (git-bash).

## Path Translation Failure Modes

### 1. Python can't open script

```
$ python3 /d/Projects/Streaming/scripts/sov status
C:\Users\limpi\AppData\Local\Microsoft\WindowsApps\python3.exe:
  can't open file 'D:\d\Projects\Streaming\scripts\sov':
  [Errno 2] No such file or directory
```

**Why**: MSYS2 translates `/d/Projects/...` to `D:\Projects\...` only when
the receiver is a bash-aware binary. Python is a native Windows binary, so
bash still translates it, but Python ALSO gets the translated path as a raw
string: `D:\d\Projects\...` (double-translated).

**Fix**: Use `D:/forward/slash/paths` (Python accepts forward slashes on
Windows, and MSYS2 doesn't double-translate them).

### 2. npm install hangs

```
$ npm install
[npm hangs indefinitely]
```

**Why**: Windows + corporate/gateway networks can block the npm registry.
The `npm install` process hangs on network calls with no timeout output.

**Fix**:
```bash
# Kill hung npm
Ctrl+C, then:
pkill -f "npm install"  # or taskkill via Task Manager

# Set mirror
npm config set registry https://registry.npmmirror.com
# or directly:
npm install --prefer-offline --no-audit
```

### 3. Vite port collision

```
Port 3001 is in use, trying another one...
Port 3002 is in use, trying another one...
```

**Why**: Previous Vite instances weren't cleaned up, or other services occupy
those ports.

**Fix**: Read the Vite log to find the actual port. Always check the log
before assuming a specific port. Log shows:
```
  Local:   http://localhost:3006/
```

### 4. curl localhost resolution

On MSYS2, `curl http://localhost:NNNN/` can fail with:
```
curl: (6) Could not resolve host: localhost
```

**Fix**: Use `http://127.0.0.1:NNNN/` explicitly.

## TypeScript Compilation Notes

### TS2307: Cannot find module

When `tsc --noEmit` reports `Cannot find module '@/path'`, the issue is
ALWAYS that `tsconfig.json` lacks the path mapping that `vite.config.ts`
has. Both files need it.

### TS1117: Duplicate in object literal

When a Zustand store merges multiple interfaces that share property names.
The fix is to write the shared property once in the initial state.

### TS2613: No default export

`import cn from '...'` when the module only has `export function cn`.
Fix: `import { cn } from '...'`.

## Quick Diagnostic Commands

```bash
# Check Python's actual working directory
python3 -c "import os; print(os.path.abspath('.'))"

# Check which Python is being used
which python3 && python3 --version

# Clear npm cache if installs are corrupted
npm cache clean --force

# List all ports used by node processes
netstat -tlnp 2>/dev/null | grep node
# Or on Windows:
netstat -ano | findstr :3001
