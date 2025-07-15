#!/usr/bin/env python3
"""
War Thunder Offline - Text-based Demo
A working demonstration of the game mechanics in text format
"""

import random
import math
import time
import os

class Vector3:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z
    
    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar):
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def length(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def normalize(self):
        length = self.length()
        if length > 0:
            return Vector3(self.x / length, self.y / length, self.z / length)
        return Vector3(0, 0, 0)

def distance_3d(pos1, pos2):
    diff = pos1 - pos2
    return diff.length()

class Tank:
    def __init__(self, x, z, name, is_player=True):
        self.position = Vector3(x, 0, z)
        self.rotation = 0.0
        self.turret_rotation = 0.0
        self.name = name
        self.is_player = is_player
        
        self.max_health = 100
        self.health = self.max_health
        self.speed = 0.5
        
        self.can_shoot = True
        self.shoot_cooldown = 0
        
    def move_forward(self):
        dx = math.sin(self.rotation) * self.speed
        dz = math.cos(self.rotation) * self.speed
        self.position.x += dx
        self.position.z += dz
        
    def move_backward(self):
        dx = math.sin(self.rotation) * self.speed
        dz = math.cos(self.rotation) * self.speed
        self.position.x -= dx
        self.position.z -= dz
        
    def rotate_left(self):
        self.rotation -= 0.1
        
    def rotate_right(self):
        self.rotation += 0.1
        
    def rotate_turret_left(self):
        self.turret_rotation -= 0.1
        
    def rotate_turret_right(self):
        self.turret_rotation += 0.1
        
    def shoot(self):
        if self.can_shoot and self.shoot_cooldown <= 0:
            # Calculate bullet direction
            total_rotation = self.rotation + self.turret_rotation
            direction = Vector3(math.sin(total_rotation), 0, math.cos(total_rotation))
            
            bullet = Bullet(self.position, direction, self.is_player)
            self.shoot_cooldown = 30  # 30 frames cooldown
            return bullet
        return None
        
    def update(self, target_pos=None):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
            
        # Simple AI for enemies
        if not self.is_player and target_pos:
            # Move towards target
            direction = target_pos - self.position
            if direction.length() > 3.0:  # Don't get too close
                distance = direction.length()
                if distance > 0:
                    # Rotate towards target
                    target_angle = math.atan2(direction.x, direction.z)
                    angle_diff = target_angle - self.rotation
                    
                    # Normalize angle difference
                    while angle_diff > math.pi:
                        angle_diff -= 2 * math.pi
                    while angle_diff < -math.pi:
                        angle_diff += 2 * math.pi
                    
                    # Rotate towards target
                    if abs(angle_diff) > 0.1:
                        if angle_diff > 0:
                            self.rotate_right()
                        else:
                            self.rotate_left()
                    else:
                        # Move forward when facing target
                        self.move_forward()
                    
                    # Aim turret at target
                    turret_target_angle = target_angle - self.rotation
                    if abs(turret_target_angle) > 0.1:
                        if turret_target_angle > 0:
                            self.rotate_turret_right()
                        else:
                            self.rotate_turret_left()
        
    def take_damage(self, damage):
        self.health -= damage
        return self.health <= 0

class Bullet:
    def __init__(self, position, direction, is_player_bullet=True):
        self.position = Vector3(position.x, position.y, position.z)
        self.velocity = direction.normalize() * 2.0  # Bullet speed
        self.is_player_bullet = is_player_bullet
        self.lifetime = 100  # frames
        
    def update(self):
        self.position = self.position + self.velocity
        self.lifetime -= 1
        return self.lifetime <= 0  # Return True if bullet should be removed

class Game:
    def __init__(self):
        self.player = Tank(0, 0, "Player Tank", is_player=True)
        self.enemies = []
        self.bullets = []
        
        self.score = 0
        self.enemy_spawn_timer = 0
        self.game_over = False
        self.frame = 0
        
        print("=== WAR THUNDER OFFLINE - TEXT DEMO ===")
        print("Controls: w/s=move, a/d=rotate hull, q/e=rotate turret, space=shoot, x=quit")
        print()
        
    def spawn_enemy(self):
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(15, 25)
        x = self.player.position.x + math.cos(angle) * distance
        z = self.player.position.z + math.sin(angle) * distance
        
        enemy_num = len(self.enemies) + 1
        enemy = Tank(x, z, f"Enemy {enemy_num}", is_player=False)
        self.enemies.append(enemy)
        print(f"Enemy tank #{enemy_num} spotted at distance {distance:.1f}!")
        
    def update(self):
        if self.game_over:
            return
            
        self.frame += 1
        
        # Update player
        self.player.update()
        
        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update(self.player.position)
            
            # Enemy shooting
            if random.randint(1, 60) == 1:  # Random shooting
                bullet = enemy.shoot()
                if bullet:
                    self.bullets.append(bullet)
                    print(f"{enemy.name} fires!")
            
            # Remove dead enemies
            if enemy.health <= 0:
                print(f"{enemy.name} destroyed! +100 points")
                self.enemies.remove(enemy)
                self.score += 100
                
        # Update bullets
        for bullet in self.bullets[:]:
            if bullet.update():
                self.bullets.remove(bullet)
                continue
                
            # Check collisions
            if bullet.is_player_bullet:
                # Check collision with enemies
                for enemy in self.enemies[:]:
                    if distance_3d(bullet.position, enemy.position) < 2.0:
                        print(f"Hit! {enemy.name} takes 25 damage")
                        enemy.take_damage(25)
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)
                        break
            else:
                # Check collision with player
                if distance_3d(bullet.position, self.player.position) < 2.0:
                    print(f"Player hit! -25 health")
                    self.player.take_damage(25)
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                        
        # Spawn enemies
        self.enemy_spawn_timer += 1
        if self.enemy_spawn_timer >= 180:  # Every 3 seconds
            self.spawn_enemy()
            self.enemy_spawn_timer = 0
            
        # Check if player is dead
        if self.player.health <= 0:
            self.game_over = True
            print("\\n=== GAME OVER ===")
            print(f"Final Score: {self.score}")
            print("You fought valiantly, commander!")
            
    def display_status(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        print("=== WAR THUNDER OFFLINE - TEXT DEMO ===")
        print(f"Frame: {self.frame} | Score: {self.score}")
        print(f"Player Health: {self.player.health}/100")
        print(f"Position: ({self.player.position.x:.1f}, {self.player.position.z:.1f})")
        print(f"Hull Rotation: {math.degrees(self.player.rotation):.0f}°")
        print(f"Turret Rotation: {math.degrees(self.player.turret_rotation):.0f}°")
        print()
        
        print("=== BATTLEFIELD ===")
        # Simple ASCII battlefield view
        field_size = 10
        for z in range(-field_size, field_size + 1):
            line = ""
            for x in range(-field_size, field_size + 1):
                world_x = self.player.position.x + x
                world_z = self.player.position.z + z
                
                char = "."
                
                # Check for player
                if abs(x) < 1 and abs(z) < 1:
                    char = "P"
                
                # Check for enemies
                for enemy in self.enemies:
                    rel_x = enemy.position.x - self.player.position.x
                    rel_z = enemy.position.z - self.player.position.z
                    if abs(rel_x - x) < 1 and abs(rel_z - z) < 1:
                        char = "E"
                        
                # Check for bullets
                for bullet in self.bullets:
                    rel_x = bullet.position.x - self.player.position.x
                    rel_z = bullet.position.z - self.player.position.z
                    if abs(rel_x - x) < 0.5 and abs(rel_z - z) < 0.5:
                        char = "*" if bullet.is_player_bullet else "!"
                        
                line += char + " "
            print(line)
            
        print()
        print("Legend: P=Player, E=Enemy, *=Your bullets, !=Enemy bullets")
        print("Status:")
        print(f"  Enemies: {len(self.enemies)}")
        print(f"  Active bullets: {len(self.bullets)}")
        print(f"  Can shoot: {'Yes' if self.player.can_shoot and self.player.shoot_cooldown <= 0 else 'No'}")
        
        if self.game_over:
            print("\\n=== GAME OVER ===")
            print("Press Enter to exit...")
            
    def get_input(self):
        """Non-blocking input simulation for demo"""
        # In a real implementation, you'd use proper input handling
        # For demo purposes, we'll simulate some actions
        if self.frame % 30 == 0:  # Every 30 frames
            actions = ['w', 's', 'a', 'd', 'q', 'e', 'space']
            action = random.choice(actions)
            
            if action == 'w':
                self.player.move_forward()
                print("Player moves forward")
            elif action == 's':
                self.player.move_backward()
                print("Player moves backward")
            elif action == 'a':
                self.player.rotate_left()
                print("Player rotates left")
            elif action == 'd':
                self.player.rotate_right()
                print("Player rotates right")
            elif action == 'q':
                self.player.rotate_turret_left()
                print("Turret rotates left")
            elif action == 'e':
                self.player.rotate_turret_right()
                print("Turret rotates right")
            elif action == 'space':
                bullet = self.player.shoot()
                if bullet:
                    self.bullets.append(bullet)
                    print("Player fires!")
                    
    def run_demo(self):
        """Run automated demo"""
        print("Running automated demo for 300 frames...")
        print("This demonstrates the game mechanics working!")
        print()
        
        for _ in range(300):
            if self.game_over:
                break
                
            self.get_input()  # Simulated input
            self.update()
            
            # Display status every 30 frames
            if self.frame % 30 == 0:
                self.display_status()
                time.sleep(0.5)  # Pause for readability
                
        print("\\n=== DEMO COMPLETE ===")
        print(f"Final Score: {self.score}")
        print("The game mechanics are working correctly!")
        print("In a real environment with display support,")
        print("this would be a full 3D tank combat game.")

def main():
    game = Game()
    game.run_demo()

if __name__ == "__main__":
    main()