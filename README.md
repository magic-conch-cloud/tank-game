# War Thunder Offline - 3D Tank Combat Game

A low-resolution 3D tank combat game inspired by War Thunder. Fight against AI-controlled enemy tanks in an immersive 3D environment with realistic tank physics and combat mechanics.

## 🎮 What's Included

### 1. Full 3D Game (`main.py`)
- **3D Graphics**: Full 3D environment with OpenGL rendering
- **Realistic Tank Combat**: Separate hull and turret controls just like real tanks
- **AI Enemies**: Smart enemy tanks that hunt and engage the player
- **Mouse Look Camera**: Free-look camera system for enhanced situational awareness
- **Physics**: Realistic movement with friction and momentum
- **Health System**: Take damage from enemy fire and collisions
- **Score System**: Earn points for destroying enemy tanks

### 2. Text-Based Demo (`text_demo.py`)
- **Working Demonstration**: Runs in any environment, including headless servers
- **All Game Mechanics**: Tank movement, turret control, shooting, AI enemies
- **ASCII Battlefield**: Visual representation of the combat area
- **Automated Demo**: Shows the game working without user input

## 🚀 Quick Start

### For Environments with Display Support

```bash
# Install dependencies
pip install -r requirements.txt

# Run the full 3D game
python main.py
```

### For Any Environment (Including Headless)

```bash
# Run the text-based demo (no dependencies needed!)
python text_demo.py
```

## 🎯 Controls

### Full 3D Game
- **W**: Move forward
- **S**: Move backward  
- **A**: Rotate hull left
- **D**: Rotate hull right
- **Left Arrow**: Rotate turret left
- **Right Arrow**: Rotate turret right
- **Mouse**: Look around (camera control)
- **Space**: Shoot
- **Escape**: Quit
- **R**: Restart (when game over)

### Text Demo
- **Automated**: The demo runs automatically to show game mechanics
- **Visual**: ASCII art shows tanks (P=Player, E=Enemy) and bullets (*=yours, !=enemy)

## 🛠 Installation

### Requirements
- Python 3.7+
- For 3D mode: Display support, OpenGL drivers
- For text demo: Nothing extra needed!

### Dependencies (for 3D game)
```bash
pip install pygame PyOpenGL PyOpenGL-accelerate numpy
```

### System Requirements
The game automatically detects your environment:
- **With OpenGL support**: Runs in full 3D mode
- **Without OpenGL/headless**: Falls back to 2D mode  
- **Any issues**: Use the text demo (`text_demo.py`)

## 🎨 Features

### Tank Combat Mechanics
- **Realistic Movement**: Tanks move and rotate like real vehicles
- **Turret Independence**: Hull and turret rotate separately for authentic tank combat
- **Ballistics**: Bullets have travel time and physics
- **Health System**: Take damage from enemy fire
- **AI Behavior**: Enemies hunt, aim, and shoot intelligently

### Technical Features
- **3D Rendering**: OpenGL-based 3D graphics with lighting
- **Collision Detection**: Accurate bullet and tank collision systems
- **Enemy AI**: Smart pathfinding and combat behavior
- **Camera System**: Third-person camera that follows the player
- **Fallback Support**: Automatically adapts to different environments

## 🔧 Troubleshooting

### "GLX is not supported" Error
This is normal in headless or virtual environments. The game will automatically fall back to 2D mode, or you can use the text demo:

```bash
python text_demo.py
```

### Audio Warnings (ALSA errors)
These are harmless warnings in headless environments. Audio is automatically disabled.

### Dependencies Issues
For the simplest experience with no dependencies:
```bash
python text_demo.py
```

## 🎯 Game Objectives

1. **Survive**: Avoid enemy fire and destruction
2. **Score Points**: Destroy enemy tanks for 100 points each
3. **Improve**: Learn tank combat tactics and positioning

## 🏗 Architecture

The game is built with a modular architecture:

- `main.py` - Game entry point
- `game.py` - Main game loop and rendering
- `entities/` - Tank, enemy, and bullet classes
- `utils/` - Math utilities, constants, and rendering helpers
- `text_demo.py` - Standalone working demonstration

## 🎮 Game Mechanics

### Tank Physics
- Forward/backward movement with realistic acceleration
- Hull rotation affects movement direction
- Turret rotates independently for aiming
- Collision detection between tanks

### Combat System  
- Bullets have travel time and physics
- Damage system with health bars
- Shooting cooldowns prevent spam
- Line-of-sight combat

### AI Behavior
- Enemies spawn around the player
- Smart pathfinding to engage the player
- Aiming and shooting when in range
- Retreat and flank maneuvers

## 📝 Development Notes

This game demonstrates:
- 3D graphics programming with OpenGL
- Game physics and collision detection
- AI behavior programming
- Real-time game loop architecture
- Cross-platform compatibility
- Graceful degradation for different environments

The text demo proves all game mechanics work correctly and can serve as a foundation for more complex implementations.

---

**Enjoy commanding your tank in battle! 🚗💥**