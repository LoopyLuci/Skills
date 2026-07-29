---
name: wsl2-performance-tuning
description: "Use when tuning WSL2 performance: memory, CPU, swap."
category: software-development
tags: [wsl2, performance, memory, cpu, swap, tuning]
---
# WSL2 Performance Tuning

Tuning WSL2 performance: memory limits, CPU count, swap, VHDX compaction.

## .wslconfig (Global Settings)

```ini
# %USERPROFILE%\.wslconfig
[wsl2]
memory=8GB                # Limit RAM (default: 50% of host)
processors=4              # Limit CPU cores (default: all)
localhostForwarding=true   # Forward WSL2 ports to localhost
swap=2GB                  # Swap file size (default: 25% of memory)
swapFile=C:\Users\limpi\AppData\Local\Temp\swap.vhdx
vmIdleTimeout=60000       # VM idle timeout in ms (default: 60000)
kernelCommandLine= vsyscall=emulate  # For older glibc compatibility
```

## Apply Changes

```powershell
# Edit %USERPROFILE%\.wslconfig, then:
wsl --shutdown
# Restart WSL2 -- new config takes effect
```

## VHDX Compaction (Shrink Disk)

```powershell
# WSL2 VHDX grows over time but rarely shrinks
# Compact to reclaim disk space:

# 1. Find VHDX location (default):
# %LOCALAPPDATA%\Packages\...\LocalState\ext4.vhdx

# 2. Zero free space inside WSL2
wsl -d Ubuntu
sudo dd if=/dev/zero of=/zero bs=1M || true
sudo rm /zero
exit

# 3. Shutdown WSL2
wsl --terminate Ubuntu

# 4. Compact with diskpart
@"
select vdisk file="%LOCALAPPDATA%\Packages\*\LocalState\ext4.vhdx"
attach vdisk readonly
compact vdisk
detach vdisk
exit
"@ | diskpart

# Or use Optimize-VHD (Windows Pro)
Optimize-VHD -Path "$env:LOCALAPPDATA\Packages\*\LocalState\ext4.vhdx" -Mode Full
```

## Performance Best Practices

```bash
# Bad: Working on Windows filesystem
cd /mnt/c/Users/limpi/project
npm install     # SLOW (~10x slower)

# Good: Working on WSL2 filesystem
cd ~/project
npm install     # FAST
```

## Memory Settings

```bash
# Monitor memory within WSL2
free -h
htop

# Check .wslconfig is applied
cat /proc/meminfo | head -5
nproc

# If Docker runs out of memory, increase limit:
# memory=16GB in .wslconfig
```

## Docker Desktop WSL2

```powershell
# Docker Desktop uses separate WSL2 distros
# docker-desktop-data stores images
# Limit Docker memory:
# Docker Desktop → Settings → Resources → Advanced → Memory

# Compact Docker VHDX manually
Optimize-VHD -Path "C:\Users\limpi\AppData\Local\Docker\wsl\data\ext4.vhdx" -Mode Full
```

## Pitfalls

- **wsl --shutdown** resets ALL WSL2 distros -- Docker Desktop data persists but restarts
- **VHDX compaction** requires the distro to be terminated
- **Memory limit** too low causes OOM kills inside WSL2
- **CPU limit** may not improve host performance -- WSL2 already yields CPU when idle
- **.wslconfig** is only read on `wsl --shutdown`, not on individual distro restart
