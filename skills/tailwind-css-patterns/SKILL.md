---
name: tailwind-css-patterns
description: "Use when implementing Tailwind CSS designs."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [tailwind, CSS, utility-classes, responsive, design-system]
    related_skills: [responsive-web-design-patterns, web-component-design, frontend-bootstrap]
---

# Tailwind CSS Patterns

Implementing designs with Tailwind CSS — from utility-first workflows through responsive design, custom themes, and component extraction.

## When to Use

- Building UIs with Tailwind CSS
- Creating responsive layouts
- Extracting reusable component classes
- Customizing Tailwind theme

## Tailwind Patterns

```jsx
// Responsive component
function Card({ title, children }) {
  return (
    <div className="
      p-4 sm:p-6 md:p-8 
      rounded-lg shadow-md 
      bg-white dark:bg-gray-800 
      hover:shadow-lg transition-shadow
    ">
      <h3 className="text-lg sm:text-xl font-bold text-gray-900 dark:text-white">
        {title}
      </h3>
      <div className="mt-2 text-gray-600 dark:text-gray-300">
        {children}
      </div>
    </div>
  );
}

// Custom theme extension (tailwind.config.js)
module.exports = {
  theme: {
    extend: {
      colors: { brand: { 500: '#6366f1' } },
      spacing: { 18: '4.5rem', 88: '22rem' },
    }
  }
}
```

## Verification Checklist

- [ ] Responsive prefixes (sm:, md:, lg:) on all layouts
- [ ] Dark mode with dark: prefix
- [ ] Custom theme in tailwind.config.js
- [ ] Component extraction for repeated patterns
- [ ] @apply only for shared component base styles
- [ ] PurgeCSS configured for production
