---
name: wsl2-filesystem-bridge
description: "Use when navigating files between Windows and WSL2."
category: software-development
tags: [wsl2, filesystem, windows, paths, interoperability]
---
# WSL2 Filesystem Bridge

Navigating files between Windows and WSL2.

## Windows → WSL2 (from Windows)

```powershell
# Access WSL2 files from Windows via UNC path
\\wsl.localhost\Ubuntu\home\user\project
\\wsl.localhost\docker-desktop\...

# Or via drive mapping
net use W: \\wsl.localhost\Ubuntu\home\user

# Or via WSL CLI
wsl -d Ubuntu -- ls -la /home/user/project
```

## WSL2 → Windows (from WSL2)

```bash
# Windows drives are mounted under /mnt/
ls /mnt/c/Users/limpi/
cd /mnt/d/Projects/

# Or via fast localhost path
\\wsl.localhost\Ubuntu\home\user\project
```

## Performance — Critical!

```bash
# /mnt/c is SLOW for I/O-heavy operations (DrvFs translation)
# WSL2 native filesystem is MUCH faster (ext4 via ext4.vhdx)

# GOOD: Keep projects in WSL2 filesystem
cd ~
mkdir project && cd project
git clone <repo>
npm install   # fast!

# BAD: Work on Windows filesystem from WSL2
cd /mnt/c/Users/limpi/project
npm install   # slow!
```

## wsl.conf Configuration

```ini
# /etc/wsl.conf
[automount]
enabled = true
mountFsTab = true
root = /mnt/
options = "metadata,umask=22,fmask=111"

[interop]
enabled = true
appendWindowsPath = true

[network]
generateHosts = true
generateResolvConf = true

# Restart WSL2 after editing: wsl --shutdown
```

## .wslconfig (Global, in Windows)

```ini
# %USERPROFILE%\.wslconfig
[wsl2]
memory=8GB
processors=4
localhostForwarding=true
swap=2GB
swapFile=C:\\Users\\limpi\\swap.vhdx
```

## Common Tasks

```bash
# Open current WSL2 directory in Windows Explorer
explorer.exe .

# Open Windows file from WSL2
notepad.exe /mnt/c/Users/limpi/notes.txt

# Run Windows tool on WSL2 files
code .   # VS Code with Remote-WSL
```

## Symlinks

```bash
# Create symlink from Windows to WSL2 directory
# (Run from WSL2)
ln -s /home/user/project ~/project-link

# Enable Windows symlink support in wsl.conf
# /etc/wsl.conf
[automount]
options = "metadata"
```

## Pitfalls

- **DrvFs performance** -- avoid node_modules, large git repos, or build caches on /mnt/
- **Case sensitivity** -- Windows is case-insensitive; ext4 is case-sensitive; can cause git issues
- **File permissions** -- WSL2 files accessed from Windows may show incorrect permissions
- **Windows Defender** scans WSL2 filesystem -- add exclusions for performance
- **Locked files** -- WSL2 files can't be modified by Windows while in use by WSL2
