# WebBuilder Visual Editor Patterns

This reference covers the visual drag-and-drop editor implementation patterns.

## Architecture

The editor uses a layered architecture:
- **EditorProvider** (React Context) — state management, undo/redo, history
- **DndContext** (@dnd-kit) — drag-and-drop from palette to canvas, section reordering
- **LivePreview** — iframe-based preview of generated code
- **DeployModal** — deployment target selection and flow
- **CollaborationPanel** — multi-user presence and session management
- **CommandPalette** — Cmd+K fuzzy search for all actions
- **ProjectManager** — save/load projects to localStorage

## State Management

```typescript
interface EditorState {
  sections: Section[];
  selectedSectionId: string | null;
  viewport: 'mobile' | 'tablet' | 'desktop';
  zoom: number;
  history: Section[][];
  historyIndex: number;
}
```

The EditorProvider wraps the entire editor and exposes:
- `addSection`, `removeSection`, `updateSection`
- `selectSection`, `undo`, `redo`
- `setViewport`, `setZoom`
- `saveCurrentProject`, `loadProject`

## Drag and Drop Pattern

```typescript
// Using @dnd-kit for both palette-to-canvas and section reordering
const sensors = useSensors(
  useSensor(PointerSensor, { activationConstraint: { distance: 8 } }),
  useSensor(KeyboardSensor, { coordinateGetter: sortableKeyboardCoordinates })
);

// Palette items have type as ID
const componentPalette = [
  { type: 'hero', name: 'Hero Section', icon: '🖼️', category: 'Layout' },
  // ...
];

// Drag end handles both palette drops and reordering
const handleDragEnd = (event: DragEndEvent) => {
  const { active, over } = event;
  if (!over) {
    // Dropped outside — add from palette
    const paletteItem = componentPalette.find(c => c.type === active.id);
    if (paletteItem) addSection(paletteItem.type, paletteItem.name);
    return;
  }
  if (active.id !== over.id) {
    // Reorder sections
    // ...
  }
};
```

## Live Preview Pattern

```typescript
// Generate React code from sections
function generateReactCode(sections: any[]): string {
  const componentCode: string[] = [];
  for (const section of sections) {
    // Map section types to component code
    if (section.component === 'hero') {
      componentCode.push(`<HeroSection title="${section.props.title}" ... />`);
    }
    // ...
  }
  return `<div>${componentCode.join('\n')}</div>`;
}

// Render in iframe
<iframe srcDoc={html} sandbox="allow-scripts" />
```

## Keyboard Shortcuts

```typescript
useKeyboardShortcuts({
  'mod+z': handleUndo,
  'mod+shift+z': handleRedo,
  'mod+s': handleSave,
  'mod+d': handleDuplicate,
  'mod+k': () => setIsPaletteOpen(true),
  '1': () => setViewport('mobile'),
  '2': () => setViewport('tablet'),
  '3': () => setViewport('desktop'),
  'delete': handleDelete,
  'escape': () => selectSection(null),
});
```

## Command Palette

```typescript
const commands = [
  ...componentPalette.map(c => ({
    id: `add-${c.type}`,
    label: `Add ${c.name}`,
    category: 'Components',
    action: () => handleComponentClick(c.type, c.name),
  })),
  { id: 'save', label: 'Save Project', shortcut: '⌘S', action: handleSave },
  // ...
];
```

## Split View Layout

```typescript
// Canvas + Preview side-by-side
<div className="flex-1 flex overflow-auto">
  <div className={isPreviewOpen ? 'w-1/2' : 'flex-1'}>
    {/* Visual canvas */}
  </div>
  {isPreviewOpen && (
    <div className="w-1/2 border-l border-border">
      <LivePreview />
    </div>
  )}
</div>
```

## Pitfalls

1. **Stale element indices**: @dnd-kit indices are only valid until next capture. Re-capture before acting.

2. **Iframe sandboxing**: Use `sandbox="allow-scripts"` for live preview. Styles must be inline or in the srcDoc.

3. **Duplicate page detection**: Next.js detects both `_app.tsx` and `_app.js` as duplicates. Remove generated `.js`/`.d.ts` files from `src/` after build.

4. **TypeScript strictness in generated code**: Use `[key: string]: any` index signatures on component props to allow arbitrary props.

5. **History management**: Deep clone sections before pushing to history to avoid mutation issues.

6. **localStorage serialization**: Section objects must be JSON-serializable for project persistence.

## Verification

- [ ] Drag from palette to canvas works
- [ ] Section reordering via drag works
- [ ] Live preview updates in real-time
- [ ] Keyboard shortcuts work
- [ ] Command palette opens with Cmd+K
- [ ] Projects save/load from localStorage
- [ ] Undo/redo works correctly
- [ ] Deploy modal opens and shows targets
- [ ] Collaboration panel shows users
