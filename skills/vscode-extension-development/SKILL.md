---
name: vscode-extension-development
description: Use for VS Code extensions with native chat, tools, and MCP.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [vscode, extension, development, chat, mcp, native-ui, build]
---

# VS Code Extension Development

## Overview

Build VS Code extensions that integrate natively into the editor's UI — activity bar, chat sidebar, and tool infrastructure. Covers the full lifecycle: project setup, tool registration, chat integration, build pipeline, and packaging.

## Critical Pitfalls

### 1. ChatParticipant ≠ Chat Provider (COMMON MISTAKE)
`vscode.chat.createChatParticipant` registers an `@mention` participant in the built-in chat. `vscode.lm.registerLanguageModelChatProvider` + `languageModelChatProviders` registers a MODEL in the chat model picker. Neither adds a "+ dropdown" entry — see the ground-truth note below.

**Correct approach (all three, for full integration):**
- `ChatParticipant` → `@Hermes` mentions in any chat session
- `LanguageModelChatProvider` → Hermes in the model picker
- `viewsContainers.activitybar` → your own sidebar chat (the surface real third-party AI extensions use)

**GROUND TRUTH (verified VS Code 1.131, July 2026): the Chat "+" dropdown ("New Chat / New Codex Agent / New Copilot CLI Session") is populated ONLY by VS Code's built-in agent-host harnesses (Agent Host Protocol). Third-party extensions do not appear there — not even Claude Code** (inspected `anthropic.claude-code-2.1.220/package.json`: zero chatParticipants, zero languageModelChatProviders — only viewsContainers/commands). A "missing + dropdown entry" is a non-bug; do not chase it. The agent-host protocol (`chat.agentHost.enabled`) is the only opt-in path, and it's experimental.

### 2. activitybar vs panel in viewsContainers
`viewsContainers.panel` puts your webview in the BOTTOM panel area. `viewsContainers.activitybar` puts an ICON in the LEFT sidebar (like Explorer, Search, Git). For Claude-like integration, use `activitybar`.

```json
"viewsContainers": {
  "activitybar": [{
    "id": "hermes-chat",
    "title": "Hermes Agent",
    "icon": "./assets/icon.svg"
  }]
}
```

### 3. LanguageModelChatProvider API location
`registerLanguageModelChatProvider` is in `vscode.lm`, NOT `vscode.chat`. And it may not be in `@types/vscode` for older type versions — use `(vscode.lm as any).registerLanguageModelChatProvider(...)` with try/catch for forward compatibility.

### 4. MCP tools/list requires initialization first
The MCP protocol requires `initialize` before `tools/list`. Without it, tools returns empty array. Always send `initialize` first in tests.

### 5. Extension activation on reload
After `code --install-extension`, VS Code doesn't always reload. Use `code -r -g D:/path/file:1` to force a window reload that triggers the new extension host.

### 6. onStartupFinished is essential
Without `onStartupFinished` in activationEvents, the MCP server won't auto-start. Early builds failed because the stale .vsix didn't have this event.

## Build Pipeline

```bash
# 1. Type-check (zero errors required)
npx tsc --noEmit --pretty

# 2. Bundle with esbuild
node esbuild.js

# 3. Package .vsix
rm -f *.vsix && npx vsce package

# 4. Kill old MCP server
PID=$(netstat -ano | grep 19999 | grep LISTENING | awk '{print $5}')
[ -n "$PID" ] && taskkill /F /PID $PID

# 5. Install and reload
code --install-extension hermes-agent-vscode-1.0.0.vsix --force
code -r -g README.md:1
```

## Tool Call Loop Pattern

The LLM outputs tool calls in ` ```tool {"name":"...","arguments":{...}} ``` ` blocks. Parse, execute, feed results back, repeat.

```typescript
// Extract tool calls from LLM text
const calls = [];
const pattern = /```tool\n?([\s\S]*?)```/g;
let match;
while ((match = pattern.exec(text)) !== null) {
  const parsed = JSON.parse(match[1].trim());
  if (parsed?.name) calls.push({ name: parsed.name, arguments: parsed.arguments || {} });
}

// Remove tool blocks from final text
const clean = text.replace(/```tool\n?[\s\S]*?```/g, '').trim();
```

Max 8-10 iterations. Each tool call result goes back as a user message with `[Tool Result: name]` wrapper.

## Native Chat Integration Checklist

- [ ] `package.json` has `languageModelChatProviders` contribution with vendor name
- [ ] `package.json` has `viewsContainers.activitybar` for sidebar icon
- [ ] `package.json` has `activationEvents: ["onStartupFinished"]`
- [ ] Extension registers `ChatParticipant` via `vscode.chat.createChatParticipant`
- [ ] Extension registers `LanguageModelChatProvider` via `vscode.lm.registerLanguageModelChatProvider`
- [ ] Extension registers `WebviewViewProvider` for the activity bar panel
- [ ] SVG icon is 24x24, stroke-based, matches VS Code's icon style
- [ ] `.vscodeignore` does NOT exclude `assets/` directory
- [ ] System prompt includes tool descriptions in the LLM-compatible format

## package.json Contribution Structure

```json
{
  "contributes": {
    "languageModelChatProviders": [{
      "vendor": "hermes",
      "icon": "./assets/hermes-icon.svg",
      "name": "Hermes Agent",
      "description": "..."
    }],
    "viewsContainers": {
      "activitybar": [{
        "id": "hermes-chat",
        "title": "Hermes Agent",
        "icon": "./assets/hermes-icon.svg"
      }]
    },
    "views": {
      "hermes-chat": [{
        "type": "webview",
        "id": "hermes.chatPanel",
        "name": "Chat"
      }]
    },
    "commands": [...],
    "configuration": { "properties": { ... } }
  }
}
```

## When to Use

- Building any VS Code extension with chat UI
- Integrating AI agents into VS Code's native chat
- Setting up MCP servers as VS Code extensions
- Creating activity bar panels with webview UI

## Support Files

- `references/native-chat-integration.md` — deeper chat integration detail
- `references/shared-db-bridge.md` — safe pattern for a second process reading/writing another app's live SQLite DB (node:sqlite, read-only reads, source-tagged writes, live-DB verification recipe). Use when syncing an extension with an app-owned state DB (e.g. Hermes Desktop `state.db`).
- `references/skin-theme-sync.md` — mirror an app's skin/theme engine onto webview CSS custom properties (built-in presets + user YAML overrides, light/dark polarity from VS Code's active theme, live reload via config watcher + fs.watch, lazy `require('vscode')` accessor so the module stays unit-testable in pure Node).
- `references/eslint9-flat-config.md` — hardening `npm run lint` for a TS extension: ESLint 9 + typescript-eslint 8 flat config, rule tuning rationale (require-await off for tool-registry contract, no-misused-promises checksVoidReturn:false for event-emitter code, unnecessary-condition/optional-chain off for defensive config paths), and the dead-code cleanup workflow (89→0 problems, zero behavior change).
- `references/mcp-reliability-self-healing.md` — making an MCP-over-HTTP server hosted by a VS Code extension self-healing: EADDRINUSE port-fallback retry (error listener + recursive `listen`), health-check watchdog with auto-restart after N consecutive failures, and using `context.secrets` (SecretStorage) instead of settings.json for API keys.
