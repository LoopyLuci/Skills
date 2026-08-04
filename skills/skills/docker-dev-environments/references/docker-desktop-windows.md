# Docker Desktop on Windows — Installation Troubleshooting

## Common Issues

### Docker Desktop not installed (registry says installed, files missing)

Symptoms: `winget list Docker` shows Docker Desktop 4.x.x, but `docker.exe` not found anywhere.

Fix:
```bash
# Check registry
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall" /s /f Docker

# If installed but broken: download fresh installer
curl -L -o DockerDesktopInstaller.exe "https://desktop.docker.com/win/main/amd64/234817/Docker%20Desktop%20Installer.exe"

# Run installer (requires admin for clean install)
DockerDesktopInstaller.exe install
```

### Docker Desktop installed but daemon not responding

Symptoms: `docker info` hangs or returns "Docker Desktop is unable to start".

Fix:
```bash
# Kill all Docker processes
taskkill /f /im "Docker Desktop.exe" 2>/dev/null
taskkill /f /im "com.docker.backend.exe" 2>/dev/null

# Wait and restart
sleep 5
"Docker Desktop.exe" &

# Wait for daemon
for i in $(seq 1 20); do
    sleep 3
    docker info >/dev/null 2>&1 && echo "Docker ready!" && break
done
```

### Docker Desktop requires admin privileges

The installer needs elevated privileges. Options:
1. Run installer from admin Command Prompt
2. Use `winget install Docker.DockerDesktop` in admin terminal
3. Fall back to local MSVC/GCC build without Docker

### WSL2 backend issues

Docker Desktop uses WSL2 on Windows. If the WSL2 distribution is stopped:
```bash
wsl -l -v  # Check WSL status
wsl -d docker-desktop  # Start Docker's WSL distro
```

### Docker not in PATH after installation

Docker Desktop installs `docker.exe` to `C:\Program Files\Docker\Docker\resources\bin\`. If not in PATH:
```bash
# Add to current session
export PATH="/c/Program Files/Docker/Docker/resources/bin:$PATH"

# Or use full path
"/c/Program Files/Docker/Docker/resources/bin/docker.exe" version
```

## Fallback: Build Without Docker

When Docker is unavailable, build locally:
```bash
# Windows (MSVC)
cmd.exe /c "build_msvc.bat Release stub"

# Linux (Clang 17)
cmake -B build -G Ninja -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_C_COMPILER=clang-17 -DCMAKE_CXX_COMPILER=clang++-17
cmake --build build --parallel
```
