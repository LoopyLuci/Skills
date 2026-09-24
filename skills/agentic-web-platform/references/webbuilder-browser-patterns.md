# WebBuilder Browser-Side Patterns

This reference covers patterns for browser-side state management, persistence, and editor interactions.

## localStorage Project Persistence

```typescript
const STORAGE_KEY = 'webbuilder-projects';

export interface SavedProject {
  id: string;
  name: string;
  description: string;
  sections: Section[];
  viewport: 'desktop' | 'tablet' | 'mobile';
  createdAt: string;
  updatedAt: string;
}

export function getSavedProjects(): SavedProject[] {
  if (typeof window === 'undefined') return [];
  try {
    const data = localStorage.getItem(STORAGE_KEY);
    return data ? JSON.parse(data) : [];
  } catch { return []; }
}

export function saveProject(project: SavedProject): void {
  const projects = getSavedProjects();
  const existing = projects.findIndex(p => p.id === project.id);
  if (existing >= 0) {
    projects[existing] = { ...project, updatedAt: new Date().toISOString() };
  } else {
    projects.push(project);
  }
  localStorage.setItem(STORAGE_KEY, JSON.stringify(projects));
}

export function deleteProject(id: string): void {
  const projects = getSavedProjects().filter(p => p.id !== id);
  localStorage.setItem(STORAGE_KEY, JSON.stringify(projects));
}
```

## Editor Context with Persistence

```typescript
interface EditorContextType {
  state: EditorState;
  isLoading: boolean;
  addSection: (component: string, name: string) => void;
  removeSection: (id: string) => void;
  updateSection: (id: string, updates: Partial<Section>) => void;
  selectSection: (id: string | null) => void;
  undo: () => void;
  redo: () => void;
  setViewport: (viewport: 'desktop' | 'tablet' | 'mobile') => void;
  setZoom: (zoom: number) => void;
  saveCurrentProject: (name: string, description: string) => void;
  loadProject: (project: SavedProject) => void;
  currentProjectId: string | null;
}

const saveCurrentProject = useCallback((name: string, description: string) => {
  const project: SavedProject = {
    id: currentProjectId || `project_${Date.now()}`,
    name, description,
    sections: state.sections,
    viewport: state.viewport,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  };
  saveProject(project);
  setCurrentProjectId(project.id);
  showToast('success', `Project "${name}" saved`);
}, [state.sections, state.viewport, currentProjectId]);

const loadProject = useCallback((project: SavedProject) => {
  setState({
    sections: project.sections,
    selectedSectionId: null,
    viewport: project.viewport,
    zoom: 1,
    history: [project.sections],
    historyIndex: 0,
  });
  setCurrentProjectId(project.id);
  showToast('success', `Project "${project.name}" loaded`);
}, []);
```

## Keyboard Shortcuts Hook

```typescript
import { useEffect, useCallback, useRef } from 'react';

type ShortcutHandler = () => void;

interface ShortcutMap {
  [key: string]: ShortcutHandler;
}

function getPlatformKey(e: KeyboardEvent): string {
  const parts: string[] = [];
  if (e.ctrlKey || e.metaKey) parts.push('mod');
  if (e.shiftKey) parts.push('shift');
  if (e.altKey) parts.push('alt');
  parts.push(e.key.toLowerCase());
  return parts.join('+');
}

export function useKeyboardShortcuts(shortcuts: ShortcutMap) {
  const shortcutsRef = useRef(shortcuts);
  shortcutsRef.current = shortcuts;

  const handleKeyDown = useCallback((e: KeyboardEvent) => {
    const target = e.target as HTMLElement;
    if (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA' || target.isContentEditable) {
      return;
    }
    const shortcutKey = getPlatformKey(e);
    const handler = shortcutsRef.current[shortcutKey];
    if (handler) {
      e.preventDefault();
      handler();
    }
  }, []);

  useEffect(() => {
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [handleKeyDown]);
}
```

## Common Shortcuts

```typescript
useKeyboardShortcuts({
  'mod+z': handleUndo,
  'mod+shift+z': handleRedo,
  'mod+s': handleSave,
  'mod+d': handleDuplicate,
  'mod+k': () => setIsPaletteOpen(true),
  'mod+=': handleZoomIn,
  'mod+-': handleZoomOut,
  'delete': handleDelete,
  'backspace': handleDelete,
  'escape': () => selectSection(null),
  '1': () => setViewport('mobile'),
  '2': () => setViewport('tablet'),
  '3': () => setViewport('desktop'),
});
```

## Command Palette Pattern

