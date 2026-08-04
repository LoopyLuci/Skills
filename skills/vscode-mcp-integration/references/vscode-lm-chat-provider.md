# LM Chat Provider Implementation Reference

**Skill:** vscode-mcp-integration  
**Session:** 2026-07-29 — Native VS Code Chat Integration  
**Source files:** `D:\Projects\HermesAgentVSCode\src\chat-model-provider.ts`, `chat-participant.ts`

## Architecture

The VS Code native chat integration uses a **dual-level** approach:

1. **ChatParticipant** (`src/chat-participant.ts`) — `@Hermes` mentions
2. **LM Chat Provider** (`src/chat-model-provider.ts`) — "New Hermes Chat" in the + dropdown

## Key APIs Used

| API | Location | Purpose |
|-----|----------|---------|
| `vscode.chat.createChatParticipant` | VS Code 1.82+ | Register @Hermes mentions |
| `vscode.lm.registerLanguageModelChatProvider` | VS Code 1.130+ | Register native chat session |
| `LanguageModelTextPart` | ctor: `new vscode.LanguageModelTextPart(text)` | Stream response chunks |
| `Progress.report()` | `progress.report(part)` | Push responses to chat view |
| `CancellationToken.onCancellationRequested` | Convert to AbortSignal for fetch | Abort support |

## Package.json Contribution

```json
"contributes": {
  "languageModelChatProviders": [
    {
      "vendor": "hermes",
      "icon": "./assets/hermes-icon.svg",
      "name": "Hermes Agent",
      "description": "AI coding assistant with full VS Code tool access"
    }
  ]
}
```

## Conversion: CancellationToken → AbortSignal

```typescript
function abortSignalFromToken(token: vscode.CancellationToken): AbortSignal {
  const controller = new AbortController();
  token.onCancellationRequested(() => controller.abort());
  return controller.signal;
}
```

## TypeScript Pitfalls

1. **`registerLanguageModelChatProvider` not in @types/vscode** (1.125)—use `(vscode.lm as any).registerLanguageModelChatProvider`
2. **`ChatFollowup` has no `title`** in 1.131 types — use only `prompt`
3. **`slashCommands` may not be typed** — use `(participant as any).slashCommands` in try/catch
4. **Nested backticks in template literals** — use string concatenation instead

## Verification

- [ ] `code --list-extensions` shows `nousresearch.hermes-agent-vscode`
- [ ] Chat panel `+` dropdown shows "Hermes Agent"
- [ ] `curl http://127.0.0.1:19999/health` returns `{"status":"ok","tools":29}`
- [ ] `@Hermes` works in any VS Code chat session
