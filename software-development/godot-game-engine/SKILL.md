---
name: godot-game-engine
description: "Use when developing games with Godot engine."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [Godot, GDScript, game-development, scene-tree, signals, C#]
    related_skills: [game-development-patterns, unity-development-patterns, unreal-engine-basics, animation-web-patterns]
---

# Godot Game Engine

Building games with Godot Engine — from scene tree architecture and GDScript through signals, physics, UI system, and export.

## When to Use

- Building 2D/3D games with lightweight open-source engine
- Rapid prototyping with GDScript
- Cross-platform export (Windows, Mac, Linux, mobile, web)
- Lightweight alternative to Unity/Unreal

## Godot Patterns

```gdscript
# Scene tree architecture
extends Node2D

# Node references
@onready var player = $Player
@onready var health_bar = $UI/HealthBar
@export var enemy_scene: PackedResource

# Signal pattern
signal player_damaged(amount: int)
signal game_over()

func _ready():
    player_damaged.connect(_on_player_damaged)
    game_over.connect(_on_game_over)

func _process(delta):
    if Input.is_action_just_pressed("shoot"):
        var enemy = enemy_scene.instantiate()
        enemy.position = player.position + Vector2(100, 0)
        add_child(enemy)

func _on_player_damaged(amount):
    health_bar.value -= amount
    if health_bar.value <= 0:
        game_over.emit()

# UI with Control nodes
# Container → VBoxContainer → Button, Label, ProgressBar
```

## Verification Checklist

- [ ] Scene tree organized (nodes as components)
- [ ] Signals for decoupled communication between nodes
- [ ] @export variables for inspector tuning
- [ ] Physics layers and collision masks configured
- [ ] UI with Control nodes (containers, themes, anchors)
- [ ] Performance: draw calls, viewport culling, LOD
- [ ] Export templates configured for target platforms
- [ ] GDScript vs C# decision based on team skills
