---
name: identity-access-management
description: "Use when implementing IAM and access control systems."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [IAM, identity, access-control, RBAC, ABAC, SSO, LDAP, SAML]
    related_skills: [oauth-authentication-patterns, certificate-management-pki, web-security-patterns, security-incident-response]
---

# Identity and Access Management (IAM)

Implementing IAM systems — from RBAC and ABAC through SSO, directory services, privileged access management, and zero-standing permissions.

## When to Use

- Managing user identities across multiple systems
- Implementing role-based or attribute-based access control
- Setting up SSO for enterprise applications
- Managing API keys and service accounts
- Implementing least-privilege access at scale

## IAM Models

```python
IAM_MODELS = {
    'rbac': 'Users have roles, roles have permissions (simplest, most common)',
    'abac': 'Access based on user/resource/environment attributes (flexible)',
    'reBAC': 'Relationship-based access (Google Zanzibar) — scalable for large systems',
}

class RBACSystem:
    """Role-based access control implementation."""
    def __init__(self):
        self.users = {}       # user -> [roles]
        self.roles = {}       # role -> [permissions]
        self.permissions = {} # permission -> description
    
    def add_permission(self, name: str, description: str = ''):
        self.permissions[name] = description
    
    def create_role(self, name: str, permissions: List[str]):
        self.roles[name] = permissions
    
    def assign_role(self, user: str, role: str):
        self.users.setdefault(user, []).append(role)
    
    def check_access(self, user: str, permission: str) -> bool:
        user_roles = self.users.get(user, [])
        for role in user_roles:
            if permission in self.roles.get(role, []):
                return True
        return False
```

## Common Pitfalls

1. **Role explosion** — too many roles make management impossible; design 10-15 roles max
2. **Permission creep** — never revoking permissions; implement periodic access reviews
3. **Over-privileged service accounts** — 90% of service accounts have more access than needed
4. **No directory integration** — separate user databases everywhere; use central IdP (LDAP, Okta, Azure AD)
5. **Privileged access not monitored** — admin actions should be logged and alerted

## Verification Checklist

- [ ] IAM model selected (RBAC, ABAC, or reBAC)
- [ ] Least-privilege principle applied to all roles
- [ ] Service accounts have minimum required permissions
- [ ] Central identity provider configured (SSO)
- [ ] Periodic access reviews scheduled (quarterly)
- [ ] Privileged access monitoring (PAM)
- [ ] API keys have rotation/expiration policy
- [ ] Audit logging for all access control changes
