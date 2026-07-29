---
name: windows-path-formats
description: "MSYS vs Windows paths for curl git Python and tools"
---

# Windows Path Formats (MSYS/git-bash)

When running in MSYS/git-bash on Windows, three path formats exist. Using the wrong one breaks tools.

## The Three Formats

| Format | Example | Works In |
|--------|---------|----------|
| MSYS/Unix | `/c/Users/Name/file.txt` | Bash, Python, git, ls, find |
| Windows | `C:\Users\Name\file.txt` | CMD, PowerShell, Windows apps |
| Windows quoted | `"C:\Users\Name\file.txt"` | curl -o, some CLI tools |

## Tool Compatibility

| Tool | Path Format to Use |
|------|-------------------|
| `ls`, `cd`, `cp`, `find` | MSYS: `/c/Users/...` |
| `python file.py` | MSYS: `/c/Users/...` |
| `curl -o` | Windows quoted: `"C:\Users\...\file.zip"` |
| `JAVA_HOME` | Windows double-backslash: `C:\\Users\\...` |
| `ANDROID_SDK_ROOT` | Windows double-backslash: `C:\\Users\\...` |
| `local.properties` | Forward slash: `C:/Users/...` |
| `MEDIA:` protocol | MSYS: `/c/Users/...` |
| Gradle/Java | Windows backslash: `C:\Users\...` |

## Quick Reference

```bash
# These work:
ls /c/Users/dubem/file.txt
cp /c/Users/dubem/file.txt /c/Projects/
python /c/Projects/app/main.py

# Use quoted Windows paths for curl:
curl -o "C:\Users\dubem\file.zip" https://example.com/file.zip

# Use Windows double-backslash for Java:
export JAVA_HOME="C:\\Users\\dubem\\jdk"
```

## Common Failures

| Command | Wrong | Right |
|---------|-------|-------|
| `curl -o /c/Users/x.zip URL` | ❌ Fails to write | ✅ `-o "C:\Users\x.zip"` |
| `export JAVA_HOME=/c/Users/jdk` | ❌ sdkmanager rejects | ✅ `C:\\Users\\jdk` |
| `unzip /c/Users/x.zip` | ✅ Works | Also works |
| `MEDIA:/c/Users/x.apk` | ✅ Works | Also `C:\Users\x.apk` |
