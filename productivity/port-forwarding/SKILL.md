---
name: port-forwarding
description: "Configure SSH tunnels and port forwarding for dev services"
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
