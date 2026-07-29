---
name: game-development-patterns
description: "Use when implementing game development patterns."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [game-development, Unity, Unreal, Godot, game-loop, ECS, state-machines]
    related_skills: [unity-development-patterns, unreal-engine-basics, godot-game-engine, webxr-ar-vr-development]
---

# Game Development Patterns

Implementing core game development patterns — from game loops and component architecture through state management, input handling, and optimization.

## When to Use

- Building games with Unity, Unreal, or Godot
- Implementing game architecture patterns (ECS, State Machine)
- Managing game state, input, and physics
- Optimizing game performance

## Core Patterns

```python
GAME_PATTERNS = {
    'game_loop': 'Update(tick) → ProcessInput → Render → fixed timestep or variable',
    'entity_component': 'ECS architecture — entities are IDs, components are data, systems are logic',
    'state_machine': 'Finite states (Idle, Walk, Jump, Attack) with transitions and conditions',
    'object_pool': 'Reuse game objects instead of allocate/destroy (bullets, particles)',
    'observer': 'Event system — decoupled communication between game systems',
}

class GameLoop:
    """Fixed timestep game loop pattern."""
    def __init__(self, fps: int = 60):
        self.target_dt = 1.0 / fps
        self.accumulator = 0.0
        self.running = False
    
    def start(self):
        import time
        self.running = True
        previous = time.time()
        while self.running:
            current = time.time()
            self.accumulator += current - previous
            previous = current
            
            while self.accumulator >= self.target_dt:
                self.update(self.target_dt)
                self.accumulator -= self.target_dt
            
            self.render()
    
    def update(self, dt: float): pass
    def render(self): pass
```

## Verification Checklist

- [ ] Game loop with fixed or variable timestep implemented
- [ ] Entity-Component or similar architecture chosen
- [ ] State machines for game entity behavior
- [ ] Object pooling for frequently spawned objects
- [ ] Input handling decoupled from game logic
- [ ] Performance profiling (frame time, draw calls, memory)
