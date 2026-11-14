---
name: frontend-ui-engineering
description: Use when building or modifying interfaces and pages, creating components, implementing layouts, meeting WCAG accessibility requirements, managing state, or when the output needs to look and feel production-quality rather than AI-generated.
version: 2.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [software-development, engineering, agent-skills, frontend, ui, ux, accessibility]
    source: addyosmani/agent-skills
    adapted: true
---

# Frontend UI Engineering

> **Adapted for the LoopyLuci Skills collection** from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- Building or modifying interfaces and pages, creating components, implementing layouts, meeting WCAG accessibility requirements, managing state, or when the output needs to look and feel production-quality rather than AI-generated

## When NOT to Use

- Components with more than 200 lines (split them)
- Inline styles or arbitrary pixel values
- Missing error states, loading states, or empty states
- No keyboard navigation testing
- Color as the sole indicator of state (red/green without text or icons)
- Generic "AI look" (purple gradients, oversized cards, stock layouts)

## Overview

Ship user interfaces that read as deliberate product work rather than model output: accessible by default, responsive from the start, consistent with the project's design system, and free of the visual defaults that make generated UI instantly recognizable. Apply these rules to any new or modified user-facing surface, and lean on the project's existing commands to verify the result instead of installing tooling just to check yourself.

## Verify With What the Project Has

