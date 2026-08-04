---
name: web-artifacts-builder
description: Use when building complex HTML artifacts with React.
tags: [react, typescript, shadcn-ui, tailwind, html-artifacts]
related_skills: [frontend-design, frontend-bootstrap]
---

# Web Artifacts Builder

Build elaborate, multi-component HTML artifacts using React, Tailwind CSS, and shadcn/ui.

## Quick Start

### Step 1: Initialize Project
```bash
bash scripts/init-artifact.sh <project-name>
cd <project-name>
```

This creates a project with:
- React + TypeScript (Vite)
- Tailwind CSS 3.4.1 with shadcn/ui theming
- Path aliases (`@/`) configured
- 40+ shadcn/ui components pre-installed
- Parcel configured for bundling

### Step 2: Develop Your Artifact
Edit the generated files following the shadcn/ui component patterns.

### Step 3: Bundle to Single HTML
```bash
bash scripts/bundle-artifact.sh
```

Creates `bundle.html` — a self-contained artifact with all JS, CSS, and dependencies inlined.

### Step 4: Share with User
Share the bundled HTML file in conversation for viewing.

### Step 5: Test (Optional)
Only test if requested or if issues arise.

## Design Guidelines

- Avoid excessive centered layouts, purple gradients, uniform rounded corners, and Inter font (hallmarks of "AI slop")
- Use modern, distinctive design choices

## Code Example

```tsx
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

export function MyComponent() {
  return (
    <Card className="p-6">
      <h2 className="text-2xl font-bold mb-4">Hello World</h2>
      <Button onClick={() => alert("Clicked!")}>Click Me</Button>
    </Card>
  );
}
```

## Reference

- shadcn/ui components: https://ui.shadcn.com/docs/components

## Common Pitfalls

- ❌ **Skipping the bundle step** — React won't work as plain HTML
- ❌ **Using Inter font by default** — Choose distinctive typefaces
- ❌ **Overly complex components** — Keep artifacts focused and performant
- ❌ **Not testing the bundle** — Always verify `bundle.html` works standalone

## Verification Checklist

- [ ] Project initializes and builds successfully
- [ ] Bundle step produces `bundle.html` without errors
- [ ] All dependencies included inline (no external CDN needed)
- [ ] Components render correctly in browser
- [ ] Design avoids "AI slop" hallmarks
- [ ] Console has no errors
