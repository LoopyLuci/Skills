# WebBuilder CI/CD Pipeline

## Local CI/CD (`scripts/ci-cd.sh`)

A bash script that simulates the GitHub Actions workflow locally.

### Stages

| Stage | Command | Purpose |
|-------|---------|---------|
| Install | `pnpm install --frozen-lockfile` | Install dependencies |
| Build | `pnpm -r build` | Build all 9 packages |
| Test | `pnpm -r test` | Run unit tests in all packages |
| E2E | `node scripts/demo-e2e.cjs` | Generate project from natural language |
| Verify | `cd /tmp/webbuilder-demo && npm install && npm run build` | Verify generated project builds |

### Usage

```bash
pnpm ci
# or
bash scripts/ci-cd.sh
```

### Output

```
========================================================================
  WebBuilder CI/CD Pipeline (Local)
========================================================================

[INFO] Starting: Install Dependencies
[PASS] Dependencies installed
[INFO] Starting: Build All Packages
[PASS] All packages built successfully
[INFO] Starting: Unit Tests
[PASS] @webbuilder/core: tests passed
...
[INFO] Starting: E2E Test
[PASS] E2E demo passed
[INFO] Starting: Verify Generated Project
[PASS] Generated project builds successfully

========================================================================
  CI/CD Pipeline Summary
========================================================================
  Passed: 6
  Failed: 0
  Warnings: 0
========================================================================
Pipeline PASSED
```

## GitHub Actions (`.github/workflows/ci.yml`)

### Jobs

| Job | Depends On | Description |
|-----|------------|-------------|
| lint | — | `pnpm -r lint` |
| test | lint | `pnpm -r test` |
| build | test | `pnpm -r build` |
| e2e | build | E2E demo + verify generated project |
| deploy | e2e | Publish to npm + GitHub Release (main only) |

### Triggers

- Push to `main` or `develop`
- Pull requests to `main`

## E2E Test Script (`scripts/demo-e2e.cjs`)

Generates a complete Next.js project from a natural language description.

### What It Does

1. Parses intent from description
2. Generates project specification
3. Creates 18 files (package.json, tsconfig, pages, components, styles)
4. Writes to `/tmp/webbuilder-demo/<project-id>`

### Usage

```bash
pnpm e2e
# or
node scripts/demo-e2e.cjs
```

### Output

```
======================================================================
WebBuilder E2E Demo — Natural Language → Generated Code
======================================================================

📝 Input Description:
   "Build a landing page for my project management SaaS..."

🔍 Parsing intent...
   ✅ Intent parsed (confidence: 65%)
   📋 Goals: Build a landing page, Create a web application
   📄 Pages: 2
   🎨 Design system: Generated

💾 Project saved: uBEHNzbWYK2AqeFtHhJLM

⚙️  Generating code...
   ✅ Generated 18 files

📁 Writing files to: C:\Users\Server\AppData\Local\Temp\webbuilder-demo\...

🎉 Project Generated Successfully!
```