Run the test, type-check, and lint commands the project already defines. Do not install a framework, test runner, or type checker solely to validate your own change. When the project has no such tooling, review the work against the [Verification](#verification) list below and state plainly which checks you could not run.

## Component Architecture

### File Layout

Keep everything belonging to a component in one folder:

```
src/components/
  TaskList/
    TaskList.tsx          # Component implementation
    TaskList.test.tsx     # Tests
    TaskList.stories.tsx  # Storybook stories (if using)
    use-task-list.ts      # Custom hook (if complex state)
    types.ts              # Component-specific types (if needed)
```

### Composition Over Configuration

Children and slots beat a wall of configuration props:

```tsx
// Good: Composable
<Card>
  <CardHeader>
    <CardTitle>Tasks</CardTitle>
  </CardHeader>
  <CardBody>
    <TaskList tasks={tasks} />
  </CardBody>
</Card>

// Avoid: Over-configured
<Card
  title="Tasks"
  headerVariant="large"
  bodyPadding="md"
  content={<TaskList tasks={tasks} />}
/>
```

A component should do one thing. When it accumulates unrelated concerns, split it rather than adding branches.

### Data Fetching vs Rendering

Containers load and guard data; presentational components render it:

```tsx
// Container: handles data
export function TaskListContainer() {
  const { tasks, isLoading, error, refetch, toggleTask, deleteTask } = useTasks();

  if (isLoading) return <TaskListSkeleton />;
  if (error) return <ErrorState message="Failed to load tasks" retry={refetch} />;
  if (tasks.length === 0) return <EmptyState message="No tasks yet" />;

  return <TaskList tasks={tasks} onToggle={toggleTask} onDelete={deleteTask} />;
}

// Presentation: handles rendering
export function TaskList({ tasks, onToggle, onDelete }: { tasks: Task[] } & Pick<TaskItemProps, 'onToggle' | 'onDelete'>) {
  return (
    <ul role="list" className="divide-y">
      {tasks.map(task => <TaskItem key={task.id} task={task} onToggle={onToggle} onDelete={onDelete} />)}
    </ul>
  );
}
```

## State Management

Choose the lightest option that fits the sharing scope:

```
Local state (useState)           → Component-specific UI state
Lifted state                     → Shared between 2-3 sibling components
Context                          → Theme, auth, locale (read-heavy, write-rare)
URL state (searchParams)         → Filters, pagination, shareable UI state
Server state (React Query, SWR)  → Remote data with caching
Global store (Zustand, Redux)    → Complex client state shared app-wide
```

Prop drilling deeper than three levels is the signal to introduce context or restructure the component tree.

## Design System Adherence

### Reference-Led Visual Direction

When a screen needs a distinct visual direction, gather evidence before picking a layout:

1. Search a trusted reference catalogue, or use references supplied by the product team.
2. Study two or three relevant screens and record decisions about hierarchy, density, navigation, controls, responsive behavior, and interaction states.
3. Turn those decisions into a short design contract before implementing: the screen's job, primary action, required states, responsive rules, and patterns to reject.
4. Rebuild the useful structure with the product's own components, tokens, content, and visual language. Never copy another product's branding, proprietary text, imagery, or exact layout.

Treat references as evidence, not templates. Without references, document the assumptions you made and check the result against the existing design system.

### Visual Tics That Signal Generated UI

| Generated Default | Why It Falls Flat | Production Replacement |
|---|---|---|
| Purple/indigo everywhere | Safe-looking palettes make every app identical | The project's actual color palette |
| Excessive gradients | Adds noise and fights most design systems | Flat fills or a subtle gradient the system defines |
| Everything maximally rounded | Ignores how real hierarchies use corner radii | Border radius values taken from the design system |
| Generic hero section | Template layout disconnected from content and user need | Content-first layout |
| Lorem ipsum-style copy | Placeholder text hides wrapping, length, and overflow problems | Realistic sample content |
| Oversized padding everywhere | Flattens hierarchy and burns screen space | Consistent spacing scale |
| Stock card grids | Uniform grid ignores information priority and scanning | Purpose-driven layout |
| Layered heavy shadows | Depth competes with content and taxes low-end devices | Subtle or no shadows unless the system specifies |

### Spacing, Typography, Color

Stay on the project's spacing scale; arbitrary pixel values break visual rhythm:

```css
/* Use the scale: 0.25rem increments (or whatever the project uses) */
/* Good */  padding: 1rem;      /* 16px */
/* Good */  gap: 0.75rem;       /* 12px */
/* Bad */   padding: 13px;      /* Not on any scale */
/* Bad */   margin-top: 2.3rem; /* Not on any scale */
```

Respect the type hierarchy and do not skip levels or style non-heading content as headings:

```
h1 → Page title (one per page)
h2 → Section title
h3 → Subsection title
body → Default text
small → Secondary/helper text
```

For color: use semantic tokens (`text-primary`, `bg-surface`, `border-default`) rather than raw hex values, hold contrast to 4.5:1 for normal text and 3:1 for large text, and never rely on color alone to convey state — pair it with icons, text, or patterns.

## Accessibility (WCAG 2.1 AA)

Every interactive element must be reachable and operable by keyboard. Follow the [WAI-ARIA APG patterns](https://www.w3.org/WAI/ARIA/apg/patterns/) exactly for menus, dialogs, tabs, listboxes, and comboboxes.

Native elements carry focus semantics for free; reach for `role` and `tabIndex` only when no native element fits, and prefer the native one:

```tsx
// Every interactive element must be keyboard accessible
<button onClick={handleClick}>Click me</button>        // ✓ Focusable by default
<div onClick={handleClick}>Click me</div>               // ✗ Not focusable
<div role="button" tabIndex={0} onClick={handleClick}    // ✓ But prefer <button>
     onKeyDown={e => {
       if (e.key === 'Enter') handleClick();
       if (e.key === ' ') e.preventDefault();
     }}
     onKeyUp={e => {
       if (e.key === ' ') handleClick();
     }}>
  Click me
</div>
```

Label anything interactive that has no visible text, and tie form inputs to labels:

```tsx
// Label interactive elements that lack visible text
<button aria-label="Close dialog"><XIcon /></button>

// Label form inputs
<label htmlFor="email">Email</label>
<input id="email" type="email" />

// Or use aria-label when no visible label exists
<input aria-label="Search tasks" type="search" />
```

Move focus when content changes, and trap it inside overlays while they are open:

```tsx
// Move focus when content changes
function Dialog({ isOpen, onClose }: DialogProps) {
  const closeRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    if (isOpen) closeRef.current?.focus();
  }, [isOpen]);

  // Trap focus inside dialog when open
  return (
    <dialog open={isOpen}>
      <button ref={closeRef} onClick={onClose}>Close</button>
      {/* dialog content */}
    </dialog>
  );
}
```

Never render a blank screen — give empty and error states content and a next step:

```tsx
// Don't show blank screens
function TaskList({ tasks, onCreateTask }: { tasks: Task[]; onCreateTask: () => void }) {
  if (tasks.length === 0) {
    return (
      <div role="status" className="text-center py-12">
        <TasksEmptyIcon className="mx-auto h-12 w-12 text-muted" />
        <h3 className="mt-2 text-sm font-medium">No tasks</h3>
        <p className="mt-1 text-sm text-muted">Get started by creating a new task.</p>
        <Button className="mt-4" onClick={onCreateTask}>Create Task</Button>
      </div>
    );
  }

  return <ul role="list">...</ul>;
}
```

## Responsive Design

Design mobile first, then expand upward:

```tsx
// Tailwind: mobile-first responsive
<div className="
  grid grid-cols-1      /* Mobile: single column */
  sm:grid-cols-2        /* Small: 2 columns */
  lg:grid-cols-3        /* Large: 3 columns */
  gap-4
">
```

Verify at 320px, 768px, 1024px, and 1440px.

## Loading and Transitions

Use skeletons instead of spinners for content regions, and mark busy regions for assistive technology:

```tsx
// Skeleton loading (not spinners for content)
function TaskListSkeleton() {
  return (
    <div className="space-y-3" role="status" aria-busy="true" aria-label="Loading tasks">
      {Array.from({ length: 3 }).map((_, i) => (
        <div key={i} className="h-12 bg-muted animate-pulse rounded" />
      ))}
    </div>
  );
}
```

Update optimistically so the interface feels fast, and roll back on failure:

```tsx
// Optimistic updates for perceived speed
function useToggleTask() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: toggleTask,
    onMutate: async (taskId) => {
      await queryClient.cancelQueries({ queryKey: ['tasks'] });
      const previous = queryClient.getQueryData(['tasks']);

      queryClient.setQueryData(['tasks'], (old: Task[]) =>
        old.map(t => t.id === taskId ? { ...t, done: !t.done } : t)
      );

      return { previous };
    },
    onError: (_err, _taskId, context) => {
      queryClient.setQueryData(['tasks'], context?.previous);
    },
  });
}
```

## Common Rationalizations

| Excuse | Reality |
|---|---|
| "Accessibility is a nice-to-have" | It is a legal obligation in many jurisdictions and an engineering standard. |
| "We'll make it responsive later" | Retrofitting responsiveness costs roughly three times building it in from the start. |
| "The design isn't final, so styling can wait" | Fall back on design system defaults; unstyled UI reads as broken to reviewers. |
| "This is just a prototype" | Prototypes become production code; get the foundation right the first time. |
| "The AI aesthetic is fine for now" | It advertises low quality; use the real design system from the beginning. |

## Red Flags

- Components past 200 lines (split them)
- Inline styles or arbitrary pixel values
- Missing error, loading, or empty states
- Keyboard navigation never exercised
- Color as the only carrier of state (red/green with no text or icon)
- Generic generated look (purple gradients, oversized cards, stock layouts)

## Verification

Check what the project's tooling can confirm, and review the remainder against this list. Do not add dependencies or install toolchains just to verify; report which checks were not runnable.

- [ ] Component renders with no console errors
- [ ] Every interactive element is keyboard reachable (tab through the page)
- [ ] A screen reader can convey the page's content and structure
- [ ] Responsive at 320px, 768px, 1024px, and 1440px
- [ ] Loading, empty, error, success, and permission states handled where applicable
- [ ] Design system conventions followed for spacing, color, and typography
- [ ] Final UI-specific finish-gate review passed
- [ ] No accessibility warnings in dev tools or axe-core

## Related Skills in This Repo

- [code-review-and-quality](../code-review-and-quality/SKILL.md) — Use when reviewing code written by yourself, another agent, or a human; you need to assess...
- [ci-cd-and-automation](../ci-cd-and-automation/SKILL.md) — Use when setting up or modifying build and deployment pipelines; you need to automate qual...
- [api-and-interface-design](../api-and-interface-design/SKILL.md) — Use when designing APIs, module boundaries, or any public interface; creating REST or Grap...
- [git-workflow-and-versioning](../git-workflow-and-versioning/SKILL.md) — Use when making any code change; committing, branching, resolving conflicts, splitting unc...
- [game-ux-ui-design](../game-ux-ui-design/SKILL.md) — Diegetic UI, HUD design, accessibility, localization, and platform certification UX requir...
- [frontend-design](../frontend-design/SKILL.md) — Guidance for distinctive, intentional visual design when building new UI or reshaping an e...
- [svelte-web-dashboard](../svelte-web-dashboard/SKILL.md) — Use when building the Sentinel web UI with Svelte 5.

## Adaptation Notes

- Description rewritten into this repo's trigger form.
- Trigger and When-NOT-to-Use sections derived from the upstream guidance.
- Body condensed and restructured; commands, file paths, and tables preserved.
- Upstream anti-patterns retained as the When-NOT-to-Use list.
- Related skills linked from this repo.
- Upstream branding and attribution lines removed (attribution below).

## Source & Attribution

- Upstream: [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)
- Path: `_sources/addyosmani_agent-skills/skills/frontend-ui-engineering/SKILL.md`
- License: MIT — Copyright (c) 2025 Addy Osmani
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.
