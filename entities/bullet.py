from utils.math3d import Vector3, distance_3d
from utils.constants import *

class Bullet:
    def __init__(self, position, direction, is_player_bullet=True):
        self.position = Vector3(position.x, position.y, position.z)
        self.velocity = direction.normalize() * BULLET_SPEED
        self.is_player_bullet = is_player_bullet
        
        # Bullet properties
        self.width = 0.2  # For collision detection
        self.lifetime = BULLET_LIFETIME
        self.gravity_velocity = 0.0
        
        # Visual properties
        self.color = BULLET_COLOR
        
    def update(self):
        """Update bullet position and physics"""
        # Apply velocity
        self.position = self.position + self.velocity
        
        # Apply gravity
        self.gravity_velocity += GRAVITY
        self.position.y += self.gravity_velocity
        
        # Decrease lifetime
        self.lifetime -= 1
        
        # Check if bullet should be removed
        return self.lifetime <= 0 or self.position.y < -10
    
    def check_collision(self, other):
        """Check collision with another object"""
        if hasattr(other, 'position'):
            distance = distance_3d(self.position, other.position)
            collision_distance = self.width + getattr(other, 'width', 1.0)
            return distance < collision_distance
        return False
    
    def draw(self, renderer):
        """Draw the bullet"""
        renderer.push_matrix()
        renderer.translate(self.position.x, self.position.y, self.position.z)
        renderer.draw_sphere(0.1, self.color, slices=8, stacks=8)
        renderer.pop_matrix()