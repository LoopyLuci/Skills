---
name: vscode-mcp-integration
description: "Use when building VS Code MCP extensions for AI agents."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [vscode, mcp, extensions, typescript, ai-agents, webview]
    related_skills: [mcp-server, mcp-server-development, frontend-bootstrap]
---

# VS Code MCP Integration — Extensions with AI Agent Tool Access

## Overview

Build VS Code extensions that expose editor capabilities as MCP (Model Context Protocol) tools, allowing AI agents like Hermes to control VS Code. Supports a **dual-mode architecture**:

- **Embedded mode**: An AI chat webview panel inside VS Code, talking to any OpenAI-compatible LLM (Ollama, OpenAI, OpenRouter)
- **External mode**: VS Code runs an MCP HTTP/SSE server on localhost. Hermes Desktop/CLI connects via `mcp_servers` config and gets 29+ VS Code control tools

## When to Use

- User wants "VS Code extension for AI agent" or "use Hermes to control VS Code"
- Building a coding agent that edits files, runs terminals, debugs, and manages git inside VS Code
- Creating a webview-based chat panel with LLM streaming inside VS Code
- Integrating VS Code with Hermes Agent, Claude Code, or any MCP-compatible client

**Don't use for:**
- General VS Code extension development without AI/agent aspects
- Python-only MCP servers (use `mcp-server-development` skill instead)
- Configuring Hermes to use existing MCP servers (see `hermes-agent` skill's `references/native-mcp.md`)

## Architecture

```
┌──────────────────────────────────────────────────────┐
│                    VS Code Window                     │
│                                                       │
│  ┌─────────────────────┐    ┌─────────────────────┐  │
│  │                     │    │  Extension Host      │  │
│  │  Hermes Webview     │◄──►│  ┌───────────────┐  │  │
│  │  (Chat UI)          │    │  │ MCP Server     │  │  │
│  │  postMessage IPC    │    │  │ (JSON-RPC 2.0) │  │  │
│  └─────────────────────┘    │  └───────┬───────┘  │  │
│                             │          │           │  │
│                             │          ▼           │  │
│                             │  ┌───────────────┐  │  │
│                             │  │ VS Code API    │  │  │
│                             │  └───────────────┘  │  │
│                             └─────────────────────┘  │
└──────────────────────────────────────────────────────┘
                              │ HTTP/SSE (localhost:19999)
                              ▼
              ┌──────────────────────────────────┐
              │  Hermes Desktop / CLI             │
              │  (mcp_servers.vscode.url)         │
              └──────────────────────────────────┘
```

## Project Structure

```
vscode-extension/
├── .vscode/
│   └── launch.json              # Extension Host debug config
├── src/
│   ├── extension.ts             # Entry point: activate(), deactivate()
│   ├── config.ts                # Constants, settings, system prompt
│   ├── mcp.ts                   # MCP protocol: MCPServer, Stdio/HTTP transports
│   ├── llm.ts                   # OpenAI-compatible LLM streaming client
│   ├── tools/
│   │   ├── registry.ts          # Tool registration, VsCodeContext interface
│   │   ├── editor.ts            # Editor tools (open, edit, tabs, diagnostics)
│   │   ├── terminal.ts          # Terminal tools (create, send, read)
│   │   ├── files.ts             # File system tools (read, write, search)
│   │   ├── commands.ts          # VS Code command execution tools
│   │   ├── workspace.ts         # Workspace tools (folders, config, tasks)
│   │   ├── debug.ts             # Debug tools (start, stop, variables)
│   │   └── git.ts               # Git tools (branches, status, commands)
│   ├── webview/
│   │   ├── panel.ts             # WebviewViewProvider for chat panel
│   │   └── media/               # Frontend assets
│   │       ├── index.html       # Chat UI template (CSP-compliant)
│   │       ├── style.css        # Dark-theme chat styles
│   │       └── chat.js          # Chat logic, markdown rendering, streaming
│   └── mcp-server.ts            # Standalone diagnostics CLI
├── package.json                 # Extension manifest
├── tsconfig.json                # TypeScript config
├── esbuild.js                   # Bundle config (vscode external)
└── README.md
```

## Key Implementation Patterns

### 1. MCP Protocol in TypeScript (JSON-RPC 2.0)

Implement the MCP protocol directly — no external SDK needed for a VS Code extension (the `vscode` module must be external, making bundled SDKs problematic).

**Core types:**
```typescript
interface MCPRequest { jsonrpc: '2.0'; id: number | string; method: string; params?: Record<string, unknown>; }
interface MCPResponse { jsonrpc: '2.0'; id: number | string | null; result?: unknown; error?: MCPError; }
```

**Message flow:**
1. Client sends `initialize` → Server responds with capabilities + serverInfo
2. Client sends `tools/list` → Server returns all registered tools
3. Client sends `tools/call` with name + arguments → Server executes handler, returns result

**Tool registration:**
```typescript
server.registerTool(name, description, inputSchema, async (args) => {
  const ctx = getVsCodeContext();
  const result = await ctx.someMethod(args.path);
  return { content: [{ type: 'text', text: result }] };
});
```

### 2. HTTP/SSE Transport

The MCP server runs inside the VS Code extension host. Use HTTP/SSE (not stdio) because a standalone Node.js process can't access `vscode` APIs.

**Endpoints:**
- `GET /mcp` → SSE event stream (client connects here, gets session_id)
- `POST /mcp?session_id=xxx` → Send JSON-RPC message, response via SSE
- `GET /health` → Status check (returns tool count, server state)

### 3. VsCodeContext Bridge

Abstract VS Code API access behind an interface so MCP tool handlers don't depend on the `vscode` module directly:

```typescript
interface VsCodeContext {
  getActiveEditorContent(): Promise<{content:string; language:string; fileName:string} | null>;
  editFile(path: string, edits: Edit[]): Promise<void>;
  createTerminal(name?: string): {name:string; send(text:string):void; show():void};
  executeCommand(command: string, ...args: unknown[]): Promise<unknown>;
  readFile(path: string): Promise<string>;
  writeFile(path: string, content: string): Promise<void>;
  getWorkspaceFolders(): string[];
  getDiagnostics(path?: string): Promise<Diagnostic[]>;
  getOpenTabs(): TabInfo[];
  startDebugging(config?: Record<string, unknown>): Promise<boolean>;
  gitCommand(args: string[]): Promise<string>;
}
```

The context is set once during `activate()` and accessed via a module-level getter:
```typescript
let _getContext: (() => VsCodeContext) | null = null;
export function setContextAccessor(getter: () => VsCodeContext): void { _getContext = getter; }
export function getVsCodeContext(): VsCodeContext {
  if (!_getContext) throw new Error('VS Code context not available');
  return _getContext();
}
```

### 4. Webview Chat UI

The webview panel uses `WebviewViewProvider` with `postMessage` IPC:

```typescript
// Extension host → webview (outbound)
private _postMessage(message: { type: string; payload?: unknown }): void {
  this._view?.webview.postMessage(message);
}

// Webview → extension host (inbound)
webviewView.webview.onDidReceiveMessage(async (msg) => {
  switch (msg.type) {
    case 'chat': await this._handleChat(msg.payload); break;
    case 'abort': this._abortController?.abort(); break;
    case 'getModels': await this._sendModels(); break;
    case 'setConfig': this._handleSetConfig(msg.payload); break;
  }
});
```

**Message types (webview → extension host):** `chat`, `abort`, `getModels`, `getConfig`, `setConfig`, `openFile`, `clearConversation`
**Message types (extension host → webview):** `addMessage`, `startStream`, `streamChunk`, `endStream`, `streamError`, `modelsList`, `configData`, `toolCall`, `toolResult`, `toolLoopThinking`

### 5. esbuild Bundle Config

```javascript
const config = {
  entryPoints: ['src/extension.ts', 'src/mcp-server.ts'],
  bundle: true,
  outdir: 'dist',
  external: ['vscode'],           // CRITICAL: vscode is only available in extension host
  format: 'cjs',
  platform: 'node',
  target: 'node18',
  sourcemap: true,
  metafile: true,
  keepNames: true,
};
```

### 6. Tool-Calling Loop (Webview LLM → MCP Tools)

The webview chat LLM needs a tool-calling loop to actually USE the registered MCP tools. Without it, the LLM can talk about code but never read, edit, or debug anything. The loop architecture:

```
User message → Build messages (system + tool descriptions + workspace context + history)
  → LLM chatComplete (non-streaming)
  → Parse response for `` `tool` `` JSON blocks
  → If tool blocks found:
      Execute each via MCPServer
      Show tool call card in webview (spinning → done/error)
      Feed result back into message history
      Loop: call LLM again with updated history
  → If no tool blocks:
      Stream clean text (with tool blocks removed) to webview
      Mark complete
```

**Algorithm (panel.ts):**

```typescript
private async _runToolLoop(): Promise<void> {
  const MAX_ITERATIONS = 10;
  let iteration = 0;

  while (iteration < MAX_ITERATIONS) {
    iteration++;

    // 1. Build context-aware messages
    const fullMessages = await this._buildMessages();

    // 2. Call LLM (non-streaming for loop cycle)
    const responseText = await chatComplete(fullMessages, this._config, abortSignal);

    // 3. Parse for tool call blocks
    const toolCalls = extractToolCalls(responseText);

    if (toolCalls.length === 0) {
      // No more tools — stream final text
      const cleanText = removeToolBlocks(responseText);
      if (cleanText) {
        this._messages.push({ role: 'assistant', content: cleanText });
        this._postMessage({ type: 'startStream', payload: {} });
        // Stream in chunks for smooth animation
        const chunkSize = Math.max(Math.ceil(cleanText.length / 20), 1);
        for (let i = 0; i < cleanText.length; i += chunkSize) {
          this._postMessage({ type: 'streamChunk', payload: { content: cleanText.slice(i, i + chunkSize) } });
        }
        this._postMessage({ type: 'endStream', payload: {} });
      }
      return;
    }

    // 4. Execute each tool call, feed results back
    for (const tc of toolCalls) {
      this._postMessage({ type: 'toolCall', payload: { name: tc.name, arguments: tc.arguments } });

      const toolEntry = this._mcpServer.getTool(tc.name);
      if (!toolEntry) {
        const errMsg = `Tool "${tc.name}" not found`;
        this._postMessage({ type: 'toolResult', payload: { tool: tc.name, error: true, result: errMsg } });
        this._messages.push({ role: 'user', content: `<tool_error>${errMsg}</tool_error>` });
        continue;
      }

      try {
        const result = await toolEntry.handler(tc.arguments || {});
        const resultText = result.content?.[0]?.text || '(empty result)';
        this._postMessage({ type: 'toolResult', payload: { tool: tc.name, error: false, result: resultText } });
        this._messages.push({ role: 'user', content: `[Tool Result: ${tc.name}]\n\`\`\`\n${resultText.slice(0, 8000)}\`\`\`` });
      } catch (err) {
        this._postMessage({ type: 'toolResult', payload: { tool: tc.name, error: true, result: String(err) } });
        this._messages.push({ role: 'user', content: `<tool_error name="${tc.name}">\n${String(err)}\n</tool_error>` });
      }
    }

    // 5. Prevent context overflow
    if (this._messages.length > 60) this._messages = this._messages.slice(-50);
    this._saveMessages();
  }
}
```

**Tool call block parsing (the key interface between LLM and tools):**

```typescript
function extractToolCalls(text: string): ParsedToolCall[] {
  const calls: ParsedToolCall[] = [];
  const pattern = /\`\`\`tool\n?([\s\S]*?)\`\`\`/g;
  let match;
  while ((match = pattern.exec(text)) !== null) {
    try {
      const parsed = JSON.parse(match[1].trim());
      if (parsed && typeof parsed.name === 'string') {
        calls.push({ name: parsed.name, arguments: (parsed.arguments as Record<string, unknown>) || {} });
      }
    } catch { /* skip malformed */ }
  }
  return calls;
}

function removeToolBlocks(text: string): string {
  return text.replace(/\`\`\`tool\n?[\s\S]*?\`\`\`/g, '').trim();
}
```

**Build tool descriptions for system prompt:**

The LLM needs to know which tools exist and how to call them. Generate the description dynamically from `MCPServer.getAllTools()`:

```typescript
function buildToolDescriptions(server: MCPServer): string {
  const tools = server.getAllTools();
  const lines = tools.map(t => {
    const props = (t.inputSchema.properties || {}) as Record<string, { description?: string; type?: string }>;
    const args = Object.keys(props).length > 0
      ? Object.entries(props).map(([k, v]) => `    ${k} (${v.type || 'any'}): ${v.description || ''}`).join('\n')
      : '    (no arguments)';
    return `- **${t.name}**: ${t.description}\n${args}`;
  });
  return `## Available Tools\n\nYou have access to ${tools.length} tools. To call one:\n\n\`\`\`tool\n{"name":"tool_name","arguments":{...}}\n\`\`\`\n\n${lines.join('\n\n')}`;
}
```

**System prompt instructions:**

The system prompt tells the LLM how to use tools:

```typescript
export const SYSTEM_PROMPT = `You are Hermes Agent, an AI coding assistant integrated into VS Code.
...
## How to Call Tools
To call a tool, embed this exact format in your response:

\`\`\`tool
{"name":"tool_name","arguments":{...}}
\`\`\`

The tool will be executed and the result fed back to you.
...
## Guidelines
- Call tools proactively — don't ask the user to do things you can do
- Read files before editing them to understand context
- If a tool fails, explain the error and try an alternative approach
- Don't ask "shall I?" — just do it and explain what you did
`;
```

**Workspace context injection:**

Before each tool loop iteration, inject current workspace state so the LLM knows what the user is working on:

```typescript
private async _gatherContext(): Promise<string> {
  const parts: string[] = [];

  // Active file + selection
  const editor = vscode.window.activeTextEditor;
  if (editor) {
    parts.push(`**Active file:** \`${editor.document.fileName}\` (${editor.document.languageId})`);
    if (!editor.selection.isEmpty) {
      parts.push(`**Selection:** ${editor.document.getText(editor.selection).slice(0, 200)}`);
    }
  }

  // Open tabs (first 8)
  const tabs = vscode.window.tabGroups.all.flatMap(group =>
    group.tabs.filter(t => t.input instanceof vscode.TabInputText)
      .map(t => (t.input as vscode.TabInputText).uri.fsPath)
  );
  if (tabs.length > 0) parts.push(`**Open tabs:** ${tabs.slice(0, 8).join(', ')}${tabs.length > 8 ? ` +${tabs.length - 8} more` : ''}`);

  // Diagnostics (errors only, first 5)
  const errors = [];
  for (const [uri, diags] of vscode.languages.getDiagnostics()) {
    for (const d of diags) {
      if (d.severity === vscode.DiagnosticSeverity.Error) {
        errors.push({ file: uri.fsPath, line: d.range.start.line + 1, message: d.message });
      }
    }
  }
  if (errors.length > 0) parts.push(`**Errors:** ${errors.slice(0, 5).map(e => `\`${e.file}:${e.line}\` ${e.message}`).join('; ')}`);

  // Git branch
  try {
    const gitApi = vscode.extensions.getExtension('vscode.git')?.exports?.getAPI(1);
    const repo = gitApi?.repositories?.[0];
    if (repo?.state?.HEAD?.name) parts.push(`**Git branch:** ${repo.state.HEAD.name}`);
  } catch { /* git not available */ }

  return parts.join('\n');
}
```

