---
name: network-automation-scripting
description: "Use when automating network configuration and management."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [network-automation, ansible, netmiko, napalm, python-networking, infrastructure-as-code]
    related_skills: [terraform-module-patterns, ci-cd-pipeline-setup, dns-implementation-patterns, monitoring-drift]
---

# Network Automation and Scripting

Automating network device configuration, management, and operations — from Python/Ansible scripts through NetOps/CI/CD pipelines and infrastructure-as-code for networking.

## When to Use

- Configuring and managing many network devices
- Automating repetitive network tasks (backups, upgrades, ACL changes)
- Implementing network infrastructure-as-code
- Reducing human error in network changes
- Building NetOps CI/CD pipelines

## Automation Patterns

```python
NETWORK_AUTOMATION_PATTERNS = {
    'config_push': 'Push configuration to devices via SSH/API (Netmiko, NAPALM)',
    'config_template': 'Use Jinja2 templates with variables for device configs',
    'state_drift': 'Detect config drift between intended and actual device state',
    'crawl_walk_run': 'Test on 1 device → subset → full rollout',
    'backup_before_change': 'Always backup running config before applying changes',
}

class NetAuto:
    """Automate network device interactions."""
    
    @staticmethod
    def backup_configs(devices: List[Dict], backup_dir: str) -> List[str]:
        """Backup running configs from all devices."""
        from netmiko import ConnectHandler
        results = []
        for device in devices:
            try:
                conn = ConnectHandler(**device)
                config = conn.send_command('show running-config')
                hostname = device.get('host', 'unknown')
                path = f"{backup_dir}/{hostname}_{datetime.now():%Y%m%d}.cfg"
                with open(path, 'w') as f: f.write(config)
                results.append(f"✓ {hostname}: backed up")
                conn.disconnect()
            except Exception as e:
                results.append(f"✗ {device.get('host')}: {e}")
        return results
```

## Common Pitfalls

1. **No backup before changes** — critical failure without rollback path
2. **Unhandled edge cases** — device OS differences break scripts; test on each platform
3. **Bulk push without validation** — pushing to 100 devices without pre/post checks
4. **No change management** — automated changes bypassing approval processes
5. **Credential management** — hardcoded credentials in scripts; use vault/secrets

## Verification Checklist

- [ ] Pre-change backup of all target devices
- [ ] Config templates version-controlled (Git)
- [ ] Dry-run mode for validation before applying
- [ ] Change management process integrated (ticket, approval)
- [ ] Rollback plan for each automation run
- [ ] Post-change verification (are changes actually applied?)
- [ ] Credentials stored in secrets manager (not scripts)
