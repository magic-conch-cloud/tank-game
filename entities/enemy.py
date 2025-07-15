from entities.tank import Tank
from utils.constants import *
import random

class Enemy(Tank):
    def __init__(self, x, z):
        super().__init__(x, z, ENEMY_COLOR, is_player=False)
        
        # Enemy-specific properties
        self.health = ENEMY_HEALTH
        self.max_health = ENEMY_HEALTH
        
        # AI behavior timing
        self.shoot_timer = 0
        self.shoot_interval = random.randint(60, 180)  # Random shooting interval
        
        # Random starting rotation
        self.rotation = random.uniform(0, 6.28)  # 0 to 2*pi
        
    def update(self, target_pos):
        """Update enemy with AI behavior"""
        # Call parent update with target position for movement AI
        super().update(target_pos=target_pos)
        
        # Update shooting timer
        self.shoot_timer += 1
        
    def should_shoot(self):
        """Check if enemy should shoot based on timer"""
        if self.shoot_timer >= self.shoot_interval and self.can_shoot:
            self.shoot_timer = 0
            self.shoot_interval = random.randint(60, 180)  # Reset with random interval
            return True
        return False