```typescript
interface Command {
  id: string;
  label: string;
  description?: string;
  icon?: React.ReactNode;
  category: string;
  shortcut?: string;
  action: () => void;
}

export function CommandPalette({ commands, isOpen, onClose }: CommandPaletteProps) {
  const [query, setQuery] = useState('');
  const [selectedIndex, setSelectedIndex] = useState(0);

  const filteredCommands = useMemo(() => {
    if (!query.trim()) return commands;
    const lowerQuery = query.toLowerCase();
    return commands
      .filter(cmd =>
        cmd.label.toLowerCase().includes(lowerQuery) ||
        cmd.description?.toLowerCase().includes(lowerQuery) ||
        cmd.category.toLowerCase().includes(lowerQuery)
      )
      .sort((a, b) => {
        const aExact = a.label.toLowerCase().startsWith(lowerQuery) ? 0 : 1;
        const bExact = b.label.toLowerCase().startsWith(lowerQuery) ? 0 : 1;
        return aExact - bExact;
      });
  }, [query, commands]);

  // ... render with keyboard navigation (ArrowUp/Down/Enter/Escape)
}
```

## Drag-and-Drop with @dnd-kit

```typescript
import { DndContext, DragOverlay, useSensor, useSensors, PointerSensor, KeyboardSensor, closestCenter } from '@dnd-kit/core';
import { SortableContext, sortableKeyboardCoordinates, verticalListSortingStrategy } from '@dnd-kit/sortable';

const sensors = useSensors(
  useSensor(PointerSensor, { activationConstraint: { distance: 8 } }),
  useSensor(KeyboardSensor, { coordinateGetter: sortableKeyboardCoordinates })
);

// Draggable from palette
const { attributes, listeners, setNodeRef, transform, isDragging } = useDraggable({
  id,
  data: { type, name },
});

// Sortable on canvas
const { attributes, listeners, setNodeRef, transform, transition, isDragging } = useSortable({ id });

// Drop zone
const { setNodeRef, isOver } = useDroppable({ id: 'canvas-dropzone' });
```

## Error Boundaries

```typescript
interface Props {
  children: ReactNode;
  fallback?: ReactNode;
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('ErrorBoundary caught:', error, errorInfo);
    this.props.onError?.(error, errorInfo);
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null });
  };

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) return this.props.fallback;
      return (
        <div className="min-h-screen flex items-center justify-center bg-background p-4">
          <div className="max-w-md w-full text-center">
            <h2 className="text-xl font-semibold mb-2">Something went wrong</h2>
            <p className="text-muted-foreground mb-6">An unexpected error occurred.</p>
            <div className="flex gap-3 justify-center">
              <button onClick={this.handleReset} className="px-4 py-2 bg-primary-600 text-white rounded-lg">
                Try Again
              </button>
              <button onClick={() => window.location.reload()} className="px-4 py-2 border rounded-lg">
                Reload Page
              </button>
            </div>
          </div>
        </div>
      );
    }
    return this.props.children;
  }
}
```

## Empty States

```typescript
interface EmptyStateProps {
  icon?: React.ReactNode;
  title: string;
  description?: string;
  action?: { label: string; onClick: () => void };
  secondaryAction?: { label: string; onClick: () => void };
}

export function EmptyState({ icon, title, description, action, secondaryAction }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center text-center p-8">
      {icon && <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-muted flex items-center justify-center text-3xl">{icon}</div>}
      <h3 className="text-lg font-semibold mb-2">{title}</h3>
      {description && <p className="text-sm text-muted-foreground mb-6 max-w-sm">{description}</p>}
      <div className="flex gap-3">
        {action && <button onClick={action.onClick} className="px-4 py-2 bg-primary-600 text-white rounded-lg">{action.label}</button>}
        {secondaryAction && <button onClick={secondaryAction.onClick} className="px-4 py-2 border rounded-lg">{secondaryAction.label}</button>}
      </div>
    </div>
  );
}
```

## Welcome Onboarding Modal

```typescript
interface WelcomeModalProps {
  isOpen: boolean;
  onClose: () => void;
  onGetStarted: () => void;
}

export function WelcomeModal({ isOpen, onClose, onGetStarted }: WelcomeModalProps) {
  const [step, setStep] = useState(0);

  const steps = [
    { title: 'Welcome to WebBuilder', description: 'Build web and Android apps with AI.', icon: '🚀' },
    { title: 'Drag & Drop', description: 'Drag components from the palette to the canvas.', icon: '🎨' },
    { title: 'Keyboard Shortcuts', description: 'Press ⌘K for command palette.', icon: '⌨️' },
    { title: 'Ready to Build', description: 'Start with a template or from scratch.', icon: '✨' },
  ];

  // ... render step content with progress dots and Next/Skip/Get Started buttons
}
```

## Vitest Configuration for Monorepo Packages

### Problem
Vitest fails to resolve `.ts` extensions in imports within monorepo packages.

### Solution
Use extensionless imports in test files and keep config minimal:

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    include: ['src/**/*.test.ts'],
  },
});
```

```typescript
// In test files — use extensionless imports
import { IntentParser } from '../src/intent';  // NOT '../src/intent.ts'
import { CodeGenerator } from '../src/codegen/codegen';
```

### Build Before Testing
When importing from `dist/` (compiled output), build the package first:
```bash
pnpm --filter @webbuilder/core build
pnpm --filter @webbuilder/core test
```
