---
name: web-component-design
description: "Use when building reusable web components."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [web-components, custom-elements, shadow-DOM, HTML-templates, reusable]
    related_skills: [frontend-bootstrap, responsive-web-design-patterns, graphql-client-patterns, web-accessibility-practices]
---

# Web Component Design

Building reusable web components using Web Components standards — Custom Elements, Shadow DOM, HTML Templates, lifecycle hooks, and framework-agnostic design.

## When to Use

- Building framework-agnostic reusable UI components
- Creating design system components that work anywhere
- Encapsulating component styles with Shadow DOM
- Building micro-frontends with shared components

## Component Lifecycle

```javascript
class BaseComponent extends HTMLElement {
    constructor() { super(); this.attachShadow({ mode: 'open' }); }
    connectedCallback() { this.render(); this.addListeners(); }
    disconnectedCallback() { this.removeListeners(); }
    attributeChangedCallback(name, oldVal, newVal) { if (oldVal !== newVal) this.render(); }
    static get observedAttributes() { return ['data-label', 'data-disabled']; }
    
    render() {
        this.shadowRoot.innerHTML = `
            <style>:host { display: block; }</style>
            <div part="container">${this.getAttribute('data-label')}</div>
        `;
    }
}
customElements.define('base-component', BaseComponent);
```

## Common Pitfalls

1. **Over-styling** — Shadow DOM hard to customize; use CSS custom properties and ::part
2. **Form participation** — custom elements need ElementInternals for form integration
3. **Accessibility** — ARIA roles and keyboard navigation aren't automatic
4. **Over-abstraction** — not everything needs to be a web component

## Verification Checklist

- [ ] Lifecycle properly implemented
- [ ] Shadow DOM for style encapsulation
- [ ] CSS custom properties for theming
- [ ] Attribute/property API documented
- [ ] Accessibility (ARIA, keyboard, focus)
- [ ] Tested in multiple frameworks
