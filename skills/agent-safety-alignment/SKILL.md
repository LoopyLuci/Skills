---
name: agent-safety-alignment
description: "Use when implementing safety guardrails for AI agents."
category: mlops
tags: [agents, safety, alignment, guardrails, constraints]
---
# Agent Safety & Alignment

Implementing safety guardrails and alignment for AI agents.

## Safety Layers

```
User Input
    │
    ▼
[Layer 1: Input Guard]     — filters malicious prompts
    │
    ▼
[Layer 2: Permission Check] — checks if action is allowed
    │
    ▼
[Layer 3: Action Approval]  — high-risk actions need confirmation
    │
    ▼
[Layer 4: Output Guard]     — filters harmful outputs
    │
    ▼
[Layer 5: Audit Log]        — records all actions
```

## Input Guard

```python
class InputGuard:
    def __init__(self):
        self.blocked_patterns = [
            r"ignore.*(previous|all).*instructions",
            r"you are (not|free|released)",
            r"(system|admin|root).*prompt",
            r"rm\s+-rf\s+(/|~)",
            r">\s*/dev/sda",
            r"DROP\s+TABLE",
            r"DELETE\s+FROM.*WHERE",
        ]

    def check(self, user_input: str) -> tuple[bool, str]:
        for pattern in self.blocked_patterns:
            import re
            if re.search(pattern, user_input, re.IGNORECASE):
                return False, f"Blocked: potentially harmful pattern detected"
        return True, "OK"

    def sanitize(self, user_input: str) -> str:
        # Remove excessive whitespace
        return " ".join(user_input.split())
```

## Permission System

```python
class PermissionSystem:
    def __init__(self):
        self.permissions = {
            "read_file": {"requires": [], "confirm": False},
            "write_file": {"requires": ["confirm"], "confirm": True},
            "delete_file": {"requires": ["confirm", "admin"], "confirm": True},
            "run_command": {"requires": ["confirm"], "confirm": True},
            "install_package": {"requires": ["confirm", "admin"], "confirm": True},
        }

    def check_action(self, action: str, user_roles: list[str]) -> tuple[bool, str]:
        if action not in self.permissions:
            return False, f"Unknown action: {action}"

        perm = self.permissions[action]
        for req in perm["requires"]:
            if req == "admin" and "admin" not in user_roles:
                return False, f"Action requires admin privileges"
            if req == "confirm":
                return False, f"Action requires user confirmation"
        return True, "OK"

    def request_confirmation(self, action: str, args: dict) -> bool:
        print(f"\n⚠️  Confirm: {action}")
        for k, v in args.items():
            print(f"   {k}: {v}")
        response = input("Proceed? (y/N): ")
        return response.lower() == 'y'
```

## Action Approval Workflow

```python
class ActionApproval:
    def __init__(self, critical_actions: list[str] = None):
        self.critical_actions = critical_actions or [
            "delete", "remove", "format", "drop",
            "shutdown", "reboot", "install", "uninstall",
        ]

    def needs_approval(self, action_description: str) -> bool:
        action_lower = action_description.lower()
        return any(c in action_lower for c in self.critical_actions)

    def approve(self, action: str, context: dict) -> tuple[bool, str]:
        if not self.needs_approval(action):
            return True, "Auto-approved (non-critical)"

        print(f"\n🔴 CRITICAL ACTION REQUIRES APPROVAL:")
        print(f"   Action: {action}")
        print(f"   Context: {context}")
        response = input("   Approve? (y/N): ")
        if response.lower() == 'y':
            return True, "Approved by user"
        return False, "Rejected by user"
```

## Audit Logging

```python
import json
from datetime import datetime

class AuditLogger:
    def __init__(self, log_file: str = "agent_audit.jsonl"):
        self.log_file = log_file

    def log(self, entry_type: str, agent_name: str,
            action: str, result: str, approved: bool):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": entry_type,
            "agent": agent_name,
            "action": action,
            "result": str(result)[:1000],
            "approved": approved,
        }
        with open(self.log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def get_recent(self, n: int = 10) -> list:
        if not os.path.exists(self.log_file):
            return []
        with open(self.log_file) as f:
            lines = f.readlines()[-n:]
        return [json.loads(l) for l in lines]
```

## Pitfalls

- Overly restrictive guardrails block legitimate actions
- Under-restrictive guardrails miss dangerous actions
- Input guards can be bypassed with encoding/obfuscation
- User confirmation fatigue → users approve without reading
- Audit logs must be append-only and tamper-evident
