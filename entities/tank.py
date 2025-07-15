import math
import pygame
from utils.math3d import Vector3, distance_3d, angle_to_target
from utils.constants import *
from entities.bullet import Bullet

class Tank:
    def __init__(self, x, z, color, is_player=True):
        self.position = Vector3(x, 0.5, z)  # Y is height above ground
        self.velocity = Vector3()
        self.rotation = 0.0  # Hull rotation
        self.turret_rotation = 0.0  # Turret rotation relative to hull
        
        self.color = color
        self.is_player = is_player
        
        # Tank properties
        self.max_health = TANK_MAX_HEALTH
        self.health = self.max_health
        self.speed = TANK_SPEED
        self.rotation_speed = TANK_ROTATION_SPEED
        self.turret_rotation_speed = TURRET_ROTATION_SPEED
        
        # Shooting
        self.can_shoot = True
        self.shoot_cooldown = 0
        self.max_shoot_cooldown = 30  # frames
        
        # Dimensions
        self.width = TANK_WIDTH
        self.length = TANK_LENGTH
        self.height = TANK_HEIGHT
        
    def update(self, keys=None, target_pos=None):
        """Update tank state"""
        if self.is_player and keys:
            self.handle_player_input(keys)
        elif target_pos:
            self.handle_ai_movement(target_pos)
        
        # Apply movement
        self.position = self.position + self.velocity
        
        # Apply friction
        self.velocity = self.velocity * FRICTION
        
        # Keep tank on terrain
        if self.position.y < 0.5:
            self.position.y = 0.5
        
        # Keep within world bounds
        world_half = WORLD_SIZE / 2
        if self.position.x > world_half:
            self.position.x = world_half
        elif self.position.x < -world_half:
            self.position.x = -world_half
        if self.position.z > world_half:
            self.position.z = world_half
        elif self.position.z < -world_half:
            self.position.z = -world_half
        
        # Update shooting cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
            if self.shoot_cooldown <= 0:
                self.can_shoot = True
    
    def handle_player_input(self, keys):
        """Handle player keyboard input"""
        # Movement
        if keys[pygame.K_w]:
            # Move forward
            forward = Vector3(math.sin(self.rotation), 0, math.cos(self.rotation))
            self.velocity = self.velocity + forward * self.speed
        if keys[pygame.K_s]:
            # Move backward
            backward = Vector3(-math.sin(self.rotation), 0, -math.cos(self.rotation))
            self.velocity = self.velocity + backward * self.speed
        
        # Rotation
        if keys[pygame.K_a]:
            self.rotation -= self.rotation_speed
        if keys[pygame.K_d]:
            self.rotation += self.rotation_speed
        
        # Turret rotation
        if keys[pygame.K_q]:
            self.turret_rotation -= self.turret_rotation_speed
        if keys[pygame.K_e]:
            self.turret_rotation += self.turret_rotation_speed
        
        # Normalize rotations
        self.rotation = self.rotation % (2 * math.pi)
        self.turret_rotation = self.turret_rotation % (2 * math.pi)
    
    def handle_ai_movement(self, target_pos):
        """Handle AI movement and turret aiming"""
        if not target_pos:
            return
        
        # Calculate distance to target
        distance = distance_3d(self.position, target_pos)
        
        # If too close, back up
        if distance < 15.0:
            backward = Vector3(-math.sin(self.rotation), 0, -math.cos(self.rotation))
            self.velocity = self.velocity + backward * (self.speed * 0.5)
        elif distance > 25.0:
            # Move toward target
            target_angle = angle_to_target(self.position, target_pos)
            angle_diff = target_angle - self.rotation
            
            # Normalize angle difference
            while angle_diff > math.pi:
                angle_diff -= 2 * math.pi
            while angle_diff < -math.pi:
                angle_diff += 2 * math.pi
            
            # Rotate toward target
            if abs(angle_diff) > 0.1:
                if angle_diff > 0:
                    self.rotation += self.rotation_speed
                else:
                    self.rotation -= self.rotation_speed
            else:
                # Move forward when facing target
                forward = Vector3(math.sin(self.rotation), 0, math.cos(self.rotation))
                self.velocity = self.velocity + forward * self.speed
        
        # Aim turret at target
        turret_target_angle = angle_to_target(self.position, target_pos)
        absolute_turret_angle = self.rotation + self.turret_rotation
        turret_angle_diff = turret_target_angle - absolute_turret_angle
        
        # Normalize turret angle difference
        while turret_angle_diff > math.pi:
            turret_angle_diff -= 2 * math.pi
        while turret_angle_diff < -math.pi:
            turret_angle_diff += 2 * math.pi
        
        # Rotate turret toward target
        if abs(turret_angle_diff) > 0.05:
            if turret_angle_diff > 0:
                self.turret_rotation += self.turret_rotation_speed
            else:
                self.turret_rotation -= self.turret_rotation_speed
    
    def shoot(self, target_pos=None):
        """Shoot a bullet"""
        if not self.can_shoot:
            return None
        
        # Calculate bullet starting position (end of turret)
        absolute_turret_angle = self.rotation + self.turret_rotation
        turret_end = Vector3(
            self.position.x + math.sin(absolute_turret_angle) * (self.length / 2 + 0.5),
            self.position.y + 0.3,
            self.position.z + math.cos(absolute_turret_angle) * (self.length / 2 + 0.5)
        )
        
        # Calculate bullet direction
        direction = Vector3(
            math.sin(absolute_turret_angle),
            0,
            math.cos(absolute_turret_angle)
        )
        
        # Create bullet
        bullet = Bullet(turret_end, direction, self.is_player)
        
        # Set cooldown
        self.can_shoot = False
        self.shoot_cooldown = self.max_shoot_cooldown
        
        return bullet
    
    def take_damage(self, damage):
        """Take damage and return True if destroyed"""
        self.health -= damage
        return self.health <= 0
    
    def check_collision(self, other):
        """Check collision with another object"""
        if hasattr(other, 'position'):
            distance = distance_3d(self.position, other.position)
            return distance < (self.width + getattr(other, 'width', 1.0)) / 2
        return False
    
    def draw(self, renderer):
        """Draw the tank using the renderer"""
        renderer.push_matrix()
        
        # Move to tank position
        renderer.translate(self.position.x, self.position.y, self.position.z)
        
        # Rotate to tank orientation
        renderer.rotate(self.rotation, 0, 1, 0)
        
        # Draw hull
        renderer.push_matrix()
        renderer.scale(self.width, self.height * 0.6, self.length)
        renderer.draw_cube(1.0, 1.0, 1.0, self.color)
        renderer.pop_matrix()
        
        # Draw turret
        renderer.push_matrix()
        renderer.translate(0, self.height * 0.4, 0)
        renderer.rotate(self.turret_rotation, 0, 1, 0)
        
        # Turret base
        renderer.push_matrix()
        renderer.scale(self.width * 0.8, self.height * 0.4, self.width * 0.8)
        renderer.draw_cube(1.0, 1.0, 1.0, self.color)
        renderer.pop_matrix()
        
        # Gun barrel
        renderer.push_matrix()
        renderer.translate(0, 0, self.length * 0.4)
        renderer.scale(0.1, 0.1, self.length * 0.6)
        darker_color = [c * 0.7 for c in self.color[:3]] + [self.color[3]]
        renderer.draw_cube(1.0, 1.0, 1.0, darker_color)
        renderer.pop_matrix()
        
        renderer.pop_matrix()  # turret
        renderer.pop_matrix()  # tank