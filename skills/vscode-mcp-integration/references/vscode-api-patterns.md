# VS Code API Implementation Patterns for MCP Tools

This reference documents the exact VS Code API calls used by each MCP tool category. Use these patterns when implementing tool handlers.

## Editor Tools

### Open File
```typescript
const uri = vscode.Uri.file(filePath);
await vscode.window.showTextDocument(uri, { preview: false });
```

### Get Active Editor Content
```typescript
const editor = vscode.window.activeTextEditor;
if (!editor) return null;
return {
  content: editor.document.getText(),
  language: editor.document.languageId,
  fileName: editor.document.fileName,
};
```

### Get Selection
```typescript
const editor = vscode.window.activeTextEditor;
if (!editor) return null;
return editor.document.getText(editor.selection);
```

### Edit File (Targeted Text Replacements)
```typescript
const uri = vscode.Uri.file(filePath);
const doc = await vscode.workspace.openTextDocument(uri);
const edit = new vscode.WorkspaceEdit();
for (const e of edits) {
  const range = new vscode.Range(e.startLine, e.startChar, e.endLine, e.endChar);
  edit.replace(uri, range, e.newText);
}
await vscode.workspace.applyEdit(edit);
```

### Get Open Tabs
```typescript
return vscode.window.tabGroups.all.flatMap(group =>
  group.tabs
    .filter(tab => tab.input instanceof vscode.TabInputText)
    .map(tab => {
      const input = tab.input as vscode.TabInputText;
      return {
        fileName: input.uri.fsPath,
        language: path.extname(input.uri.fsPath).slice(1) || 'plaintext',
        isDirty: tab.isDirty,
      };
    })
);
```

### Close Tab
```typescript
const uri = vscode.Uri.file(filePath);
for (const group of vscode.window.tabGroups.all) {
  for (const tab of group.tabs) {
    if (tab.input instanceof vscode.TabInputText && tab.input.uri.fsPath === uri.fsPath) {
      await vscode.window.tabGroups.close(tab);
      return;
    }
  }
}
```

### Get Diagnostics
```typescript
const all = vscode.languages.getDiagnostics();
for (const [uri, diagnostics] of all) {
  for (const d of diagnostics) {
    results.push({
      file: uri.fsPath,
      line: d.range.start.line + 1,
      message: d.message,
      severity: d.severity === vscode.DiagnosticSeverity.Error ? 'error'
        : d.severity === vscode.DiagnosticSeverity.Warning ? 'warning'
        : d.severity === vscode.DiagnosticSeverity.Information ? 'info' : 'hint',
    });
  }
}
```

## Terminal Tools

### Create / Get Terminal
```typescript
let term = vscode.window.terminals.find(t => t.name === termName);
if (!term) {
  term = vscode.window.createTerminal(termName);
}
return { name: termName, send(text: string) { term!.sendText(text); }, show() { term!.show(); } };
```

### Read Terminal Output
**Not directly supported by VS Code API.** Use workarounds:
- Redirect output to files: `command > /tmp/output.log`
- Use VS Code shell integration API (limited to VS Code 1.85+ with specific shells)

```typescript
// Fallback message:
return '(Terminal output not directly readable through VS Code API. Use file_read on log files, or redirect output to files.)';
```

## File System Tools

All file operations use `vscode.workspace.fs` (the VS Code file system API):

```typescript
// Read
const content = await vscode.workspace.fs.readFile(uri);
return new TextDecoder().decode(content);

// Write
await vscode.workspace.fs.writeFile(uri, new TextEncoder().encode(content));

// Create (empty file)
await vscode.workspace.fs.writeFile(uri, new Uint8Array());

// Delete
try { await vscode.workspace.fs.delete(uri, { useTrash: true }); }
catch { await vscode.workspace.fs.delete(uri, { useTrash: false }); }

// List directory
const entries = await vscode.workspace.fs.readDirectory(uri);
return entries.map(([name, type]) =>
  type === vscode.FileType.Directory ? name + '/' : name
);

// Search files (by name pattern)
const pattern = new vscode.RelativePattern(searchDir || workspaceRoot, query);
const uris = await vscode.workspace.findFiles(pattern, undefined, 200);
return uris.map(uri => ({ file: uri.fsPath, line: 0, match: path.basename(uri.fsPath) }));
```

## Command Tools

### Execute Any VS Code Command
```typescript
await vscode.commands.executeCommand(commandId, ...args);
```

### Useful VS Code Command IDs

| Category | Command ID | Description |
|----------|-----------|-------------|
| Files | `workbench.action.files.save` | Save current file |
| Files | `workbench.action.files.saveAll` | Save all modified files |
| Editor | `editor.action.formatDocument` | Format document |
| Editor | `editor.action.organizeImports` | Organize imports |
| Editor | `editor.action.rename` | Rename symbol |
| Editor | `editor.action.goToDefinition` | Go to definition |
| Editor | `editor.action.sourceAction` | Show refactoring actions |
| Navigation | `workbench.action.navigateBack` | Navigate back |
| Navigation | `workbench.action.quickOpen` | Quick open file |
| Terminal | `workbench.action.terminal.new` | New terminal |
| Terminal | `workbench.action.terminal.toggleTerminal` | Toggle terminal |
| Debug | `workbench.action.debug.start` | Start debugging |
| Debug | `workbench.action.debug.stop` | Stop debugging |
| Debug | `workbench.action.debug.run` | Run without debug |
| View | `workbench.view.explorer` | Show explorer |

