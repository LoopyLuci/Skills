# VS Code ChatParticipant — Full Implementation Pattern

This reference documents the complete `chat-participant.ts` implementation for registering `@Hermes` in VS Code's native Chat view. See the SKILL.md section "7. Native Chat Integration via ChatParticipant API" for the overview and design rationale.

## Full Source: `src/chat-participant.ts`

```typescript
import * as vscode from 'vscode';
import { MCPServer, MCPTool } from './mcp';
import { LLMConfig, LLMMessage, chatComplete } from './llm';
import { SYSTEM_PROMPT } from './config';

// ─── Tool Call Parsing ─────────────────────────────────────

interface ParsedToolCall {
  name: string;
  arguments: Record<string, unknown>;
}

function extractToolCalls(text: string): ParsedToolCall[] {
  const calls: ParsedToolCall[] = [];
  const pattern = /```tool\n?([\s\S]*?)```/g;
  let match: RegExpExecArray | null;
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
  return text.replace(/```tool\n?[\s\S]*?```/g, '').trim();
}

// ─── Tool Descriptions ─────────────────────────────────────

function buildToolDescriptions(server: MCPServer): string {
  const tools = server.getAllTools();
  if (tools.length === 0) return '';
  const lines = tools.map((t: MCPTool) => {
    const props = (t.inputSchema.properties || {}) as Record<string, { description?: string; type?: string }>;
    const args = Object.keys(props).length > 0
      ? Object.entries(props).map(([k, v]) => `    ${k} (${v.type || 'any'}): ${v.description || ''}`).join('\n')
      : '    (no arguments)';
    return `- **${t.name}**: ${t.description}\n${args}`;
  });
  return `## Available Tools\n\nYou have access to ${tools.length} tools. Call one by embedding:\n\n\`\`\`tool\n{"name":"tool_name","arguments":{...}}\n\`\`\`\n\n${lines.join('\n\n')}`;
}

// ─── Context Gathering ─────────────────────────────────────

async function gatherWorkspaceContext(): Promise<string> {
  const parts: string[] = [];
  try {
    const editor = vscode.window.activeTextEditor;
    if (editor) {
      parts.push(`**Active file:** \`${editor.document.fileName}\` (${editor.document.languageId})`);
      if (!editor.selection.isEmpty) {
        parts.push(`**Selection:** ${editor.document.getText(editor.selection).slice(0, 200)}`);
      }
    }
    const tabs = vscode.window.tabGroups.all.flatMap(group =>
      group.tabs.filter(t => t.input instanceof vscode.TabInputText)
        .map(t => (t.input as vscode.TabInputText).uri.fsPath)
    );
    if (tabs.length > 0) {
      parts.push(`**Open tabs:** ${tabs.slice(0, 6).join(', ')}${tabs.length > 6 ? ` +${tabs.length - 6} more` : ''}`);
    }
    const folders = vscode.workspace.workspaceFolders;
    if (folders?.length) {
      parts.push(`**Workspace:** ${folders.map(f => f.uri.fsPath).join(', ')}`);
    }
  } catch { /* fail gracefully */ }
  return parts.join('\n');
}

// ─── Config ────────────────────────────────────────────────

function getLLMConfig(): LLMConfig {
  const config = vscode.workspace.getConfiguration('hermes');
  return {
    endpoint: config.get<string>('llm.endpoint') || 'http://127.0.0.1:11434/v1',
    model: config.get<string>('llm.model') || 'qwen2.5:7b',
    apiKey: config.get<string>('llm.apiKey') || undefined,
  };
}

// ─── CancellationToken → AbortSignal ───────────────────────

function abortSignalFromToken(token: vscode.CancellationToken): AbortSignal {
  const controller = new AbortController();
  token.onCancellationRequested(() => controller.abort());
  return controller.signal;
}

// ─── Registration ──────────────────────────────────────────

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
        { prompt: 'Generate tests' },
      ];
    },
  };

  try {
    (participant as any).slashCommands = [
      { name: 'help', description: 'Show available tools and capabilities' },
      { name: 'explain', description: 'Explain the selected code or current file' },
      { name: 'fix', description: 'Find and fix errors in the workspace' },
      { name: 'refactor', description: 'Suggest refactoring improvements' },
      { name: 'test', description: 'Generate tests for selected code' },
    ];
  } catch { /* older VS Code — slash commands not supported */ }

  context.subscriptions.push(participant);
  return participant;
}

// ─── Request Handler ───────────────────────────────────────

