# PowerShell Encoding Pitfalls

## The Core Problem

Windows PowerShell 5.1 (powershell.exe) defaults to the system's ANSI code page
when reading `.ps1` files without a BOM. PowerShell Core 7+ (pwsh.exe) defaults
to UTF-8 regardless of BOM.

This means: a `.ps1` containing multi-byte characters (em-dash `—` U+2014,
checkmark `✓` U+2713, box-drawing `┌┐└┘`, or any emoji) will corrupt when
PS 5.1 reads a BOM-less UTF-8 file.

## Solutions

### Option A: UTF-8 BOM (recommended)

Add the UTF-8 BOM (0xEF 0xBB 0xBF) to the file. This forces PS 5.1 to
interpret the file as UTF-8.

```python
# Python
with open('script.ps1', 'w', encoding='utf-8-sig') as f:
    f.write(content)
```

```powershell
# PowerShell (from within PowerShell)
$content | Out-File 'script.ps1' -Encoding UTF8
# Out-File -Encoding UTF8 adds BOM automatically in PS 5.1
```

### Option B: Strip non-ASCII characters

Replace Unicode glyphs with ASCII equivalents before they reach the file:

| Unicode | Replace With |
|---------|-------------|
| `—` (em-dash) | `--` |
| `✓` (checkmark) | `OK` |
| `✗` (cross) | `FAIL` |
| `→` (arrow) | `->` |
| `•` (bullet) | `*` |
| Emoji | Descriptive text in brackets: `[BOX]`, `[OK]`, etc. |
| Box-drawing (┌┐└┘│) | Basic ASCII: `+|+-` |

## Character-Specific Issues

### Em-dash in PowerShell 5.1

```powershell
# Raw UTF-8 bytes: 0xE2 0x80 0x94
# When read as Windows-1252: â€" (3 garbage chars)
$x = "File detected — backup required"  # WRONG in PS 5.1 without BOM
$x = "File detected -- backup required"  # OK everywhere
```

### Emoji and Box-Drawing

```powershell
# These work in PS Core 7+, corrupt in PS 5.1 without BOM:
Write-Host "  ┌─────────────────────┐"  # box drawing chars
Write-Host "  ✓ Task complete"           # checkmark
Write-Host "  📦 Container Info"         # emoji

# ASCII-safe alternatives:
Write-Host "+-----------------------+"    # ASCII box
Write-Host "  OK Task complete"           # text check
Write-Host "[PACKAGE] Container Info"     # text emoji
```

## Diagnostic

To detect encoding corruption at runtime:

```powershell
function Test-FileEncoding {
    param([string]$Path)
    $bytes = [System.IO.File]::ReadAllBytes($Path)
    $hasBOM = $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF
    $hasNonASCII = $bytes | Where-Object { $_ -gt 127 } | Select-Object -First 1
    return @{ HasBOM = $hasBOM; HasNonASCII = $null -ne $hasNonASCII }
}
```

## Common Errors When Encoding Is Wrong

| Error Message | Likely Cause |
|---|---|
| "Unexpected token 'backup' in expression or statement" | Em-dash in string literal corrupts parser |
| "Variable reference is not valid" | Corrupted `$_` or `$()` from encoding issues |
| "The string is missing the terminator" | Quote character mangled by wrong encoding |
| "Expressions are only allowed as the first element" | Multiple lines collapsed by encoding corruption |
| Characters displaying as `�` or `?` | Save-as without BOM |
