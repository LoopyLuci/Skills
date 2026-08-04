---
name: algorithmic-art
description: Use when creating p5.js generative art or animations.
tags: [generative-art, p5js, creative-coding, procedural-generation]
related_skills: [canvas-design, p5js]
---

# Algorithmic Art

Create gallery-quality computational art using p5.js with seeded randomness and interactive parameter exploration. This skill follows a two-step process: (1) create an algorithmic philosophy, (2) express it as an interactive p5.js HTML artifact.

## Process Overview

**User request** → **Algorithmic philosophy** → **Implementation**

1. **Interpret the user's intent** — What aesthetic is being sought?
2. **Create an algorithmic philosophy** (4-6 paragraphs) describing the computational approach
3. **Implement it in code** — Build the algorithm that expresses this philosophy
4. **Design appropriate parameters** — What should be tunable?
5. **Build matching UI controls** — Sliders/inputs for those parameters

## Algorithmic Philosophy Creation

Begin by creating an ALGORITHMIC PHILOSOPHY (not static images or templates) describing:
- Computational processes, emergent behavior, mathematical beauty
- Seeded randomness, noise fields, organic systems
- Particles, flows, fields, forces
- Parametric variation and controlled chaos

### Philosophy Structure

Name the movement (1-2 words), then articulate the philosophy in 4-6 paragraphs covering:
- Computational processes and mathematical relationships
- Noise functions and randomness patterns
- Particle behaviors and field dynamics
- Temporal evolution and system states
- Parametric variation and emergent complexity

## p5.js Implementation

### Technical Requirements

```javascript
// ALWAYS use a seed for reproducibility
let seed = 12345;
randomSeed(seed);
noiseSeed(seed);
```

```javascript
let params = {
  seed: 12345,
  // control quantities, scales, probabilities, ratios, angles, thresholds
};
```

### Canvas Setup

```javascript
function setup() {
  createCanvas(1200, 1200);
}

function draw() {
  // Can be static (noLoop) or animated
}
```

### Craftsmanship Requirements
- **Balance**: Complexity without visual noise, order without rigidity
- **Color Harmony**: Thoughtful palettes, not random RGB values
- **Composition**: Visual hierarchy and flow even in randomness
- **Performance**: Smooth execution, optimized for real-time if animated
- **Reproducibility**: Same seed ALWAYS produces identical output

## Interactive Artifact Structure

```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.7.0/p5.min.js"></script>
</head>
<body>
  <div id="canvas-container"></div>
  <div id="controls">
    <!-- Seed controls + parameter sliders + actions -->
  </div>
  <script>// ALL p5.js code inline</script>
</body>
</html>
```

### Fixed UI Sections
- Seed display with Prev/Next/Random/Jump controls
- Parameters section with sliders for numeric values
- Actions section: Regenerate, Reset, Download PNG buttons

## Common Pitfalls

- ❌ **Creating HTML from scratch** — Always start from the template structure
- ❌ **Over-parameterizing** — Only expose parameters that meaningfully change the output
- ❌ **Animating without purpose** — Every visual element should serve the algorithmic philosophy

## Verification Checklist

- [ ] p5.js loads from CDN and sketch runs
- [ ] Seed controls work (prev/next/random/jump)
- [ ] All parameters have UI controls that update output
- [ ] Same seed produces identical output every time
- [ ] Color palette is intentional and harmonious
- [ ] Self-contained HTML works directly in any browser
