---
name: three-js-3d-web
description: "Use when building 3D web experiences with Three.js."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [three-js, 3D, WebGL, WebGPU, rendering, GLTF, animation]
    related_skills: [webxr-ar-vr-development, game-development-patterns, animation-web-patterns, performance-budgeting-web]
---

# Three.js 3D Web Development

Building 3D web experiences with Three.js — from scene setup and geometry through lighting, materials, animation, interactivity, and performance optimization.

## When to Use

- Adding 3D visualizations to web applications
- Building product configurators or 3D viewers
- Creating interactive 3D experiences
- Data visualization in 3D space

## Three.js Setup

```javascript
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// Scene, Camera, Renderer
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.z = 5;

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// GLTF Model Loading
const loader = new THREE.GLTFLoader();
loader.load('model.gltf', (gltf) => {
    scene.add(gltf.scene);
});

// Animation loop
function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
}
animate();
```

## Verification Checklist

- [ ] Scene, camera, and renderer configured
- [ ] Lighting set up (ambient, directional, point)
- [ ] Model loading (GLTF, OBJ, or procedural geometry)
- [ ] Interactivity (raycasting, OrbitControls, click events)
- [ ] Performance: geometry merging, LOD, instancing, texture atlases
- [ ] Responsive: handle window resize
- [ ] Fallback when WebGL unavailable
