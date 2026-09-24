# WebBuilder Code Generation Lessons

This file captures session-specific lessons learned during the development of WebBuilder's code generation pipeline.

## Bugs Found and Fixed

### 1. Layout Imports Non-Existent Components
**Problem**: Generated `src/app/layout.tsx` imported `Header` and `Footer` components that were never generated.
**Error**: `Cannot find module '@/components/Header' or its corresponding type declarations`
**Fix**: Removed imports for non-existent components. Layout now only imports `globals.css` and renders `{children}` directly.

### 2. Component Interfaces Too Restrictive
**Problem**: Generated component interfaces only had `title`, `subtitle`, `className` props, but pages passed additional props like `columns`, `type`, `limit`.
**Error**: `Type '{ title: string; columns: number; }' is not assignable to type 'IntrinsicAttributes & StatsGridProps'`
**Fix**: Added `[key: string]: any` index signature to all generated component interfaces, plus `...props` rest parameter.

### 3. Intent Parser Constructor Signature
**Problem**: IntentParser constructor takes no arguments; description goes to `parse()`.
**Error**: `Cannot read properties of undefined (reading 'toLowerCase')` when tests passed description to constructor
**Fix**: Tests create `const parser = new IntentParser()` then call `parser.parse(description)`.

## Testing Patterns

### Vitest TypeScript in Monorepo
**Problem**: Vitest fails to resolve `.ts` extensions in imports within monorepo packages.
**Solution**: 
- Use `import { X } from '../src/module'` (without `.ts` extension) in test files
- Build the package first (`pnpm build`) before running tests if importing from `dist/`
- Keep `vitest.config.ts` simple — minimal resolve config

### Verifying Generated Code Works
**Problem**: Code generation tests pass but generated code doesn't actually compile.
**Solution**: Always run E2E verification:
1. Generate project with `node scripts/demo-e2e.cjs`
2. Navigate to generated directory
3. Run `npm install && npm run build`
4. Verify dev server starts and serves pages

## Architecture Decisions

### Generated Component Interface Pattern
```typescript
export interface ComponentNameProps {
  title?: string;
  subtitle?: string;
  className?: string;
  [key: string]: any;  // Allow arbitrary props
}

export function ComponentName({ title, subtitle, className = '', ...props }: ComponentNameProps) {
  return (
    <section className={`py-16 px-8 ${className}`}>
      {/* Component content */}
    </section>
  );
}
```

### Minimal Layout Pattern
```typescript
'use client';
import './globals.css';

export const metadata = { title: 'Project Name', description: 'Description' };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <main>{children}</main>
      </body>
    </html>
  );
}
```

## CI/CD Pipeline

### Local CI/CD Script (`scripts/ci-cd.sh`)
Stages: Install → Build → Test → E2E → Verify Generated Project
Run with: `pnpm ci` or `bash scripts/ci-cd.sh`

### GitHub Actions Workflow (`.github/workflows/ci.yml`)
Stages: Lint → Test → Build → E2E → Deploy (production only)

### E2E Test Script (`scripts/demo-e2e.cjs`)
Generates a project from natural language and writes files to `/tmp/webbuilder-demo/`.
Run with: `pnpm e2e` or `node scripts/demo-e2e.cjs`

## Key Insight
Always verify generated code actually works end-to-end — compilation, build, and serving. TypeScript errors in generated code are silent failures that only surface when users try to run the project.
