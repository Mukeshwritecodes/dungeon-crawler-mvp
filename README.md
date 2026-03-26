# 2D Dungeon Crawler (Shapebound)

A 2D dungeon crawler game developed using Python and Pygame, featuring real-time combat, enemy AI, and a dynamic transformation system. This project focuses on modular architecture and core gameplay mechanics.

---

## Features

* Player movement with physics (gravity, jumping)
* Real-time combat system
* Multiple enemy types with unique behaviors (Slime, Bat, Golem)
* Transformation system with different abilities
* Tile-based map with collision detection
* Smooth camera system with zoom and clamping
* State-based animation system
* Sound effects integration
* Hazard system (spikes, death, respawn)
* XP and leveling system

---

## Controls

| Key   | Action            |
| ----- | ----------------- |
| A / D | Move Left / Right |
| Space | Jump              |
| Q     | Attack            |
| T     | Transform         |
| ESC   | Pause Menu        |

---

## Core Systems

### Player System

Handles movement, gravity, jumping, animations, and transformations. Each transformation modifies player attributes such as speed, attack, and movement capabilities.

### Enemy AI

Includes different enemy types with distinct behaviors:

* Slime: ground-based jumping enemy
* Bat: flying enemy with tracking behavior
* Golem: boss-type enemy with higher stats

### Combat System

Implements collision-based hit detection, damage calculation using attack and defense values, and cooldown-based attacks.

### Transformation System

Allows switching between different forms. Each form dynamically updates player stats, abilities, animations, and hitboxes.

### Camera System

Implements smooth following using interpolation and zoom functionality.

### TileMap System

Loads maps from CSV files created using Tiled Map Editor. Supports multiple layers and handles collision detection using tile rectangles.

---

## Tech Stack

* Language: Python
* Library: Pygame-ce
* Tools:

  * Tiled Map Editor (map design)
  * PyCharm

---

## Project Structure

```
core/
  game.py
  input_handler.py

entities/
  player.py
  enemy.py
  entity_base.py
  enemyTypes/
    bosses/
      mud_golem.py
    mobs/  
      slime_monster.py
      bat_monster.py

forms/
  base_form.py
  bat_form.py
  slime_form.py

systems/
  combat_system.py
  xp_system.py
  sound_manager.py
  transformation_system.py

world/
  tilemap.py
  camera.py

utils/
  helpers.py
  constants.py
config.py
main.py
```

---

## How to Run

1. Install dependencies:

```
pip install pygame-ce
```

2. Run the game:

```
python main.py
```

---

## Current Status

This project is a Minimum Viable Product (MVP) demonstrating core gameplay systems and architecture.

---

## Future Improvements

* Advanced enemy AI and behaviors
* Improved animations and visual effects
* Enhanced level design with exploration elements
* Boss mechanics and attack patterns
* UI/UX improvements
* Migration to Godot Engine for full-scale development

---

## Inspiration

Inspired by games like Hollow Knight, focusing on exploration, combat, and responsive gameplay.

---

## Author

Mukesh Choudhary

---

Game screen shots:
---
<img width="1429" height="827" alt="image" src="https://github.com/user-attachments/assets/eb42a28f-1858-463c-b4d0-9f07aa6f06bf" />
<img width="1427" height="822" alt="image" src="https://github.com/user-attachments/assets/545ed8bc-3344-4644-8454-70d9a64c4727" />
<img width="1417" height="809" alt="image" src="https://github.com/user-attachments/assets/26d8d2a3-96f0-4d45-a407-288d36792245" />
<img width="1349" height="803" alt="image" src="https://github.com/user-attachments/assets/afc125ef-75de-4ad5-8e64-d9fa145cad6f" />






