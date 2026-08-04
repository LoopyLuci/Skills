# VS Code 1.109+ Chat API Reference

**Skill:** vscode-mcp-integration  
**Added:** 2026-07-29 — discovered during native chat integration work  
**Source:** VS Code 1.109 release notes + 1.131 runtime

## Overview

VS Code 1.109 (Jan 2026) introduced significant chat API changes. VS Code 1.131 (Jul 2026) has further evolved. Our `@types/vscode` 1.125 lags behind — many APIs are available at runtime but not in type definitions.

## Key APIs (1.109+)

### 1. LanguageModelChatProvider (Updated Signature)

The provider API changed from the older `provideLanguageModelChatResponse` to a new signature:

```typescript
// OLD (our @types/vscode 1.125):
provideLanguageModelChatResponse(model, messages, options, progress, token): Promise<void>

// NEW (VS Code 1.109+ runtime):
provideLanguageModelResponse(messages, options, extensionToken, configuration, token): Promise<void>
```

The `configuration` parameter contains user-entered values from VS Code's UI (API keys, model selections).

### 2. Chat Session Item Controller (NEW in 1.109)

```typescript
const controller = vscode.chat.createChatSessionItemController(
  'myExtension.chatSessions',
  async (token) => {
    const sessions = await fetchSessionsFromBackend();
    const items = sessions.map(s =>
      controller.createChatSessionItem(
        vscode.Uri.parse(`my-scheme://session/${s.id}`),
        s.title
      )
    );
    controller.items.replace(items);
  }
);
```

This is for session management in the sessions sidebar, NOT for the "+" dropdown.

### 3. Agent Types (1.109+)

VS Code 1.109+ organizes chat by "agent types":
- **Local** — runs on user's machine
- **Copilot** — GitHub Copilot
- **Cloud** — remote cloud agents
- **Third-party** — extensions like Hermes

The `languageModelChatProviders` contribution makes extensions appear as third-party agent types.

## Contribution Points

| Contribution | Where it appears | API needed |
|-------------|-----------------|------------|
| `languageModelChatProviders` | Model selector / "+" dropdown as third-party | `vscode.lm.registerLanguageModelChatProvider` |
| `viewsContainers.activitybar` | Left sidebar icon | `WebviewViewProvider` |
| `viewsContainers.panel` | Bottom panel tab | `WebviewViewProvider` |
| Chat participant (API only) | @mentions in any chat | `vscode.chat.createChatParticipant` |

## Pitfalls

1. **`@types/vscode` lags VS Code runtime** — 1.125 types don't have 1.131 APIs. Use `(vscode.lm as any)` casts.
2. **`provideLanguageModelResponse` vs `provideLanguageModelChatResponse`** — method name changed in 1.109+.
3. **`createChatSessionItemController` is for session lists** — NOT for the "+" dropdown.
4. **Third-party agents appear under "Third-party"** — users must click that category to find Hermes.
