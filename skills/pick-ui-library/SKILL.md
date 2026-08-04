---
name: pick-ui-library
description: Use when picking the right library for a frontend task.
tags: [ui-libraries, frontend, react, components, tools]
related_skills: [frontend-design, emil-design-eng]
---

# Picking The Right Library

A curated, opinionated list of frontend libraries. When invoked with a task, match to the list and recommend.

## How to Use

1. **Identify the task**, not the library the user named
2. **Check what's already installed** in `package.json`
3. **Recommend one library**, state what it's for in one sentence
4. If the task isn't covered, say so explicitly

## The List

### UI Components & Primitives
| Task | Library |
|---|---|
| Unstyled, accessible UI components (dialogs, popovers, menus, selects) | [base-ui](https://base-ui.com) |
| Command menus (⌘K palettes) | [cmdk](https://cmdk.paco.me) |
| Toasts / notifications | [Sonner](https://sonner.emilkowal.ski) |
| OTP / verification code inputs | [input-otp](https://input-otp.rodz.dev) |
| Customizable GUIs / control panels | [Leva](https://github.com/pmndrs/leva) |

### Motion & Visuals
| Task | Library |
|---|---|
| General-purpose animation | [motion](https://motion.dev) (Framer Motion) |
| Animating numbers (counters, stats) | [NumberFlow](https://number-flow.barvian.me) |
| Animated text components | [torph](https://torph.lochie.me/) |
| 3D globes | [Cobe](https://cobe.vercel.app) |
| Dynamic OG images | [Satori](https://github.com/vercel/satori) |
| Syntax highlighting | [shiki](https://shiki.style) |

### Charts
| Task | Library |
|---|---|
| Real-time / streaming charts | [Liveline](https://github.com/benjtaylor/liveline) |
| General charts | [recharts](https://recharts.org) |

### Interaction & Performance
| Task | Library |
|---|---|
| Drag and drop | [dnd kit](https://dndkit.com) |
| Virtualization (long lists) | [Virtuoso](https://virtuoso.dev) |

### State & Styling
| Task | Library |
|---|---|
| State management | [zustand](https://zustand.docs.pmnd.rs) |
| Conditional className strings | [clsx](https://github.com/lukeed/clsx) |
| Type-safe variant styling | [cva](https://cva.style) |
| Theme switching (no flash) | [next-themes](https://github.com/pacocoursey/next-themes) |

## Common Mismatches to Catch

- Toasts built by hand → Sonner
- `<div>`-based dropdown with manual focus → base-ui
- Animating numbers via re-render → NumberFlow
- 1,000+ row list rendered directly → Virtuoso
- `useState` web of props → zustand

## Common Pitfalls

- ❌ **Presenting a menu of options** — Recommend one library
- ❌ **Ignoring what's already installed** — Check package.json first
- ❌ **Churning dependencies unnecessarily** — Use existing libraries
- ❌ **Recommending outside the list without flagging it** — Say when you've left the curated list

## Verification Checklist

- [ ] Task correctly identified (not the library the user named)
- [ ] `package.json` checked for existing dependencies
- [ ] One library recommended with clear reason
- [ ] If outside curated list, explicitly flagged
- [ ] Installation/wiring provided if part of request
