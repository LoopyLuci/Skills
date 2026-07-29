---
name: wsl2-systemd-config
description: "Use when enabling systemd in WSL2 distros."
category: software-development
tags: [wsl2, systemd, linux, service-management]
---
# WSL2 systemd Configuration

Enabling systemd in WSL2 distributions.

## Enable systemd

```ini
# /etc/wsl.conf (inside WSL2 distro)
[boot]
systemd=true
```

```powershell
# Restart WSL2 to apply
wsl --terminate Ubuntu
# Or:
wsl --shutdown
```

## Verify systemd

```bash
# Inside WSL2
systemctl list-units --type=service
systemctl status docker
systemctl status ssh
systemctl --version
```

## Docker with systemd

```bash
# Docker is now managed by systemd automatically
sudo systemctl enable docker
sudo systemctl start docker
sudo systemctl status docker

# Check that it starts on boot
sudo systemctl is-enabled docker
```

## systemd Service Management

```bash
# Enable services that need to autostart
sudo systemctl enable ssh
sudo systemctl enable postgresql

# View all services
systemctl list-unit-files --type=service

# Journal logs
journalctl -u docker -n 50 --no-pager
journalctl -f  # follow logs
```

## Pitfalls

- systemd increases WSL2 startup time slightly
- Not all WSL2 distros support systemd (needs WSL2, not WSL1)
- Some older Ubuntu releases need manual init setup
- Docker installed via apt uses systemd when systemd is enabled
- Conflicts with /etc/init.d scripts that were used before systemd
