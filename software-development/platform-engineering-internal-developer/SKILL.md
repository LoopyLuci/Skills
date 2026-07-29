---
name: platform-engineering-internal-developer
description: "Use when building internal developer platforms."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [platform-engineering, IDP, developer-experience, Backstage, golden-path]
    related_skills: [site-reliability-engineering, gitops-argocd-flux, devsecops-shift-left, monorepo-management]
---

# Platform Engineering and IDPs

Building internal developer platforms (IDPs) — from platform as a product through golden paths, Backstage, developer portals, and reducing cognitive load on developers.

## When to Use

- Reducing developer friction and cognitive load
- Standardizing infrastructure and deployment patterns
- Building self-service developer capabilities
- Creating golden paths for common workflows

## Platform Engineering

```python
PLATFORM_PRINCIPLES = {
    'platform_as_product': 'Treat platform like a product — user research, roadmap, feedback cycles',
    'golden_paths': 'Curated, opinionated workflows for common tasks (deploy, create service, add DB)',
    'cognitive_load': 'Reduce decisions developers need to make; provide sensible defaults',
    'self_service': 'Developers provision infra, deploy, and manage via UI/CLI without tickets',
    'abstraction': 'Hide infrastructure complexity behind simple interfaces (CRUD for services)',
}

class DeveloperPortal:
    """Self-service developer portal capabilities."""
    capabilities = {
        'scaffold_service': 'Template-based service creation with CI/CD, monitoring, docs',
        'deploy': 'One-click deploy to staging/production with rollback',
        'add_database': 'Provision PostgreSQL/Redis with backups, monitoring, connection string',
        'view_logs': 'Aggregated logs with search, filters, and alerting',
        'add_secret': 'Store and rotate secrets with audit trail',
        'run_migration': 'Execute database migrations with dry-run and rollback',
    }
```

## Verification Checklist

- [ ] Platform treated as product (user research, roadmap, feedback)
- [ ] Golden paths defined for common workflows
- [ ] Self-service capabilities for infra, deploy, databases
- [ ] Developer portal (Backstage, custom, or Portal) operational
- [ ] Cognitive load measured and reduced (surveys, DORA metrics)
- [ ] Platform adoption tracked (teams using golden paths)
- [ ] Platform documentation current and discoverable
