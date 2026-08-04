---
name: slack-gif-creator
description: Use when creating animated GIFs optimized for Slack.
tags: [gif, animation, slack, pil, creative-coding]
related_skills: [algorithmic-art]
---

# Slack GIF Creator

Create animated GIFs optimized for Slack using Python PIL.

## Slack Requirements

| Parameter | Emoji GIFs | Message GIFs |
|-----------|------------|--------------|
| Dimensions | 128×128 | 480×480 |
| FPS | 10-30 | 10-30 |
| Colors | 48-128 | 48-128 |
| Duration | Under 3 seconds | Flexible |

## Core Workflow

```python
from PIL import Image, ImageDraw

width, height = 128, 128
frames = []
fps = 10

for i in range(fps * 3):
    frame = Image.new('RGB', (width, height), (240, 248, 255))
    draw = ImageDraw.Draw(frame)
    # Draw animation using PIL primitives
    frames.append(frame)

frames[0].save(
    'output.gif',
    save_all=True,
    append_images=frames[1:],
    duration=1000//fps,
    loop=0,
    optimize=True,
    palette='adaptive'
)
```

### Drawing Primitives

```python
draw = ImageDraw.Draw(frame)
draw.ellipse([x1, y1, x2, y2], fill=(r,g,b), outline=(r,g,b), width=3)
draw.polygon(points, fill=(r,g,b), outline=(r,g,b), width=3)
draw.line([(x1,y1), (x2,y2)], fill=(r,g,b), width=5)
draw.rectangle([x1,y1,x2,y2], fill=(r,g,b), outline=(r,g,b), width=3)
```

### Animation Concepts
- **Shake**: Use `math.sin()` with frame index
- **Pulse**: Scale rhythmically with sine wave
- **Bounce**: Ease-out physics for landing
- **Spin**: `image.rotate(angle, resample=Image.BICUBIC)`
- **Fade**: `Image.blend(image1, image2, alpha)`
- **Explode**: Particles with random angles and velocities

## Common Pitfalls

- ❌ **Using emoji fonts** — Unreliable across platforms
- ❌ **Thin lines (width=1)** — Looks amateurish
- ❌ **Linear motion without easing** — Feels mechanical
- ❌ **File size too large** — Slack has strict size limits

## Verification Checklist

- [ ] Dimensions match Slack requirements (128×128 or 480×480)
- [ ] FPS between 10-30
- [ ] Colors reduced to ≤128
- [ ] Duration appropriate for use case
- [ ] Lines use width ≥ 2
- [ ] GIF renders correctly (not corrupted)
