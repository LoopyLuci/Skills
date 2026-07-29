---
name: webxr-ar-vr-development
description: "Use when building WebXR AR/VR experiences."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [webxr, AR, VR, three-js, A-Frame, spatial-computing, immersive]
    related_skills: [three-js-3d-web, game-development-patterns, responsive-web-design-patterns, animation-web-patterns]
---

# WebXR AR/VR Development

Building immersive AR/VR experiences with WebXR — from session management and spatial tracking through 3D rendering, hand input, and performance optimization.

## When to Use

- Building browser-based VR experiences
- Implementing AR features (object placement, face tracking)
- Creating cross-platform XR apps with Three.js or A-Frame
- Adding spatial UI and interactions

## WebXR Setup

```javascript
// Request XR session
async function startXR(mode = 'immersive-vr') {
    if (!navigator.xr) throw new Error('WebXR not supported');
    
    const session = await navigator.xr.requestSession(mode, {
        requiredFeatures: ['local-floor', 'hand-tracking']
    });
    
    session.addEventListener('end', () => { /* cleanup */ });
    return session;
}

// Animation loop with XR frame
function xrFrameCallback(time, frame) {
    const pose = frame.getViewerPose(referenceSpace);
    if (pose) {
        for (const view of pose.views) {
            // Render from each eye (left/right)
            renderer.render(scene, view.projectionMatrix, view.transform.matrix);
        }
    }
    session.requestAnimationFrame(xrFrameCallback);
}
```

## Verification Checklist

- [ ] WebXR feature detection (navigator.xr)
- [ ] VR/AR session mode selected appropriately
- [ ] Reference space type chosen (local, local-floor, bounded-floor, unbounded)
- [ ] Hand/controller input handled
- [ ] Performance: 90fps target, use instancing, LOD
- [ ] Graceful fallback when WebXR unavailable
