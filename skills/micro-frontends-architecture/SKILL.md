---
name: micro-frontends-architecture
description: "Use when building micro-frontend architectures."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [micro-frontends, web-components, module-federation, Qwik, iframe, MFE]
    related_skills: [microservices-decomposition, web-component-design, monorepo-management, frontend-bootstrap]
---

# Micro-Frontends Architecture

Building micro-frontend architectures — from integration approaches (iframe, Web Components, Module Federation) through routing, shared dependencies, and team ownership.

## When to Use

- Large frontend applications with multiple teams
- Decomposing a monolithic frontend into independent features
- Allowing teams to choose their own frontend frameworks
- Incrementally migrating from legacy frontend to modern stack
- Scaling frontend development across multiple teams

## Integration Approaches

```python
INTEGRATION_STRATEGIES = {
    'web_components': 'Each MFE is a Custom Element, framework-agnostic',
    'module_federation': 'Webpack 5 Module Federation — runtime code sharing',
    'iframe': 'Each MFE in its own iframe — strong isolation, poor UX',
    'single_spa': 'Orchestrator framework that mounts/unmounts MFEs',
    'podium': 'Server-side composition of micro-frontends',
}

class MicroFrontendOrchestrator:
    """Client-side micro-frontend integration via Web Components."""
    def __init__(self):
        self.apps = {}  # route -> { name, entry, element }
    
    def register_app(self, route: str, name: str, 
                     entry_url: str, element_name: str):
        self.apps[route] = {
            'name': name, 'entry': entry_url, 'element': element_name
        }
    
    def navigate(self, path: str):
        app = self._match_route(path)
        if app:
            # Lazy load app if not loaded
            self._load_app(app)
            # Render into shell
            container.innerHTML = f'<{app["element"]} route="{path}"></{app["element"]}>'
```

## Common Pitfalls

1. **Shared dependency version hell** — different MFEs using different React versions; agree on shared deps
2. **CSS conflicts** — styles from one MFE leak into another; use Shadow DOM or CSS modules
3. **Cross-MFE communication** — global event bus becomes unmanageable; use custom events with namespacing
4. **Performance overhead** — loading 20 MFEs with 20 bundles on a single page is slow; use lazy loading
5. **Integration testing across MFEs** — changes in one MFE can break integration; contract testing needed

## Verification Checklist

- [ ] Integration strategy chosen (Web Components, Module Federation, or server-side)
- [ ] Shared dependency strategy defined (peer dependencies, externals)
- [ ] Cross-MFE communication pattern (custom events, pub/sub, shared state)
- [ ] Each MFE deployable independently
- [ ] CSS isolation method (Shadow DOM, CSS modules, BEM)
- [ ] Shell application for layout, routing, and error boundaries
- [ ] Performance budget per MFE (bundle size, load time)
- [ ] Contract tests between MFEs and shell
