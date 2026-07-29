---
name: firewall-configuration
description: "Configure ufw iptables firewall rules for common services"
---

# Firewall Configuration

## UFW (Ubuntu)
```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
sudo ufw status verbose
```

## Common Rules
```bash
sudo ufw allow from 192.168.1.0/24
sudo ufw deny from 10.0.0.1
sudo ufw limit ssh  # Rate limit SSH attempts
```
