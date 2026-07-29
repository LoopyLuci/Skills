# PowerShell Tool Authoring — Reference Transcripts

## Error 1: `#Requires -RunAsAdministrator` → silent exit

Observed: Double-click/batch launches script → window flashes and vanishes.
Root cause: `#Requires -RunAsAdministrator` at top of script. PowerShell immediately
exits with no visible message when not running as admin.

Fix: Remove `#Requires -RunAsAdministrator`. Handle non-admin gracefully with
choice prompt ([A]uto-elevate / [C]ontinue / [N]o exit).

## Error 2: UTF-8 without BOM → parse errors on PS5

Observed: Right-click → Run with PowerShell 5.1 → "Unexpected token '}'" errors
on lines containing box-drawing characters, em-dashes, or Unicode symbols.
Same script works fine on PowerShell 7.

Root cause: PS5 assumes ANSI encoding without BOM. Multi-byte UTF-8 sequences
get decoded as individual ANSI bytes → parser sees garbage tokens.

Fix: Save .ps1 with UTF-8 BOM (`encoding='utf-8-sig'` in Python).
Also replace all non-ASCII Unicode with ASCII equivalents as belt-and-suspenders.

```python
# Python: save with BOM
with open('script.ps1', 'w', encoding='utf-8-sig') as f:
    f.write(content)
```

## Error 3: `$var:` in strings → PS7 parse error

Observed: `Write-Host "  FAIL $svc: $_"` → PS7 parser error:
"Variable reference is not valid. ':' was not followed by a valid variable
name character. Consider using ${} to delimit the name."

Root cause: PS7 is stricter about `$varname:` in strings. It attempts to
resolve `$var:` as a namespace-scope reference (like `$env:PATH`).
Even a space after the colon doesn't help in PS7.

Fix: Use format operator: `Write-Host ("  FAIL {0}: {1}" -f $svc, $_)`

## Error 4: Start-Process -ArgumentList array → UAC child fails

Observed: `Invoke-Elevated` tries to launch elevated PowerShell with array-based
ArgumentList. Result: Error "Cannot process argument transformation on parameter
'Data'..." and string shows with wrong quoting like:
`"D:\path\script.ps1\ -AdminAction EnvSanitizer-Machine"`
(path and -AdminAction concatenated into one string).

Root cause: `Start-Process -Verb RunAs` with array-based `-ArgumentList` mangles
the quoting of embedded quotes. The array elements get joined with spaces but
the embedded quote characters (`"`) are not properly escaped for the command line.

Fix: Use flat string:
```powershell
$argString = '-NoProfile -ExecutionPolicy Bypass -File "' + $scriptPath + '" -AdminAction ' + $Action
Start-Process -FilePath $psExe -Verb RunAs -ArgumentList $argString -PassThru -Wait
```

Also apply this fix to the startup auto-elevation:
```powershell
Start-Process -FilePath $psExe -Verb RunAs `
    -ArgumentList ('-NoProfile -ExecutionPolicy Bypass -File "' + $myPath + '"')
```

## Error 5: New-RestorePoint return value → leaked path to console

Observed: After calling `New-RestorePoint -Label "Environment Sanitizer"`,
the full restore point path appears on console.

Root cause: The function does `return $rpDir` at the end. PowerShell emits
uncaptured return values from function calls to the output stream, even when
called as a statement (not assigned to a variable).

Fix: Always capture with `$null = New-RestorePoint ...`

## Error 6: Docker Desktop installer reports "Existing installation is up to date"

Observed: After running full Docker uninstall that deleted files, directories,
registry keys, and WSL2 distros, the Docker Desktop installer still says
"Existing installation is up to date" and refuses to install fresh.

Root cause: The Docker Desktop installer checks
`HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Docker Desktop`
to determine if Docker is already installed. This uninstall registration key
persists even after all Docker files are deleted. The Windows Installer (MSI)
database still has the product registered.

Fix: Remove these additional registry paths:
```powershell
# These are what the installer checks:
'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Docker Desktop'
'HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Docker Desktop'
'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\Docker Desktop.exe'
```

Also kill any running Docker Desktop Installer processes and clean MSI files
from the installer cache:
```powershell
Get-Process -Name "*Docker Desktop Installer*" -ErrorAction SilentlyContinue |
    Stop-Process -Force -ErrorAction SilentlyContinue

$installerCache = "$env:SystemRoot\Installer"
if (Test-Path $installerCache) {
    Get-ChildItem $installerCache -Filter "*.msi" -Recurse -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -match '(?i)docker' } |
        ForEach-Object { Remove-Item $_.FullName -Force -ErrorAction SilentlyContinue }
}
```

After these steps, the Docker Desktop installer will see zero traces and offer
a clean installation.

## Pattern: Auto-Elevation Architecture

Three-component system:

1. **`param([string]$AdminAction = '')`** — at script top, allows child invocation
2. **`Invoke-Elevated`** — non-admin caller function:
   - If already admin → run `Invoke-AdminAction -Action $Action` directly
   - If not admin → `Start-Process -Verb RunAs` with flat-string argument
3. **`Invoke-AdminAction`** — the admin work, called from elevated context:
   - Switch on `$Action`: 'EnvSanitizer-Machine', 'Registry-Cleanup', 'Services-Stop'

Entry point checks `if ($AdminAction)` first → runs action, shows results, exits.
Otherwise shows interactive menu.

## Pattern: Can't Edit User-Owned Skills

When `skill_manage(action='patch', ...)` returns:
"Refusing background curator patch for skill 'X': the skill is not curator-managed
(created_by=None). User-owned skills are off-limits to autonomous curation."

Skills created via `write_file` directly to the skills directory are user-owned.
Skills created via `skill_manage(action='create', ...)` by the system are
curator-managed and can be patched.

To make a user-owned skill editable by background curators, run:
```
hermes curator adopt <name>
```
