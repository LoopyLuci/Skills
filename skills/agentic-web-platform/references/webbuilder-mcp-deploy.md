# WebBuilder MCP Server Deployability

This reference covers making the WebBuilder MCP Server deployable as an npm package and CLI tool.

## Package Configuration

```json
{
  "name": "@webbuilder/mcp-server",
  "version": "1.0.0",
  "description": "WebBuilder MCP Server — AI agent integration for building web and Android apps",
  "license": "MIT",
  "publishConfig": {
    "access": "public"
  },
  "main": "./dist/index.js",
  "module": "./dist/index.mjs",
  "types": "./dist/index.d.ts",
  "bin": {
    "webbuilder-mcp": "./dist/cli.js"
  },
  "files": ["dist", "README.md"],
  "scripts": {
    "build": "tsup src/index.ts src/cli.ts --format cjs,esm --dts",
    "start": "node dist/cli.js",
    "test": "vitest run"
  }
}
```

## CLI Entry Point

```typescript
#!/usr/bin/env node
import { Command } from 'commander';
import { startMCPServer } from './index.js';

const program = new Command();
program
  .name('webbuilder-mcp')
  .description('WebBuilder MCP Server — AI agent integration')
  .version('1.0.0')
  .action(async () => {
    console.error('Starting WebBuilder MCP Server...');
    await startMCPServer();
  });

program.parse();
```

## Agent Configuration

Users add to their MCP configuration (Claude Desktop, Cursor, Windsurf):

```json
{
  "mcpServers": {
    "webbuilder": {
      "command": "npx",
      "args": ["@webbuilder/mcp-server"]
    }
  }
}
```

## MCP Tool Catalog

| Tool | Description |
|------|-------------|
| `webbuilder_project_create` | Create web project from natural language |
| `webbuilder_project_list` | List all projects |
| `webbuilder_project_get` | Get project details |
| `webbuilder_project_delete` | Delete a project |
| `webbuilder_codegen_generate` | Generate code files |
| `webbuilder_component_search` | Search for components |
| `webbuilder_design_generate` | Generate design system |
| `webbuilder_design_apply_theme` | Apply theme |
| `webbuilder_deploy_preview` | Deploy preview |
| `webbuilder_deploy_production` | Deploy to production |
| `webbuilder_test_generate` | Generate tests |
| `webbuilder_test_run` | Run tests |
| `webbuilder_optimize_performance` | Optimize performance |
| `webbuilder_optimize_accessibility` | Check accessibility |
| `webbuilder_optimize_seo` | Optimize SEO |
| `webbuilder_android_create` | Create Android project |
| `webbuilder_android_components` | List Android components |
| `webbuilder_android_devices` | List device presets |

## Publishing to npm

```bash
# Build
pnpm --filter @webbuilder/mcp-server build

# Login (first time)
npm login

# Publish
pnpm --filter @webbuilder/mcp-server publish --access public
```

## Verification

```bash
# Test CLI locally
npx @webbuilder/mcp-server

# Test in MCP client
# Add to MCP config and verify tools appear
```