**Conversation persistence:**

Save/load chat history via `vscode.ExtensionContext.globalState`:

```typescript
// In HermesPanelProvider constructor:
this._messages = context.globalState.get<LLMMessage[]>('hermes.conversation.v1', []);

// After each tool loop completion:
private _saveMessages(): void {
  const toSave = this._messages.slice(-100);
  this._context.globalState.update('hermes.conversation.v1', toSave);
}
```

**Tool call card rendering (webview side):** — see `references/message-assembly-tool-loop.md` for the message building and streaming patterns.

```javascript
// chat.js — Add a spinning tool call card
function addToolCallCard(name, args) {
  const card = document.createElement('div');
  card.className = 'tool-call-card';
  card.innerHTML = `
    <div class="tool-call-header">
      <span class="tool-call-icon">🔧</span>
      <span class="tool-call-name">${escapeHtml(name)}</span>
      <span class="tool-call-status spinning">⟳</span>
    </div>
    <div class="tool-call-args"><pre>${escapeHtml(JSON.stringify(args, null, 2))}</pre></div>
    <div class="tool-call-result-container hidden"><div class="tool-call-result"></div></div>
  `;
  messagesEl.appendChild(card);
  requestAnimationFrame(() => card.classList.add('visible'));
  scrollToBottom();
}

// Update card when tool completes
function updateToolCallCard(name, result, isError) {
  const card = findLastSpinningCard(name);
  if (!card) return;
  const status = card.querySelector('.tool-call-status');
  const resultContainer = card.querySelector('.tool-call-result-container');
  status.textContent = isError ? '❌' : '✅';
  status.className = `tool-call-status ${isError ? 'error' : 'done'}`;
  card.classList.add(isError ? 'tool-call-error' : 'tool-call-done');
  resultContainer.classList.remove('hidden');
  if (result) resultContainer.querySelector('.tool-call-result').textContent = String(result).slice(0, 1000);
  scrollToBottom();
}
```

