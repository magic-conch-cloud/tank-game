# Game constants and configuration for 3D War Thunder

# Screen settings
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

# Colors (RGB values)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)

# 3D World settings
WORLD_SIZE = 200.0
TERRAIN_SIZE = 100.0
TERRAIN_HEIGHT = 5.0

# Camera settings
CAMERA_HEIGHT = 8.0
CAMERA_DISTANCE = 15.0
CAMERA_SPEED = 0.2
MOUSE_SENSITIVITY = 0.002

# Tank settings
TANK_WIDTH = 2.0
TANK_LENGTH = 3.0
TANK_HEIGHT = 1.5
TANK_SPEED = 0.15
TANK_ROTATION_SPEED = 0.02
TURRET_ROTATION_SPEED = 0.03

# Bullet settings
BULLET_SPEED = 1.0
BULLET_DAMAGE = 25
COLLISION_DAMAGE = 50
BULLET_LIFETIME = 300  # frames

# Game mechanics
ENEMY_SPAWN_RATE = 300  # frames between enemy spawns
TANK_MAX_HEALTH = 100
ENEMY_HEALTH = 50
MAX_ENEMIES = 8

# Physics
GRAVITY = -0.01
FRICTION = 0.95

# Colors for 3D objects
SKY_COLOR = [0.5, 0.7, 1.0, 1.0]  # Light blue sky
GROUND_COLOR = [0.2, 0.8, 0.2, 1.0]  # Green ground
PLAYER_COLOR = [0.0, 0.6, 0.0, 1.0]   # Dark green player tank
ENEMY_COLOR = [0.8, 0.0, 0.0, 1.0]    # Red enemy tanks
BULLET_COLOR = [1.0, 1.0, 0.0, 1.0]   # Yellow bullets
EXPLOSION_COLOR = [1.0, 0.5, 0.0, 1.0]

# Lighting
AMBIENT_LIGHT = [0.3, 0.3, 0.3, 1.0]
DIFFUSE_LIGHT = [0.8, 0.8, 0.8, 1.0]
LIGHT_POSITION = [10.0, 20.0, 10.0, 1.0]

# Input keys
MOVE_LEFT_KEY = 'a'
MOVE_RIGHT_KEY = 'd'
MOVE_UP_KEY = 'w'
MOVE_DOWN_KEY = 's'
SHOOT_KEY = 'space'