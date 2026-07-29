---
name: unreal-engine-basics
description: "Use when developing with Unreal Engine."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [Unreal-Engine, C++, Blueprints, game-development, rendering, Quixel]
    related_skills: [game-development-patterns, unity-development-patterns, three-js-3d-web, animation-web-patterns]
---

# Unreal Engine Development

Building games and applications with Unreal Engine — from Blueprints and C++ through rendering, physics, animation, and optimization.

## When to Use

- Building high-fidelity 3D games
- Architectural visualization
- Film and broadcast production (virtual production)
- Real-time simulation and training

## Unreal Architecture

```cpp
// C++ Actor pattern
UCLASS()
class AMyCharacter : public ACharacter
{
    GENERATED_BODY()
public:
    UPROPERTY(EditAnywhere, Category = "Combat")
    float Health = 100.0f;
    
    UPROPERTY(EditDefaultsOnly, Category = "Effects")
    UParticleSystem* HitEffect;
    
    UFUNCTION(BlueprintCallable, Category = "Combat")
    void TakeDamage(float Damage)
    {
        Health -= Damage;
        if (Health <= 0.0f) Die();
    }
    
    virtual void Die() { /* death logic */ }
};

// Blueprint node equivalent
// [Event Hit] → [Apply Damage] → [Play Hit Effect] → [Branch: Health <= 0 → Die]
```

## Verification Checklist

- [ ] Project structure set (Content, Source, Plugins)
- [ ] C++ vs Blueprints decision by feature (Blueprints for iteration, C++ for performance)
- [ ] Rendering pipeline configured (forward/deferred, Lumen, Nanite)
- [ ] Physics and collision set up
- [ ] Animation blueprint (state machine, blend spaces)
- [ ] Performance: draw calls, poly count, texture budgets
- [ ] Build for target platform (Windows, console, mobile)