Key CSS for tool cards:

```css
.tool-call-card {
  align-self: flex-start;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-left: 3px solid var(--accent);     /* blue while running */
  border-radius: 8px;
  margin: 2px 0;
  width: 100%;
  opacity: 0;
  transform: translateY(4px);
  transition: opacity 0.2s, transform 0.2s;
}
.tool-call-card.visible { opacity: 1; transform: translateY(0); }
.tool-call-done { border-left-color: var(--success); }  /* green when done */
.tool-call-error { border-left-color: var(--error); }    /* red on error */
.tool-call-status.spinning { animation: spin 1.2s linear infinite; }
```

**Abort mechanism:**

Allow the user to stop generation mid-stream:

```typescript
// panel.ts — AbortController managed per-turn
this._abortController = new AbortController();

// In _runToolLoop, check before each LLM call:
if (this._abortController?.signal.aborted) return;

// On abort message from webview:
case 'abort':
  this._abortController?.abort();
  this._postMessage({ type: 'endStream', payload: { aborted: true } });
  break;
```
```javascript
// chat.js — Stop button and Escape key
stopBtn.addEventListener('click', () => vscode.postMessage({ type: 'abort' }));
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && state.streaming) {
    e.preventDefault();
    vscode.postMessage({ type: 'abort' });
  }
});
```

