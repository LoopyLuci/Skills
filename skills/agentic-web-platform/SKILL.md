---
name: agentic-web-platform
description: "Architect MCP-first agentic web building platforms."
version: 0.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [mcp, agentic, web-builder, multi-agent, codegen, monorepo, architecture]
    related_skills: [claude-code, codex, opencode]
---

# Agentic Web Platform

Build next-generation agentic web building platforms where AI agents are first-class citizens — not bolted-on assistants. This skill covers the architecture, MCP integration, multi-agent orchestration, code generation pipeline, and monorepo structure for platforms that let agents design, develop, and deploy web projects.

## When to Use

- Designing an AI-native web development platform from scratch
- Adding MCP (Model Context Protocol) server capabilities to a web building tool
- Building multi-agent orchestration for collaborative web development
- Creating a code generation pipeline from natural language → structured spec → working code
- Architecting a monorepo for agentic development tools
- Implementing intent parsing for project specifications

Don't use for:
- Simple website builders without agent integration
- Single-agent coding assistants (use `claude-code` or `codex` instead)
- Static site generators or traditional CMS tools

## Architecture Overview

The platform follows an MCP-first, agent-native architecture:

```
┌─────────────────────────────────────────────────────────────────┐
│                     AGENT LAYER (MCP + Custom)                  │
│  Hermes Agent │ Claude │ Codex │ Custom Agents │ Future Agents  │
└──────────────────────────┬──────────────────────────────────────┘
                           │ MCP Protocol
┌──────────────────────────▼──────────────────────────────────────┐
│                      MCP SERVER GATEWAY                         │
│   Tools: project/create, component/search, design/generate,     │
│          codegen/generate, deploy/preview, test/run, etc.       │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                       CORE ENGINES                              │
│  Intent │ Context │ Component │ Design │ Logic │ Deploy │ Observe │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                    PROJECT MANAGER                              │
│   Persistence │ History │ File System │ Version Tracking       │
└─────────────────────────────────────────────────────────────────┘
```

### Seven Core Engines

| Engine | Responsibility |
|--------|---------------|
| **Intent Parser** | Natural language → structured project spec (goals, constraints, pages, design, features, deployment) |
| **Context Manager** | Cross-session state, agent memory, time-travel debugging, user preference learning |
| **Component Engine** | Framework-agnostic component registry (React/Vue/Svelte/Angular/Vanilla adapters) |
| **Design Engine** | Token system, CSS variable generation, Tailwind config, WCAG validation |
| **Logic Engine** | Features, integrations, workflows, data models, API generation |
| **Deploy Engine** | Multi-target deployment (Vercel/Netlify/Cloudflare/AWS/Docker) with cost estimation |
| **Observability** | Performance metrics, analytics, logging, alerting, feedback |

## MCP Server Design

### Tool Catalog Structure

Every capability is exposed as an MCP tool with Zod-validated schemas. **IMPORTANT**: Tool names use underscores (`webbuilder_project_create`), NOT slashes (`webbuilder/project/create`). Slashes trigger MCP validation warnings:

```typescript
server.registerTool(
  'webbuilder_project_create',
  {
    description: 'Create a new web project from a natural language description',
    inputSchema: {
      description: z.string(),
      name: z.string().optional(),
      outputDir: z.string().optional(),
    },
  },
  async ({ description, name, outputDir }) => {
    const parsed = parseIntent(description);
    const generated = generateCode(parsed.spec);
    // Write files to disk...
    return { content: [{ type: 'text', text: JSON.stringify(result) }] };
  }
);
```

### Tool Categories

| Category | Tools |
|----------|-------|
| **Project** | `project/create`, `project/list`, `project/get`, `project/delete` |
| **Code Gen** | `codegen/generate` |
| **Component** | `component/search`, `component/add` |
| **Design** | `design/generate`, `design/apply-theme` |
| **Deploy** | `deploy/preview`, `deploy/production` |
| **Testing** | `test/generate`, `test/run` |
| **Optimize** | `optimize/performance`, `optimize/accessibility`, `optimize/seo` |

## Multi-Agent Orchestration

### Agent Types

