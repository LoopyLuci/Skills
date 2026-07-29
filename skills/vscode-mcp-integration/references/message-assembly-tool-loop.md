# Message Assembly & Tool Loop Patterns

## Message Assembly Order

The tool-loop LLM receives messages in this exact order:

```
1. System prompt                  (role: system)
2. Tool descriptions              (role: system — from buildToolDescriptions())
3. Workspace context              (role: system — from _gatherContext())
4. Conversation history           (mixed roles — last 30 messages)
```

This ordering matters: tool descriptions must come AFTER the system prompt (so they override any generic instruction) but BEFORE any history (so the LLM knows what tools exist from the first turn).

### Implementation

```typescript
private async _buildMessages(): Promise<LLMMessage[]> {
  const context = await this._gatherContext();
  const toolDesc = buildToolDescriptions(this._mcpServer);

  const messages: LLMMessage[] = [
    { role: 'system', content: SYSTEM_PROMPT },
    { role: 'system', content: toolDesc },
  ];

  if (context) {
    messages.push({ role: 'system', content: `## Current Workspace Context\n${context}` });
  }

  // Last 30 messages keeps token budget under control
  const history = this._messages.slice(-30);
  for (const msg of history) {
    messages.push(msg);
  }

  return messages;
}
```

### Token Budget Calculation

| Component | Approx tokens | Notes |
|-----------|--------------|-------|
| System prompt | 300 | Fixed |
| Tool descriptions | 500–1500 | 29 tools × ~50t each |
| Workspace context | 100–300 | Variable by open files/diags |
| History (30 msgs) | 2000–6000 | Depends on message length |
| **Total** | **~2900–8100** | Well within 32K context |

## Response Splitting

When the LLM returns text with embedded tool call blocks, you need to separate them:

```typescript
/**
 * Split LLM response text into text and tool call parts.
 * Preserves ordering so you can reconstruct the conversation.
 */
private _splitByToolBlocks(text: string): Array<{ type: 'text' | 'tool'; content: string }> {
  const parts: Array<{ type: 'text' | 'tool'; content: string }> = [];
  const regex = /(```tool\n?[\s\S]*?```)/g;
  let lastIndex = 0;
  let match: RegExpExecArray | null;
  while ((match = regex.exec(text)) !== null) {
    if (match.index > lastIndex) {
      parts.push({ type: 'text', content: text.slice(lastIndex, match.index) });
    }
    parts.push({ type: 'tool', content: match[1] });
    lastIndex = match.index + match[1].length;
  }
  if (lastIndex < text.length) {
    parts.push({ type: 'text', content: text.slice(lastIndex) });
  }
  return parts;
}
```

### Usage in the Loop

After extracting tool calls, the non-tool text parts become the assistant's message in history:

```typescript
const textParts = this._splitByToolBlocks(responseText);
const assistantText = textParts
  .filter(p => p.type === 'text')
  .map(p => p.content)
  .join('')
  .trim();

if (assistantText) {
  this._messages.push({ role: 'assistant', content: assistantText });
}
```

The tool results are pushed as `role: 'user'` with a clear label:

```typescript
// On success:
this._messages.push({
  role: 'user',
  content: `[Tool Result: ${name}]\n\`\`\`\n${resultText.slice(0, 8000)}\`\`\``,
});

// On error:
this._messages.push({
  role: 'user',
  content: `<tool_error name="${name}">\n${errorMsg}\n</tool_error>`,
});
```

This `role: 'user'` for tool results is intentional — it prevents the LLM from treating them as its own output and encourages it to reason about the result.

## History Truncation

Prevent context overflow by capping history length:

```typescript
if (this._messages.length > 60) {
  this._messages = this._messages.slice(-50);
}
```

And when persisting:

```typescript
private _saveMessages(): void {
  const toSave = this._messages.slice(-100);  // Keep last 100 for reload
  this._context.globalState.update('hermes.conversation.v1', toSave);
}
```

## Streaming the Final Response

After the tool loop converges (no more tool blocks), stream the clean text to the webview in chunks for smooth animation:

```typescript
const cleanText = removeToolBlocks(responseText);
if (cleanText) {
  this._messages.push({ role: 'assistant', content: cleanText });
  this._postMessage({ type: 'startStream', payload: {} });

  // ~20 chunks gives smooth typewriter effect
  const chunkSize = Math.max(Math.ceil(cleanText.length / 20), 1);
  for (let i = 0; i < cleanText.length; i += chunkSize) {
    this._postMessage({
      type: 'streamChunk',
      payload: { content: cleanText.slice(i, i + chunkSize) },
    });
  }
  this._postMessage({ type: 'endStream', payload: {} });
}
```

The webview appends each chunk to a `streamingMessage` div:

```javascript
function startStreamingMessage() {
  const div = document.createElement('div');
  div.className = 'message assistant';
  div.id = 'streamingMessage';
  div.innerHTML = '<p></p>';
  messagesEl.appendChild(div);
  scrollToBottom();
}

function appendToStream(text) {
  currentAssistantContent += text;
  const p = currentAssistantEl.querySelector('p');
  p.innerHTML = renderMarkdown(currentAssistantContent);
  scrollToBottom();
}
```

## Tool Result Format for LLM Consumption

The format used to inject tool results back into the message stream affects how well the LLM uses them:

| Format | LLM Quality | Notes |
|--------|-------------|-------|
| `[Tool Result: name]\n\`\`\`\n...\`\`\`` | Good | Clear delimiter, Code blocks preserve formatting |
| `<tool_result name="x">...</tool_result>` | Medium | HTML-like tags, but may confuse some LLMs into thinking it's real HTML |
| `The tool "x" returned: ...` (narrative) | Poor | Blends into the conversation, LLM may ignore it |
| Raw JSON | Poor | Wastes tokens on structure the LLM doesn't need |
