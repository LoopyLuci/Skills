---
name: port-forwarding
description: Configure SSH tunnels and port forwarding for dev services
version: 1.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [port, forwarding]
---

# Port Forwarding

## Local Forwarding
```bash
# Access remote service locally
ssh -L 8080:localhost:80 user@server
# Now http://localhost:8080 reaches server:80
```

## Remote Forwarding
```bash
# Expose local service to remote
ssh -R 9090:localhost:3000 user@server
# Server:9090 reaches your local port 3000
```

## Dynamic (SOCKS Proxy)
```bash
ssh -D 1080 user@server
# Use localhost:1080 as SOCKS proxy
```

## Trigger

Activate this skill when the user mentions:
- port, forwarding workflows or issues
- Building, fixing, or optimizing port forwarding


## Core Concepts

- Domain fundamentals and best practices
- Key tools and methodologies
- Quality standards and common patterns