### 7. Native Chat Integration — Dual-Level Architecture

VS Code's native chat can be integrated at **two levels**, each solving a different user-facing need:

| Level | API | What the user sees |
|-------|-----|-------------------|
| **1. ChatParticipant** (`@Hermes`) | `vscode.chat.createChatParticipant` | Type `@Hermes` in any chat session to invoke the tool agent |
| **2. LM Chat Provider** (native session) | `vscode.lm.registerLanguageModelChatProvider` + `languageModelChatProviders` contribution | **"Hermes Agent"** appears in the Chat panel's `+` dropdown alongside "New Chat", "New Codex Session" |

You should implement BOTH. Level 1 is quick to add. Level 2 requires a `package.json` contribution point and is what makes the extension feel like a built-in VS Code feature.

#### Level 1: ChatParticipant (@Hermes Mentions)

Register a chat participant. Users type `@Hermes` in any existing chat session.

**Key differences from webview panel:**
- Uses `stream.markdown()` instead of `postMessage` for output
- Uses `vscode.CancellationToken` (converted to `AbortSignal` for fetch)
- No tool call cards — results are fed back to LLM silently, only final markdown streams
- Supports file references (`#file:path`) and slash commands
- Registered with try/catch for backward API compatibility

#### Registration

```typescript
export function registerChatParticipant(
  context: vscode.ExtensionContext,
  mcpServer: MCPServer
): vscode.ChatParticipant {
  const participant = vscode.chat.createChatParticipant(
    'hermes-agent-vscode.hermes',
    async (request, _chatContext, stream, token) => {
      await handleRequest(request, stream, token, mcpServer);
    }
  );
  participant.iconPath = new vscode.ThemeIcon('symbol-constant');
  participant.followupProvider = {
    provideFollowups(): vscode.ChatFollowup[] {
      return [
        { prompt: 'What can you do?' },
        { prompt: 'Explain the current file' },
        { prompt: 'Find and fix errors' },
        { prompt: 'Refactor this code' },
      ];
    },
  };
  try {
    (participant as any).slashCommands = [
      { name: 'help', description: 'Show available tools' },
      { name: 'explain', description: 'Explain selected code' },
      { name: 'fix', description: 'Find and fix errors' },
      { name: 'test', description: 'Generate tests' },
    ];
  } catch { /* older VS Code — slash commands not supported */ }
  context.subscriptions.push(participant);
  return participant;
}
```

