---
name: network-diagnostics
description: "Diagnose connectivity traceroute mtr tcpdump analysis"
---

# Network Diagnostics

## Quick Checks
```bash
# Connectivity
ping -c 4 google.com

# Path tracing
traceroute google.com
mtr google.com

# Port check
nc -zv host 80
```

## DNS
```bash
nslookup example.com
dig example.com
dig -x 8.8.8.8  # Reverse lookup
```

## HTTP Debugging
```bash
curl -v https://example.com
curl -o /dev/null -w "Connect: %{time_connect}s, Total: %{time_total}s" https://example.com
```
