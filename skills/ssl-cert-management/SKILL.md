---
name: ssl-cert-management
description: Request and renew Let's Encrypt certs with certbot
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [ssl, cert, management]
---

# SSL Certificate Management

## Certbot
```bash
# Install
sudo apt install certbot python3-certbot-nginx

# Get cert
sudo certbot --nginx -d example.com -d www.example.com

# Test renewal
sudo certbot renew --dry-run

# Auto-renewal (systemd)
sudo systemctl enable certbot.timer
```

## Manual DNS Challenge
```bash
certbot certonly --manual --preferred-challenges dns -d example.com
```

## Trigger

Activate this skill when the user mentions:
- ssl, cert, management workflows or issues
- Building, fixing, or optimizing ssl cert management


## Core Concepts

- Domain fundamentals and best practices
- Key tools and methodologies
- Quality standards and common patterns
