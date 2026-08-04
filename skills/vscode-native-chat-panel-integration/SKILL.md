---
name: vscode-native-chat-panel-integration
description: Use when building VS Code native Chat panel integrations.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [vscode, chat, participant, provider, extension, native-ui, integration]
    related_skills: [vscode-extension-development, vscode-mcp-integration, vscode-extension-100-year-architecture]
---

# VS Code Native Chat Panel Integration

## Overview

VS Code's built-in Chat panel can be extended at **three distinct levels**, each controlled by a separate `package.json` contribution point plus a runtime API call. Confusing them is the #1 reason "my extension doesn't appear in the + dropdown."

| Level | Contribution `package.json` | Runtime API | What the user sees |
|-------|---------------------------|-------------|-------------------|
| **Chat Participant** (mention) | `chatParticipants` | `vscode.chat.createChatParticipant(id, handler)` | Type `@Hermes` in any chat session |
| **LM Chat Provider** (model) | `languageModelChatProviders` | `vscode.lm.registerLanguageModelChatProvider(vendor, provider)` | Model selector in chat UI |
| **Activity Bar** (sidebar icon) | `viewsContainers.activitybar` | `WebviewViewProvider` | Icon in left sidebar |

**Critical distinction:**

- `chatParticipants` → registers a **chat participant** (`@Hermes` mention + `createChatParticipant` handler)
- `languageModelChatProviders` → registers a **LANGUAGE MODEL** that appears in the model picker
- `viewsContainers.activitybar` → your OWN chat sidebar (the surface third-party AI extensions actually ship)
- You need BOTH participants and providers for full native integration: one for the @-mention, one for the LLM power

**Ground truth (verified on VS Code 1.131, July 2026): the Chat "+" dropdown ("New Chat / New Codex Agent / New Copilot CLI Session") is populated ONLY by VS Code's built-in agent-host harnesses (the 1.131 agent-host rearchitecture based on the Agent Host Protocol). Third-party extensions do NOT appear there — not even Claude Code.** Inspected `anthropic.claude-code-2.1.220-win32-x64/package.json`: zero `chatParticipants`, zero `languageModelChatProviders`; it contributes only `viewsContainers`/views/commands/keybindings and ships its own sidebar. So "my extension is missing from the + dropdown" is a **non-bug**: no third party is listed there. The real integration surfaces are (1) `@Hermes` in native chat, (2) the model picker via `languageModelChatProviders`, (3) your own activity-bar view. Do not chase a "+ dropdown" entry — it is not achievable via the extension API (only via the experimental agent-host protocol, `chat.agentHost.enabled`).

## The Three Levels

### Level 1: Chat Participant — @Mention

Makes `@Hermes` available in any VS Code chat session.

**`package.json`:**
```json
"chatParticipants": [
  {
    "id": "hermes-agent-vscode.hermes",
    "name": "Hermes",
    "fullName": "Hermes Agent",
    "description": "AI coding assistant with 29 VS Code tools",
    "icon": "./assets/hermes-icon.svg",
    "isSticky": true
  }
]
```

**Runtime:**
```typescript
const p = vscode.chat.createChatParticipant(
  'hermes-agent-vscode.hermes',  // MUST match "id"
  async (request, context, stream, token) => { /* handler */ }
);
p.iconPath = new vscode.ThemeIcon('symbol-constant');
try { (p as any).displayName = 'Hermes Agent'; } catch {}
context.subscriptions.push(p);
```

### Level 2: LM Chat Provider — Model Picker

Makes the extension selectable as a language model.

**`package.json`:**
```json
"languageModelChatProviders": [
  {
    "vendor": "hermes",
    "icon": "./assets/hermes-icon.svg",
    "name": "Hermes Agent",
    "description": "AI coding assistant with 29 VS Code tools"
  }
]
```

**Runtime:**
```typescript
try {
  context.subscriptions.push(
    (vscode.lm as any).registerLanguageModelChatProvider(
      'hermes',  // MUST match vendor
      { provideLanguageModelChatInformation, provideLanguageModelResponse, provideTokenCount }
    )
  );
} catch (err) { console.warn('Failed:', err); }
```

### Level 3: Activity Bar — Sidebar Icon

**`package.json`:**
```json
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
}
```

**Key:** `"activitybar"` = left sidebar. `"panel"` = bottom panel.

## Combined Skeleton

```json
{
  "activationEvents": ["onStartupFinished"],
  "contributes": {
    "chatParticipants": [{
      "id": "ext.id",
      "name": "Agent",
      "fullName": "My Agent",
      "description": "What it does",
      "icon": "./assets/icon.svg",
      "isSticky": true
    }],
    "languageModelChatProviders": [{
      "vendor": "myvendor",
      "icon": "./assets/icon.svg",
      "name": "My Agent",
      "description": "Description"
    }],
    "viewsContainers": {
      "activitybar": [{
        "id": "my-chat",
        "title": "My Agent",
        "icon": "./assets/icon.svg"
      }]
    },
    "views": {
      "my-chat": [{ "type": "webview", "id": "my.panel", "name": "Chat" }]
    }
  }
}
```

## Verification

- [ ] `chatParticipants` id matches `createChatParticipant()` argument
- [ ] `languageModelChatProviders` vendor matches `registerLanguageModelChatProvider()` argument
- [ ] SVG icon is 24x24, stroke-based
- [ ] `.vscodeignore` does NOT exclude `assets/`
- [ ] All registrations wrapped in try/catch
- [ ] `"onStartupFinished"` in activationEvents
- [ ] Both `chatParticipants` AND `createChatParticipant` present
- [ ] **Confirm what actually surfaces** — don't assume the extension host Node matches your dev Node. Add a runtime probe to your MCP/HTTP `/health` endpoint reporting `process.versions.node`, `process.versions.electron`, and whether `node:sqlite` (`.DatabaseSync`) resolves; then `curl /health`. VS Code 1.131 uses Node 24 / Electron 42 (much newer than @types/vscode): verify at runtime, not by reading types.

## Pitfalls

1. **chatParticipants ≠ languageModelChatProviders.** One adds a participant; the other adds a MODEL.
2. **chatParticipants requires VS Code 1.130+.** Silently ignored on older versions.
3. **Icon must be SVG file path, not a Codicon.** `$(symbol-constant)` works in code, not in package.json.
4. **@types/vscode lags behind actual API.** Use raw JSON fields — VS Code validates from schema, not types. VS Code 1.131's runtime Node is Node 24 / Electron 42; `node:sqlite` IS available there — usable for reading the Hermes Desktop `state.db` directly from the extension host.
5. **Activation events matter.** Without `onStartupFinished`, nothing fires until the user runs a command.
6. **"Not in the + dropdown" is NOT a registration bug.** That dropdown is built-in agent-host harnesses only (verified 1.131); Claude Code itself doesn't appear there. Verify @-mention, model picker, and activity-bar instead of re-adding contribution points.
7. **Extension host Node ≠ dev machine Node.** Probe the runtime (`node:sqlite` availability, versions) through your own health endpoint before relying on built-in modules; feature-detect and fall back (e.g. to `globalState`) when unavailable.