Wrap in try/catch during activate() since `vscode.chat` may not exist:

```typescript
try {
  if (mcpServer) registerChatParticipant(context, mcpServer);
} catch (err) {
  console.warn('[Hermes] Chat participant registration failed:', err);
}
```

#### CancellationToken Conversion

```typescript
function abortSignalFromToken(token: vscode.CancellationToken): AbortSignal {
  const controller = new AbortController();
  token.onCancellationRequested(() => controller.abort());
  return controller.signal;
}
```

#### Tool Loop in Chat Handler

The same algorithm as the webview panel, but output goes to `stream.markdown()`:

```typescript
async function handleRequest(
  request: vscode.ChatRequest,
  stream: vscode.ChatResponseStream,
  token: vscode.CancellationToken,
  mcpServer: MCPServer
): Promise<void> {
  const config = getLLMConfig();
  const llmSignal = abortSignalFromToken(token);

  // Build messages: system + tool descriptions + workspace context + references
  let messages: LLMMessage[] = [
    { role: 'system', content: SYSTEM_PROMPT },
    { role: 'system', content: buildToolDescriptions(mcpServer) },
  ];
  const wsContext = await gatherWorkspaceContext();
  if (wsContext) messages.push({ role: 'system', content: `## Current Workspace Context\n${wsContext}` });

  // Handle file references from chat input (#file:path)
  if (request.references?.length) {
    const fileContents: string[] = [];
    for (const ref of request.references) {
      if (ref.value instanceof vscode.Uri) {
        try {
          const doc = await vscode.workspace.openTextDocument(ref.value);
          fileContents.push(`### ${ref.value.fsPath}\n\`\`\`${doc.languageId}\n${doc.getText()}\n\`\`\``);
        } catch { /* skip unreadable */ }
      }
    }
    if (fileContents.length > 0)
      messages.push({ role: 'system', content: `## Referenced Files\n${fileContents.join('\n\n')}` });
  }

  messages.push({ role: 'user', content: request.prompt });

  // Tool loop (same algorithm, MARKDOWN output instead of postMessage)
  const MAX_ITERATIONS = 8;
  for (let i = 0; i < MAX_ITERATIONS; i++) {
    if (token.isCancellationRequested) return;
    const responseText = await chatComplete(messages, config, llmSignal);
    const toolCalls = extractToolCalls(responseText || '');
    if (toolCalls.length === 0) {
      const cleanText = removeToolBlocks(responseText || '');
      if (cleanText) stream.markdown(cleanText);
      return;
    }
    for (const tc of toolCalls) {
      const toolEntry = mcpServer.getTool(tc.name);
      if (!toolEntry) {
        messages.push({ role: 'user', content: `<error>Tool "${tc.name}" not found</error>` });
        continue;
      }
      try {
        const result = await toolEntry.handler(tc.arguments || {});
        const text = result.content?.[0]?.text || '(empty)';
        messages.push({ role: 'user', content: `[Tool Result: ${tc.name}]\n\`\`\`\n${text.slice(0, 8000)}\n\`\`\`` });
      } catch (err) {
        messages.push({ role: 'user', content: `<error name="${tc.name}">${String(err)}</error>` });
      }
    }
    if (messages.length > 50) messages = [...messages.slice(0, 3), ...messages.slice(-47)];
  }
  stream.markdown('\n\n> ⚠️ Reached max tool iterations.');
}
```

#### Pitfalls

1. **`ChatFollowup.title` does not exist** — only `prompt` field, no `title` in VS Code 1.131 type definitions.
2. **`slashCommands` may not be in types** — use `(participant as any).slashCommands` wrapped in try/catch.
3. **`vscode.chat` namespace may not exist** — entire chat feature is gated. Always wrap registration in try/catch.
4. **No tool call cards** — native chat doesn't support custom DOM. Tool status is silent (no intermediate UI feedback).
5. **No history persistence** — VS Code manages its own native chat history. Each `@Hermes` is independent.
6. **Rate limits** — 8 iterations × LLM calls per user message is slow on local models. Consider reducing iterations.

See `references/vscode-chat-participant.md` for the full implementation file.

#### Level 2: LM Chat Provider (Native Chat Session)

This is the mechanism that makes **"Hermes Agent"** appear as a selectable option in the Chat panel's `+` dropdown — alongside "New Chat" and "New Codex Session". It uses the `LanguageModelChatProvider` API combined with a `languageModelChatProviders` contribution point in `package.json`.

**Three things are needed:**

1. **`package.json` contribution** — declares the provider to VS Code's UI
2. **`HermesChatModelInformation`** — describes the model (id, name, capabilities, token limits)
3. **`HermesChatModelProvider`** — implements `LanguageModelChatProvider` with the tool loop

**`package.json` contribution:**

```json
"contributes": {
  "languageModelChatProviders": [
    {
      "vendor": "hermes",
      "icon": "$(comment-discussion)",
      "name": "Hermes Agent",
      "description": "AI coding assistant with full VS Code tool access"
    }
  ]
}
```

**Important:** The `vendor` string in `package.json` must match the first argument to `registerLanguageModelChatProvider('hermes', provider)`.

**Model information class:**

```typescript
class HermesChatModelInformation implements vscode.LanguageModelChatInformation {
  readonly id = 'hermes-agent';
  readonly name = 'Hermes Agent';
  readonly family = 'hermes';
  readonly version = '1.0.0';
  readonly maxInputTokens = 64000;
  readonly maxOutputTokens = 16384;
  readonly tooltip = 'Local or remote LLM via configurable endpoint';
  readonly capabilities = { toolCalling: false, imageInput: false };

