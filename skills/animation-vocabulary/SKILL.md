---
name: animation-vocabulary
description: Use when naming a motion effect by its feel description.
tags: [animation, motion, ui, vocabulary, css]
related_skills: [apple-design, frontend-design]
---

# Animation Vocabulary

Turn a vague description of a motion or effect into the precise term.

## How to Use

1. **Read for intent, not keywords** — Users describe what they *see* or *feel*, not the technical name
2. **Quote the glossary verbatim** — Descriptions are authoritative
3. **Disambiguate close terms** — Contrast similar terms so the user can pick
4. **When nothing matches** — Name the closest term and say it's an approximation

### Example Output Format
```
**Stagger** — Animate several items one after another with a small delay between each, creating a cascade.
```

### Disambiguation Example
```
**Morph** — One shape smoothly turns into another shape, e.g. Dynamic Island.

Close alternates:
- **Crossfade** — if they simply fade over each other
- **Shared element transition** — if an element travels and transforms
```

## Glossary

### Entrances & Exits
- **Fade in/out** — Element appears/disappears by changing opacity
- **Slide in** — Element enters by sliding from off-screen
- **Scale in** — Element grows from smaller to full size
- **Pop in** — Element appears with slight overshoot, like it bounces
- **Reveal** — Content uncovered gradually by animating clip-path or mask

### Sequencing & Timing
- **Stagger** — Animate items one after another with small delays
- **Orchestration** — Deliberately timing multiple animations
- **Keyframes** — Defined animation points (0%, 50%, 100%)

### Movement & Transforms
- **Translate** — Move element along X or Y axis
- **Scale** — Make element bigger or smaller
- **Rotate** — Spin element around a point
- **Origin-aware animation** — Element animates from its trigger

### Transitions Between States
- **Crossfade** — One fades out as another fades in
- **Morph** — One shape turns into another
- **Shared element transition** — Element travels and transforms
- **Layout animation** — Element animates to new position/size

### Scroll
- **Scroll reveal** — Elements animate as they enter viewport
- **Parallax** — Background/foreground move at different speeds

### Feedback & Interaction
- **Hover effect** — Visual change on cursor hover
- **Press feedback** — Subtle scale-down on click
- **Rubber-banding** — Resistance at scroll boundaries
- **Ripple** — Circle expanding from tap point

### Easing
- **Ease-out** — Starts fast, ends slow (default for UI)
- **Ease-in** — Starts slow, ends fast (avoid for UI)
- **Spring** — Physics-based motion (tension, mass, damping)

## Common Pitfalls

- ❌ **Paraphrasing glossary terms** — Use verbatim descriptions
- ❌ **Giving an essay instead of a name** — Lead with the term
- ❌ **Inventing terms** — If it's not in glossary, say so
- ❌ **Matching keywords instead of intent** — Read for the sensation

## Verification Checklist

- [ ] User's description mapped to correct term
- [ ] Glossary quoted verbatim (not paraphrased)
- [ ] Disambiguation provided when multiple terms fit
- [ ] Output leads with the matching term, not an explanation
- [ ] If no match, closest term named with honest caveat
