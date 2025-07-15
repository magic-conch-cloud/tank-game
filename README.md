# War Thunder Offline - 3D Tank Combat Game

A low-resolution 3D tank combat game inspired by War Thunder. Fight against AI-controlled enemy tanks in an immersive 3D environment with realistic tank physics and combat mechanics.

## Features

- **3D Graphics**: Full 3D environment with OpenGL rendering
- **Realistic Tank Combat**: Separate hull and turret controls just like real tanks
- **AI Enemies**: Smart enemy tanks that hunt and engage the player
- **Mouse Look Camera**: Free-look camera system for enhanced situational awareness
- **Physics**: Realistic movement with friction and momentum
- **Health System**: Take damage from enemy fire and collisions
- **Score System**: Earn points for destroying enemy tanks

## Controls

### Movement
- **W**: Move forward
- **S**: Move backward
- **A**: Rotate hull left
- **D**: Rotate hull right

### Combat
- **Q**: Rotate turret left
- **E**: Rotate turret right
- **Space**: Shoot
- **Mouse**: Look around / Camera control

### Game Controls
- **ESC**: Pause/Resume game
- **R**: Restart game (when game over)

## Installation

1. **Install Python 3.7+** if not already installed

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game**:
   ```bash
   python main.py
   ```

## Gameplay

- Survive as long as possible against waves of enemy tanks
- Enemy tanks will spawn around the perimeter and attack you
- Use your mobility and turret to outmaneuver and destroy enemies
- The game gets progressively more challenging as more enemies spawn
- Your tank can take damage from enemy fire and collisions
- The game ends when your health reaches zero

## Technical Details

- **Engine**: PyOpenGL with Pygame
- **Graphics**: Low-poly 3D models for retro aesthetic
- **Physics**: Simple physics simulation with momentum and friction
- **AI**: Basic AI with pathfinding and targeting
- **Rendering**: Real-time 3D rendering with lighting

## System Requirements

- Python 3.7 or higher
- OpenGL 2.1 compatible graphics card
- Keyboard and mouse
- Minimum 512MB RAM
- 100MB free disk space

## License

This is a fan-made game inspired by War Thunder. Not affiliated with Gaijin Entertainment.

## Known Issues

- Text rendering is simplified (uses basic OpenGL text)
- Some platforms may require additional OpenGL setup
- Mouse sensitivity may need adjustment based on system

Enjoy the battle!