  constructor() {
    const config = getLLMConfig();
    this.detail = `Model: ${config.model} @ ${config.endpoint}`;
  }
}
```

**Provider class skeleton:**

```typescript
import * as vscode from 'vscode';
import { MCPServer } from './mcp';
import { LLMConfig, LLMMessage, chatComplete } from './llm';
import { SYSTEM_PROMPT } from './config';

export class HermesChatModelProvider
  implements vscode.LanguageModelChatProvider<HermesChatModelInformation> {

  private _onDidChange = new vscode.EventEmitter<void>();
  readonly onDidChangeLanguageModelChatInformation = this._onDidChange.event;

  constructor(private readonly _mcpServer: MCPServer) {}

  provideLanguageModelChatInformation(
    _options: vscode.PrepareLanguageModelChatModelOptions,
    _token: vscode.CancellationToken
  ): vscode.ProviderResult<HermesChatModelInformation[]> {
    return [new HermesChatModelInformation()];
  }

  provideTokenCount(
    _model: HermesChatModelInformation,
    text: string | vscode.LanguageModelChatRequestMessage,
    _token: vscode.CancellationToken
  ): Thenable<number> {
    const content = typeof text === 'string' ? text : JSON.stringify(text);
    return Promise.resolve(Math.ceil(content.length / 4));
  }

  async provideLanguageModelChatResponse(
    _model: HermesChatModelInformation,
    messages: readonly vscode.LanguageModelChatRequestMessage[],
    _options: vscode.ProvideLanguageModelChatResponseOptions,
    progress: vscode.Progress<vscode.LanguageModelResponsePart>,
    token: vscode.CancellationToken
  ): Promise<void> {
    const config = getLLMConfig();
    const llmMessages: LLMMessage[] = [
      { role: 'system', content: SYSTEM_PROMPT },
      { role: 'system', content: buildToolDescriptions(this._mcpServer) },
    ];

    // Inject workspace context
    const wsContext = await gatherWorkspaceContext();
    if (wsContext) {
      llmMessages.push({ role: 'system', content: `## Current Workspace Context\\n${wsContext}` });
    }

    // Convert incoming messages
    for (const msg of messages) {
      const role = msg.role === vscode.LanguageModelChatMessageRole.User
        ? 'user' as const : 'assistant' as const;
      llmMessages.push({ role, content: msg.content.map(c => String(c)).join(' ') });
    }

    // Tool loop (same algorithm as webview + ChatParticipant)
    const MAX_ITERATIONS = 8;
    for (let i = 0; i < MAX_ITERATIONS; i++) {
      if (token.isCancellationRequested) return;
      const responseText = await chatComplete(llmMessages, config, abortSignalFromToken(token));
      const toolCalls = extractToolCalls(responseText || '');
      if (toolCalls.length === 0) {
        const cleanText = removeToolBlocks(responseText || '');
        if (cleanText) progress.report(new vscode.LanguageModelTextPart(cleanText));
        return;
      }
      for (const tc of toolCalls) {
        const toolEntry = this._mcpServer.getTool(tc.name);
        if (!toolEntry) {
          llmMessages.push({ role: 'user', content: `<error>Tool "${tc.name}" not found</error>` });
          continue;
        }
        try {
          const result = await toolEntry.handler(tc.arguments || {});
          const text = result.content?.[0]?.text || '(empty)';
          progress.report(new vscode.LanguageModelTextPart(\`\\n\\n> 🔧 **\${tc.name}** ✅\`));
          llmMessages.push({
            role: 'user',
            content: \`[Tool Result: \${tc.name}]\\n\\\`\\\`\\\`\\n\${text.slice(0, 8000)}\\n\\\`\\\`\\\``,
          });
        } catch (err) {
          llmMessages.push({ role: 'user', content: \`<error name="\${tc.name}">\${String(err)}</error>\` });
        }
      }
      if (llmMessages.length > 50) {
        const system = llmMessages.slice(0, 3);
        llmMessages.length = 0;
        llmMessages.push(...system, ...llmMessages.slice(-47));
      }
    }
  }
}
```

**Registration in `activate()`:**

```typescript
// NOTE: vscode.lm.registerLanguageModelChatProvider may not be in @types/vscode
// (it was added in VS Code 1.130+). Use (vscode.lm as any) cast + try/catch.

try {
  if (mcpServer) {
    context.subscriptions.push(
      (vscode.lm as any).registerLanguageModelChatProvider(
        'hermes',
        new HermesChatModelProvider(mcpServer)
      )
    );
  }
} catch (err) {
  console.warn('[Hermes] LM Chat Provider registration failed:', err);
}
```

**Key differences from Level 1 ChatParticipant:**

| Aspect | Level 1 (ChatParticipant) | Level 2 (LM Chat Provider) |
|--------|--------------------------|---------------------------|
| Trigger | `@Hermes` in any chat | **"Hermes Agent"** in `+` dropdown |
| UI | Shares VS Code's chat session | Dedicated session named "Hermes Agent" |
| History | Managed by VS Code | Managed by VS Code |
| Output API | `stream.markdown()` | `progress.report(new LanguageModelTextPart(...))` |
| Input format | `ChatRequest` with `prompt` + `references` | `LanguageModelChatRequestMessage[]` |
| Registration | `vscode.chat.createChatParticipant` | `vscode.lm.registerLanguageModelChatProvider` |
| Package.json | No contribution needed | `languageModelChatProviders` required |
| Type defs | Present in `@types/vscode` 1.85+ | May need `(as any)` cast in earlier defs |

**Pitfalls:**

1. **`registerLanguageModelChatProvider` may not be in your `@types/vscode`** — it was added around VS Code 1.130+. Use `(vscode.lm as any).registerLanguageModelChatProvider`.
2. **The `vendor` string must match** between `package.json` `languageModelChatProviders[].vendor` and the call `registerLanguageModelChatProvider('vendor', ...)`.
3. **`LanguageModelTextPart` requires `new`** — it's a class, not an interface. Use `new vscode.LanguageModelTextPart(text)`.
4. **No custom DOM** — you cannot render tool cards or custom UI. Only markdown text is supported.
5. **Tool loop is silent** — intermediate tool execution is invisible to the user. Only the final markdown and formatted status lines appear.
6. **Rate limits** — 8 iterations per request. Each iteration is a full LLM call, so on local models this may feel slow.
7. **TypeScript backtick nesting** — when using template literals inside template literals (e.g., constructing tool result messages), use `\\` escapes or concatenation to avoid nested backtick issues.

## Extension Manifest (package.json)

```json
{
  "activationEvents": ["onStartupFinished", "onCommand:hermes.openPanel"],
  "main": "./dist/extension.js",
  "contributes": {
    "commands": [
      { "command": "hermes.openPanel", "title": "Open Hermes Agent Panel" },
      { "command": "hermes.showMcpStatus", "title": "Show MCP Server Status" }
    ],
    "viewsContainers": { "panel": [{ "id": "hermes-chat", "title": "Hermes Agent" }] },
    "views": { "hermes-chat": [{ "type": "webview", "id": "hermes.chatPanel", "name": "Chat" }] },
    "configuration": {
      "title": "Hermes Agent",
      "properties": {
        "hermes.mcp.enabled": { "type": "boolean", "default": true },
        "hermes.mcp.port": { "type": "number", "default": 19999 },
        "hermes.llm.endpoint": { "type": "string", "default": "http://127.0.0.1:11434/v1" },
        "hermes.llm.model": { "type": "string", "default": "qwen2.5:7b" }
      }
    }
  }
}
```

## MCP Tool Categories

| Category | Tools |
|----------|-------|
| **Editor** | `editor_open_file`, `editor_get_content`, `editor_get_selection`, `editor_edit_file`, `editor_get_open_tabs`, `editor_close_tab`, `editor_get_diagnostics` |
| **Terminal** | `terminal_create`, `terminal_send`, `terminal_read` |
| **Files** | `file_read`, `file_write`, `file_create`, `file_delete`, `file_list_directory`, `file_search`, `file_search_content` |
| **Commands** | `command_execute`, `command_list_common` |
| **Workspace** | `workspace_get_folders`, `workspace_get_config`, `workspace_set_config`, `workspace_run_task` |
| **Debug** | `debug_start`, `debug_stop`, `debug_get_variables` |
| **Git** | `git_get_branches`, `git_get_status`, `git_command` |

## Hermes Desktop Configuration

Add to `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  vscode:
    url: "http://localhost:19999/mcp"
    timeout: 120
```

After restart, tools appear as `mcp_vscode_editor_open_file`, `mcp_vscode_terminal_send`, etc.

## Common Pitfalls

### 1. Extension Activation on Windows
VS Code uses lazy activation — extensions only start when one of their `activationEvents` fires. Without `"onStartupFinished"`, the MCP server won't start until the user runs a command.

**Fix:** Include `"onStartupFinished"` in `activationEvents`. Without this, manually trigger via `code -r -g <file>:<line>`.

**Force activation on Windows (when `onStartupFinished` doesn't fire due to cached manifest):**
```sh
# 1. Kill any existing MCP server process
taskkill /F /PID $(netstat -ano | grep 19999 | grep LISTENING | awk '{print $5}')

# 2. Install/update the extension
code --install-extension hermes-agent-vscode-1.0.0.vsix --force

# 3. Trigger extension host re-evaluation by opening a file
code -r -g package.json:1

# 4. If MCP server still doesn't start, force activation via command
# The `--command` flag is not officially documented but works on Windows
code --command hermes.openPanel

# 5. Verify MCP is running
curl http://127.0.0.1:19999/health
```

**Note:** The `--reload-window` flag passes through to Electron unhandled on Windows. Always use `code -r -g <file>` which triggers a proper window reload.

### 2. MCP Process Management During Development
When rebuilding and reinstalling the extension during development, the old MCP server process continues running on the same port until killed:

**Fix:** Always kill the MCP server process before reinstalling:
```sh
# Find the MCP server PID
PID=$(netstat -ano | grep ":19999 " | grep LISTENING | awk '{print $5}')
if [ -n "$PID" ]; then
  taskkill /F /PID $PID
  sleep 2  # Wait for port to free
fi
```

### 3. Verify Installation by Comparing Dist Files
After reinstalling an extension, VS Code's extension host may still have the old code loaded if it cached the previous manifest. Verify that the installed version matches the source:

```sh
# Compare installed code with built code
diff dist/extension.js ~/.vscode/extensions/<publisher>.extension-<version>/dist/extension.js

# Compare webview media files
diff dist/webview/media/chat.js ~/.vscode/extensions/<publisher>.extension-<version>/dist/webview/media/chat.js
```

Zero diff output confirms the installed extension is the latest build.

### 4. MCP Requires initialize Before tools/list
The `tools/list` handler checks an `initialized` flag set during `initialize`. Without initialization, the server returns an error. The `/health` endpoint bypasses this for diagnostics.

Connect via SSE (recommended) or direct POST:
```sh
# Direct POST — must initialize first
curl -X POST http://127.0.0.1:19999/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0.0"}}}'

# Then list tools
curl -X POST http://127.0.0.1:19999/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}'
```

### 3. MCP Requires initialize Before tools/list
The `tools/list` handler checks an `initialized` flag set during `initialize`. Without initialization, the server returns an error. The `/health` endpoint bypasses this for diagnostics.

### 4. vscode Module Must Be External in Bundle
esbuild must have `external: ['vscode']`. The `vscode` module only exists in the extension host process. Bundling it produces a 0-size placeholder.

### 5. Webview CSP Requirements
VS Code webviews have strict CSP. Script sources must use `webview.asWebviewUri()` paths.

```html
<meta http-equiv="Content-Security-Policy"
  content="default-src 'none'; style-src ${cspSource} 'unsafe-inline'; script-src ${cspSource}; font-src ${cspSource};">
```

### 6. Terminal Output Not Readable via API
VS Code's extension API does not expose terminal output. Redirect command output to files, or use shell integration (limited availability).

### 7. Debug API Evolution
`vscode.debug.getConfiguration()` was removed. Use `workbench.action.debug.start` command as fallback.

### 8. Separate Webview IPC Message Types
Inbound messages (webview→host) have a narrow union type; outbound (host→webview) uses a generic `string` type since the webview receives many message types.

```typescript
interface WebviewInMessage { type: 'chat' | 'abort' | 'getModels' | 'getConfig' | 'setConfig' | 'openFile' | 'clearConversation'; payload?: unknown; }
interface WebviewOutMessage { type: string; payload?: unknown; }
```

## Verification Checklist

### MCP Server
- [ ] `tsc --noEmit` passes with zero errors
- [ ] `node esbuild.js` produces extension.js + mcp-server.js bundles
- [ ] `npx vsce package` produces a valid .vsix
- [ ] Extension installs via `code --install-extension <vsix>`
- [ ] After VS Code reload, port responds: `curl http://127.0.0.1:19999/health`
- [ ] MCP initialize + tools/list returns all registered tools (~29)
- [ ] At least one tool call returns real VS Code data (`workspace_get_folders`)
- [ ] Webview panel opens and shows the chat UI

### Tool Loop
- [ ] User message triggers `_runToolLoop()` (not just a direct LLM call)
- [ ] System prompt includes tool descriptions from `buildToolDescriptions()`
- [ ] LLM response with a ` ` ` tool ` ` ` block triggers tool execution via MCPServer
- [ ] Tool call card appears in webview (spinning → done/error)
- [ ] Tool result feeds back into next LLM iteration
- [ ] Final response (no tool blocks) streams to webview with clean text
- [ ] Stop button and Escape key abort mid-generation
- [ ] Max iteration limit (10) prevents infinite loops

### Conversation & Context
- [ ] Chat history persists across VS Code window reloads
- [ ] Open file / selection / diagnostics injected into system prompt
- [ ] Git branch and workspace folders included in context
- [ ] Input disabled during tool loop, re-enabled on completion
