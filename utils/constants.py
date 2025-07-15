# Game constants and configuration

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

# Game colors
SKY_COLOR = (135, 206, 235)  # Light blue sky
GROUND_COLOR = (139, 69, 19)  # Brown ground
PLAYER_COLOR = (0, 128, 0)   # Green player tank
ENEMY_COLOR = (128, 0, 0)    # Red enemy tanks
BULLET_COLOR = YELLOW

# Tank settings
TANK_WIDTH = 30
TANK_HEIGHT = 20
TANK_SPEED = 3
TANK_ROTATION_SPEED = 2

# Bullet settings
BULLET_WIDTH = 4
BULLET_HEIGHT = 8
BULLET_SPEED = 8
BULLET_DAMAGE = 25
COLLISION_DAMAGE = 50

# Game mechanics
ENEMY_SPAWN_RATE = 180  # frames between enemy spawns
TANK_MAX_HEALTH = 100
ENEMY_HEALTH = 50

# Input keys
MOVE_LEFT_KEY = 'a'
MOVE_RIGHT_KEY = 'd'
MOVE_UP_KEY = 'w'
MOVE_DOWN_KEY = 's'
SHOOT_KEY = 'space'