| Agent | Role | Capabilities |
|-------|------|-------------|
| **Designer** | Visual design | Design systems, color palettes, typography, responsive layouts |
| **Developer** | Implementation | Component coding, API development, feature implementation |
| **Tester** | Quality assurance | Unit/integration/e2e/visual/a11y/performance tests |
| **Optimizer** | Performance | Core Web Vitals, bundle optimization, SEO, accessibility |
| **Deployer** | Deployment | Multi-target deployment, rollback, CI/CD |
| **Orchestrator** | Coordination | Workflow management, dependency resolution, task delegation |

### Workflow Execution

```typescript
const orchestrator = new AgentOrchestrator();
const workflow = orchestrator.createWorkflow('Build Landing Page');

orchestrator.addStep(workflow.id, 'designer', { type: 'create-design-system' });
orchestrator.addStep(workflow.id, 'developer', { type: 'implement-components' }, [designStepId]);
orchestrator.addStep(workflow.id, 'tester', { type: 'run-tests' }, [devStepId]);

const result = await orchestrator.executeWorkflow(workflow.id);
```

## Code Generation Pipeline

### Pipeline Stages

```
Natural Language Description
           │
           ▼
    ┌──────────────┐
    │ Intent Parser │ → Goals, Constraints, References, Pages, Design, Features
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │  Spec Builder │ → Complete ProjectSpec (JSON)
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │ Code Generator│ → FileChange[] (package.json, pages, components, styles)
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │ File Writer   │ → Files written to disk, ready to run
    └──────────────┘
```

### Generated Output Structure

```
project/
├── package.json          # Dependencies, scripts
├── tsconfig.json         # TypeScript config
├── next.config.js        # Next.js config
├── tailwind.config.js    # Design tokens → Tailwind theme
├── postcss.config.js     # PostCSS with Tailwind
├── .gitignore
├── src/
│   ├── app/
│   │   ├── layout.tsx    # Root layout with header/footer
│   │   ├── globals.css   # CSS variables from design tokens
│   │   └── page.tsx      # Home page
│   ├── pages/
│   │   └── index.tsx     # Main page with all sections
│   ├── components/
│   │   ├── HeroDefault.tsx
│   │   ├── FeaturesDefault.tsx
│   │   ├── PricingDefault.tsx
│   │   └── ...
│   └── styles/
│       └── tokens.json   # Design tokens
```

## Intent Parser Design

The Intent Parser converts natural language into a complete project specification:

```typescript
interface ParsedIntent {
  intent: Intent;           // Extracted goals, constraints, references
  spec: Partial<ProjectSpec>; // Generated project specification
  clarificationsNeeded: ClarificationQuestion[];
  confidence: number;       // 0-1 confidence score
}
```

### Extraction Targets

| Source | Extracted |
|--------|-----------|
| "Build a landing page for my SaaS" | Goals: ["Build a landing page"] |
| "Use React and Tailwind" | Constraints: [{type: "tech-stack", value: "React"}] |
| "Make it look like Stripe" | References: [{type: "design", description: "Stripe"}] |
| "Fast, accessible, dark mode" | Constraints: [performance, accessibility, custom] |

## Project Manager

Handles persistence and lifecycle:

```typescript
class ProjectManager {
  create(spec: ProjectSpec): ProjectEntry;
  load(projectId: string): ProjectSpec | null;
  save(spec: ProjectSpec): void;
  list(): ProjectEntry[];
  delete(projectId: string): boolean;
  saveFile(projectId: string, path: string, content: string): void;
  addHistoryEntry(projectId: string, change: ChangeSet): void;
}
```

## Monorepo Structure

```
webbuilder/
├── packages/
│   ├── core/              ← Intent, Context, Component, Design, Logic, Deploy, Observe + Codegen
│   ├── mcp-server/        ← MCP server with tool catalog
│   ├── agents/            ← Multi-agent orchestration system
│   ├── components/        ← Universal component library
│   ├── cli/               ← Developer CLI
│   ├── plugins/           ← Plugin SDK + Marketplace
│   ├── testing/           ← Testing utilities
│   └── ai/                ← AI models + prompt templates
├── apps/
│   ├── web/               ← Visual editor + dashboard (Next.js)
│   ├── docs/              ← Documentation site
│   └── playground/        ← Interactive playground
└── examples/              ← Sample projects
```

## Component Engine

Framework-agnostic component system:

```typescript
interface Component {
  id: string;
  name: string;
  spec: ComponentSpec;                    // Atomic/Composite/Pattern/Template
  implementations: Partial<Record<Framework, FrameworkImplementation>>;
  props: PropSchema[];
  styles: StyleSchema;
  accessibility: A11ySchema;
}
```

Supported frameworks: React, Vue, Svelte, Angular, Vanilla JS, Solid, Qwik.

## Design Token System

```typescript
interface DesignTokens {
  colors: TokenSet;      // Primary, secondary, accent, semantic
  fonts: TokenSet;       // Sans, mono, display
  spacing: TokenSet;     // 0-32 scale
  sizing: TokenSet;      // sm, base, lg, xl
  borders: TokenSet;     // thin, medium, thick
  shadows: TokenSet;     // sm, md, lg, xl
  radii: TokenSet;       // sm, md, lg, xl, full
  opacity: TokenSet;     // disabled, hover, overlay
  semantic: SemanticTokens; // Primary, surface, text, background
}
```

## Quick Reference

### Creating a New Project

```typescript
// 1. Parse intent
const parsed = parseIntent("Build a landing page for my SaaS");

// 2. Create project
const projectManager = createProjectManager();
projectManager.create(parsed.spec as ProjectSpec);

// 3. Generate code
const generated = generateCode(parsed.spec as ProjectSpec);

// 4. Write files
for (const file of generated.files) {
  writeFileSync(join(outputDir, file.path), file.content);
}
```

### Adding an MCP Tool

```typescript
server.registerTool(
  'webbuilder/<domain>/<action>',
  {
    description: 'Clear description of what this tool does',
    inputSchema: {
      paramName: z.string().describe('Parameter description'),
      optionalParam: z.number().optional().describe('Optional parameter'),
    },
  },
  async ({ paramName, optionalParam }) => {
    // Implementation
    return { content: [{ type: 'text', text: JSON.stringify(result) }] };
  }
);
```

### Registering an Agent

```typescript
orchestrator.registerAgent('designer', new DesignerAgent());
orchestrator.registerAgent('developer', new DeveloperAgent());
```

## Pitfalls

1. **Circular type imports**: Core package engines must not import from each other. Use the types barrel (`types/index.ts`) for shared types.

2. **Optional vs required fields**: When building type systems for generated code, make most fields optional with sensible defaults. TypeScript strict mode will catch missing required fields at build time.

3. **Template literal types in generated code**: When generating code templates with `${variable}` syntax, ensure escape sequences are correct in TypeScript template literals.

4. **Framework adapter parity**: Each component implementation should have the same props interface across all framework adapters, even if the implementation differs.

5. **MCP tool schema evolution**: Adding optional fields to existing tool schemas is backward compatible. Changing required fields breaks existing agent integrations.

6. **Intent parser confidence**: Low confidence scores (< 0.5) should trigger clarifying questions rather than proceeding with assumptions.

7. **File system paths in MCP**: Always use `path.join()` for cross-platform compatibility. Never hardcode `/` or `\` in paths.

8. **MCP tool naming**: Use underscores (`webbuilder_project_create`), not slashes (`webbuilder/project/create`). Slashes trigger MCP validation warnings and may cause compatibility issues with some clients.

9. **Compiled JS files in src/**: When iterating on TypeScript monorepos, stale `.js` and `.d.ts` files in `src/` can cause runtime errors even after fixing the `.ts` source. Always `find src -name "*.js" -delete` before rebuilding when encountering mysterious import errors.

## Verification

- [ ] MCP server starts and tools are discoverable by agents
- [ ] Intent parser correctly extracts goals, constraints, and references from descriptions
- [ ] Code generator produces valid, runnable project files
- [ ] All packages build successfully (CJS + ESM + DTS)
- [ ] Multi-agent workflows execute with correct dependency resolution
- [ ] Component engine supports at least React and one other framework
- [ ] Design tokens generate valid CSS variables and Tailwind config

## References

- `references/webbuilder-local-first-deploy.md` — local-first deployment: bare metal, Docker, Kubernetes, export module
- `references/webbuilder-codegen-lessons.md` — code generation bugs, fixes, and testing patterns
- `references/webbuilder-cicd.md` — CI/CD pipeline (local script + GitHub Actions)
- `references/webbuilder-mcp-deploy.md` — MCP server npm packaging and CLI entry point
- `references/webbuilder-browser-patterns.md` — persistence, editor interactions, error boundaries
