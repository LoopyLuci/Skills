---
name: unity-development-patterns
description: "Use when developing games with Unity engine."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [Unity, C#, game-development, ECS, DOTS, MonoBehavior, shaders]
    related_skills: [game-development-patterns, unreal-engine-basics, godot-game-engine, webxr-ar-vr-development]
---

# Unity Development Patterns

Building games and applications with Unity — from MonoBehavior architecture and ECS/DOTS through asset management, physics, lighting, and build optimization.

## When to Use

- Building 2D/3D games with Unity
- Implementing Unity ECS (DOTS) for performance
- Managing assets, scenes, and builds
- Optimizing Unity project performance

## Unity Architecture

```csharp
// MonoBehavior component pattern
public class PlayerController : MonoBehavior
{
    [SerializeField] private float moveSpeed = 5f;
    [SerializeField] private Rigidbody rb;
    
    void Awake() => rb ??= GetComponent<Rigidbody>();
    void FixedUpdate() => HandleMovement();
    void OnCollisionEnter(Collision other) => HandleCollision(other);
    
    private void HandleMovement()
    {
        float h = Input.GetAxis("Horizontal");
        float v = Input.GetAxis("Vertical");
        rb.AddForce(new Vector3(h, 0, v) * moveSpeed);
    }
}

// DOTS ECS pattern
public struct VelocityComponent : IComponentData { public float3 Value; }
public partial struct MovementSystem : ISystem
{
    public void OnUpdate(ref SystemState state)
    {
        foreach (var (vel, trans) in 
                 SystemAPI.Query<RefRW<VelocityComponent>, RefRW<LocalTransform>>())
        {
            trans.ValueRW.Position += vel.ValueRO.Value * SystemAPI.Time.DeltaTime;
        }
    }
}
```

## Verification Checklist

- [ ] Project structure organized (Scenes, Scripts, Prefabs, Assets)
- [ ] MonoBehavior components follow single responsibility
- [ ] Physics layers and collision matrix configured
- [ ] Build settings per platform (standalone, mobile, WebGL)
- [ ] Performance profiling (frame debugger, profiler, memory)
- [ ] Asset bundle/addressable strategy for content management
- [ ] DOTS/ECS considered for CPU-intensive systems
