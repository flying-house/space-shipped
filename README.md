#  Space Shipped

*A 2D space "shipping" game featuring Newtonian physics in an expansive asteroid field*

NOTE: *This is a learning project, expect lots of changes/potentially broken code*


##  About

Space Shipped is a 2D space simulation game where players take on the role of pilot in an asteroid belt full of mining stations. The player is tasked with transiting the belt between stations while managing fuel, avoiding harm, and delivering on each mission's requirements.


## Current Features

- **Newtonian mechanics** and conservation of momentum
- **Real-time fuel consumption** for thrust and maneuvering

## Roadmap
*Goals are in priority order*

### Immediate Goals (in priority order):
- Slew thrust (`Q`/`E`) & related fuel consumption
- Procedural background layers in parallax
    - **Very** slow-moving distant star layer
    - Nearer layers of dim, non-colliding asteroids
    - Object pooling for performance
- Foreground obstacles
    - Simple asteroids w/ self collision & fragmenting
    - **Ship-to-asteroid collisions:** punitive, not immediately game-ending
- Economic gameplay (basic A->B reward system)
- Saved game state
- General tuning:
    - Thrust/mass balancing
    - Fuel consumption
    - Distances/playability

### Near Future (Core) Goals:
- Menus: Main, Map, Station Upgrade/Repair Shop, Contracts
    - Map limited to active player & known locations
    - Upgrades/repair shop unique per station
- Sound effects, music
- Ship weapons to destroy asteroids (expensive)
- Thrust visualization/particle effects
- Collision particle effects

### Distant Future Goals:
- **PyInstaller** for easier access to audience
- Detailed pixel art for ships, stations, engines
    - Fixed-camera view for possible station docking minigame; would need fine control mode
- Procedural asteroid appearance?

## Installation

Depends on Python 3.11+ and pip 

1. **Clone the repository**
   ```bash
   git clone https://github.com/flying-house/space-shipped.git
   ```

2. **Set up virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the game**
   ```bash
   python3 src/main.py
   ```

## Controls

| Key | Action |
|-----|--------|
| `W` | Forward thrust |
| `S` | Reverse thrust |
| `A` | Rotate left |
| `D` | Rotate right |
| `Q` | Slew left |
| `E` | Slew right |


## Misc

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Pygame](https://img.shields.io/badge/Pygame-2.6+-green.svg)](https://pygame.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Development Status](https://img.shields.io/badge/Status-Alpha-red.svg)]()