## Workspace Tools

### Get Workspace Folders
```typescript
return (vscode.workspace.workspaceFolders || []).map(f => f.uri.fsPath);
```

### Get/Set Configuration
```typescript
// Get
return vscode.workspace.getConfiguration().get(key);

// Set
await vscode.workspace.getConfiguration().update(key, value, vscode.ConfigurationTarget.Workspace);
```

### Run Task
```typescript
const tasks = await vscode.tasks.fetchTasks();
const task = tasks.find(t => t.name === taskName);
if (!task) return `Task not found: "${taskName}"`;

const disposable = vscode.tasks.onDidEndTaskProcess(e => {
  if (e.execution.task.name === taskName) {
    disposable.dispose();
    resolve(e.exitCode === 0 ? `Task completed` : `Task failed (exit ${e.exitCode})`);
  }
});
vscode.tasks.executeTask(task);
```

## Debug Tools

### Start Debugging
```typescript
// With explicit config:
const folder = vscode.workspace.workspaceFolders?.[0];
return vscode.debug.startDebugging(folder, config as vscode.DebugConfiguration)
  .then(() => true, () => false);

// Fallback (no getConfiguration() available in new VS Code):
await vscode.commands.executeCommand('workbench.action.debug.start');
```

### Stop Debugging
```typescript
vscode.debug.stopDebugging();
```

### Get Debug Variables (when paused at breakpoint)
```typescript
const session = vscode.debug.activeDebugSession;
if (!session) return {};
const stack = await session.customRequest('stackTrace', { threadId: 1 });
const scopes = await session.customRequest('scopes', { frameId: stack.stackFrames[0].id });
const variables: Record<string, string> = {};
for (const scope of scopes.scopes.slice(0, 3)) {
  const vars = await session.customRequest('variables', { variablesReference: scope.variablesReference });
  for (const v of vars.variables.slice(0, 30)) {
    variables[v.name] = String(v.value || '');
  }
}
return variables;
```

## Git/SCM Tools

Use the VS Code Git extension API (not child_process git):

```typescript
const gitExtension = vscode.extensions.getExtension('vscode.git')?.exports;
const api = gitExtension?.getAPI(1);
if (!api?.repositories?.[0]) return [];

const repo = api.repositories[0];

// Status
for (const change of repo.state.workingTreeChanges) {
  status.push({ file: change.uri.fsPath, status: 'M' });
}
for (const change of repo.state.indexChanges) {
  status.push({ file: change.uri.fsPath, status: 'M' });
}

// Branches
const branches = repo.state.refs?.filter((r: { type: number; name: string }) => r.type === 1) || [];

// Arbitrary git command
const result = await repo.run(args);
```

## LLM Streaming Client

Use `fetch` with `ReadableStream` for streaming from OpenAI-compatible endpoints:

```typescript
const response = await fetch(url, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${apiKey}` },
  body: JSON.stringify({ model, messages, stream: true, temperature: 0.7, max_tokens: 16384 }),
  signal,
});

const reader = response.body!.getReader();
const decoder = new TextDecoder();
let buffer = '';

while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  buffer += decoder.decode(value, { stream: true });
  for (const line of buffer.split('\n')) {
    if (line.startsWith('data: ')) {
      const data = line.slice(6);
      if (data === '[DONE]') return;
      const parsed = JSON.parse(data);
      const content = parsed.choices?.[0]?.delta?.content || '';
      if (content) yield { content, done: false };
    }
  }
}
```

## esbuild Configuration for VS Code Extensions

```javascript
const config = {
  entryPoints: ['src/extension.ts', 'src/mcp-server.ts'],
  bundle: true,
  outdir: 'dist',
  external: ['vscode'],                    // vscode module is runtime-only
  format: 'cjs',
  platform: 'node',
  target: 'node18',
  sourcemap: true,
  metafile: true,                           // reports output sizes
  keepNames: true,                          // preserves function names for stack traces
};

// Copy non-code assets (webview media) separately
const mediaSrc = 'src/webview/media';
const mediaDst = 'dist/webview/media';
fs.cpSync(mediaSrc, mediaDst, { recursive: true });
```

## Known API Quirks

1. **`vscode.debug.startDebugging`** requires 2 arguments (folder + nameOrConfiguration). The standalone overload was removed.
2. **`vscode.debug.getConfiguration`** does not exist — removed in VS Code 1.120+. Use `workbench.action.debug.start` command instead.
3. **`vscode.TabInputText`** is the class for text editor tabs. Use `instanceof` check before casting.
4. **`vscode.workspace.fs.readDirectory`** returns `[string, FileType][]` — FileType enum distinguishes file vs directory.
5. **Git extension API** (`vscode.extensions.getExtension('vscode.git')`) returns `undefined` if Git is disabled or unavailable.
6. **Diagnostics severity** is an enum (`vscode.DiagnosticSeverity`): Error=0, Warning=1, Information=2, Hint=3.
7. **`TextDecoder`/`TextEncoder`** are available globally in VS Code's Node.js environment (not from `util`).
