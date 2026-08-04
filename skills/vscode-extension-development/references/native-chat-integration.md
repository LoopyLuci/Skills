# Native Chat Integration — API Surface Reference

## Two APIs, Two Purposes

### `vscode.chat.createChatParticipant(id, handler)`
- **Purpose:** Register an `@mention` handler in the built-in chat view
- **Namespace:** `vscode.chat`
- **Result:** User types `@Hermes do something` → handler fires
- **Does NOT:** Appear in the "New Chat" dropdown
- **Supports:** Slash commands (via `participant.slashCommands`), follow-up suggestions, tool call loop

### `vscode.lm.registerLanguageModelChatProvider(vendor, provider)`
- **Purpose:** Register a language model that appears as a selectable chat provider
- **Namespace:** `vscode.lm` (NOT `vscode.chat`)
- **Result:** "New Hermes Chat" appears in the chat panel `+` dropdown
- **Requires:** `languageModelChatProviders` contribution in package.json
- **May NOT be in `@types/vscode`** for older type versions — use `as any` cast

## LanguageModelChatProvider Interface

```typescript
interface LanguageModelChatProvider<T extends LanguageModelChatInformation> {
  // Called to list available models
  provideLanguageModelChatInformation(options, token): ProviderResult<T[]>;

  // Called when user sends a chat message
  provideLanguageModelChatResponse(model, messages, options, progress, token): Thenable<void>;

  // Token counting (character estimate is fine)
  provideTokenCount(model, text, token): Thenable<number>;
}
```

## LanguageModelChatInformation Fields

```typescript
interface LanguageModelChatInformation {
  id: string;              // Unique per provider
  name: string;            // Display name in UI
  family: string;          // e.g. 'hermes', 'gpt-4', 'claude'
  version: string;         // Version string
  maxInputTokens: number;  // Max input tokens
  maxOutputTokens: number; // Max output tokens
  capabilities: {          // What the model supports
    toolCalling?: boolean | number;
    imageInput?: boolean;
  };
  tooltip?: string;
  detail?: string;
}
```

## Streaming Responses

Use `progress.report(new vscode.LanguageModelTextPart(text))` to stream text chunks. The VS Code chat UI renders each chunk as it arrives.

## Activity Bar vs Panel

```json
// Activity bar (left sidebar icons) — what Claude/Copilot use
"viewsContainers": {
  "activitybar": [{ "id": "...", "title": "...", "icon": "..." }]
}

// Panel (bottom area) — what terminal/debug use
"viewsContainers": {
  "panel": [{ "id": "...", "title": "...", "icon": "..." }]
}
```

## Package.json Contribution Points for Chat

```json
{
  "languageModelChatProviders": [{
    "vendor": "hermes",
    "icon": "./assets/icon.svg",
    "name": "Hermes Agent",
    "description": "AI coding assistant"
  }],
  "viewsContainers": {
    "activitybar": [{
      "id": "hermes-chat",
      "title": "Hermes Agent",
      "icon": "./assets/icon.svg"
    }]
  },
  "views": {
    "hermes-chat": [{
      "type": "webview",
      "id": "hermes.chatPanel",
      "name": "Chat"
    }]
  }
}
```

## Registration in extension.ts

```typescript
// Chat participant (@Hermes mentions)
const participant = vscode.chat.createChatParticipant('hermes.hermes', handler);
context.subscriptions.push(participant);

// LM Chat Provider ("New Hermes Chat" dropdown)
context.subscriptions.push(
  (vscode.lm as any).registerLanguageModelChatProvider('hermes', new MyProvider())
);

// Activity bar webview panel
context.subscriptions.push(
  vscode.window.registerWebviewViewProvider('hermes.chatPanel', new PanelProvider())
);
```

## VS Code Version Compatibility

| API | Min VS Code | Notes |
|-----|------------|-------|
| `createChatParticipant` | 1.82 | Well-typed in @types/vscode |
| `registerLanguageModelChatProvider` | 1.93+ | May need `as any` cast in older types |
| `activitybar` viewsContainers | 1.0 | Always available |
| `ChatFollowupProvider` | 1.82 | `prompt` only (no `title` in older types) |