async function handleRequest(
  request: vscode.ChatRequest,
  stream: vscode.ChatResponseStream,
  token: vscode.CancellationToken,
  mcpServer: MCPServer
): Promise<void> {
  const config = getLLMConfig();
  const llmSignal = abortSignalFromToken(token);
  const MAX_ITERATIONS = 8;

  // Build messages
  let messages: LLMMessage[] = [
    { role: 'system', content: SYSTEM_PROMPT },
    { role: 'system', content: buildToolDescriptions(mcpServer) },
  ];

  const wsContext = await gatherWorkspaceContext();
  if (wsContext) {
    messages.push({ role: 'system', content: `## Current Workspace Context\n${wsContext}` });
  }

  // File references (#file:path)
  if (request.references?.length) {
    const fileContents: string[] = [];
    for (const ref of request.references) {
      if (ref.value instanceof vscode.Uri) {
        try {
          const doc = await vscode.workspace.openTextDocument(ref.value);
          fileContents.push(`### ${ref.value.fsPath}\n\`\`\`${doc.languageId}\n${doc.getText()}\n\`\`\``);
        } catch { /* skip */ }
      }
    }
    if (fileContents.length > 0) {
      messages.push({ role: 'system', content: `## Referenced Files\n${fileContents.join('\n\n')}` });
    }
  }

  // Handle command + prompt
  messages.push({ role: 'user', content: ((request.command || '') + ' ' + (request.prompt || '')).trim() });

  // Tool loop
  for (let i = 0; i < MAX_ITERATIONS; i++) {
    if (token.isCancellationRequested) return;

    const responseText = await chatComplete(messages, config, llmSignal);
    if (!responseText) { stream.markdown('_(empty response)_'); return; }

    const toolCalls = extractToolCalls(responseText);

    if (toolCalls.length === 0) {
      const cleanText = removeToolBlocks(responseText);
      if (cleanText) stream.markdown(cleanText);
      return;
    }

    // Split text and tool blocks before executing
    const textParts = splitByToolBlocks(responseText);
    const assistantText = textParts.filter(p => p.type === 'text').map(p => p.content).join('').trim();
    if (assistantText) messages.push({ role: 'assistant', content: assistantText });

    for (const tc of toolCalls) {
      if (token.isCancellationRequested) return;
      const toolEntry = mcpServer.getTool(tc.name);
      if (!toolEntry) {
        messages.push({ role: 'user', content: `<error>Tool "${tc.name}" not found</error>` });
        continue;
      }
      try {
        const result = await toolEntry.handler(tc.arguments || {});
        const text = result.content?.[0]?.text ||
          result.content?.map((c: { text?: string }) => c.text || '').join('\n') || '(empty)';
        messages.push({ role: 'user', content: `[Tool Result: ${tc.name}]\n\`\`\`\n${text.slice(0, 8000)}\n\`\`\`` });
      } catch (err: unknown) {
        const errMsg = err instanceof Error ? err.message : String(err);
        messages.push({ role: 'user', content: `<error name="${tc.name}">${errMsg}</error>` });
      }
    }

    if (messages.length > 50) messages = [...messages.slice(0, 3), ...messages.slice(-47)];
  }

  stream.markdown('\n\n> ⚠️ Reached maximum tool iterations for one request.');
}

// ─── Helpers ───────────────────────────────────────────────

function splitByToolBlocks(text: string): Array<{ type: 'text' | 'tool'; content: string }> {
  const parts: Array<{ type: 'text' | 'tool'; content: string }> = [];
  const regex = /(```tool\n?[\s\S]*?```)/g;
  let lastIndex = 0;
  let match: RegExpExecArray | null;
  while ((match = regex.exec(text)) !== null) {
    if (match.index > lastIndex) parts.push({ type: 'text', content: text.slice(lastIndex, match.index) });
    parts.push({ type: 'tool', content: match[1] });
    lastIndex = match.index + match[1].length;
  }
  if (lastIndex < text.length) parts.push({ type: 'text', content: text.slice(lastIndex) });
  return parts;
}

const participantSlashCommands = [
  { name: 'help', description: 'Show available tools and capabilities' },
  { name: 'explain', description: 'Explain the selected code or current file' },
  { name: 'fix', description: 'Find and fix errors in the workspace' },
  { name: 'refactor', description: 'Suggest refactoring improvements' },
  { name: 'test', description: 'Generate tests for selected code' },
];
```

## Wiring in extension.ts

```typescript
// Import
import { registerChatParticipant } from './chat-participant';

// In activate(), after MCP server is created:
try {
  if (mcpServer) {
    registerChatParticipant(context, mcpServer);
  }
} catch (err) {
  console.warn('[Hermes Agent] Chat participant registration failed:', err);
}
```

## Verification

- [ ] TypeScript compiles: `npx tsc --noEmit` — zero errors
- [ ] Extension builds with esbuild — chat-participant.ts is bundled into extension.js
- [ ] After VS Code reload, open Chat view (Ctrl+Shift+I)
- [ ] Type `@Hermes` — the participant selector should show Hermes
- [ ] Type `@Hermes what can you do?` — response shows capabilities
- [ ] Native chat view shows follow-up buttons after response
- [ ] Esc during generation stops the tool loop
