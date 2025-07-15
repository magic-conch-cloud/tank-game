import pygame
from pygame.locals import *
import random
import math
import os
import sys

# Try to import OpenGL, but handle gracefully if not available
try:
    from OpenGL.GL import *
    OPENGL_AVAILABLE = True
except ImportError:
    OPENGL_AVAILABLE = False
    print("OpenGL not available, falling back to 2D mode")

from entities.tank import Tank
from entities.enemy import Enemy
from entities.bullet import Bullet
from utils.constants import *
from utils.math3d import Vector3, distance_3d

# Check if we're in a headless environment
HEADLESS = os.environ.get('DISPLAY') is None

class Game:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        
        # Disable audio to avoid ALSA warnings in headless environments
        pygame.mixer.quit()
        
        # Try to set up 3D mode, but fall back to 2D if it fails
        self.mode_3d = False
        
        if OPENGL_AVAILABLE:
            try:
                print("Attempting to initialize 3D OpenGL mode...")
                self.screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
                pygame.display.set_mode(self.screen_size, DOUBLEBUF | OPENGL)
                
                # Test if OpenGL actually works
                glClear(GL_COLOR_BUFFER_BIT)
                
                print("3D OpenGL mode successful!")
                self.mode_3d = True
                
                # Hide mouse cursor and capture it
                pygame.mouse.set_visible(False)
                pygame.event.set_grab(True)
                
                self.setup_opengl()
                
            except Exception as e:
                print(f"3D mode failed ({e}), falling back to 2D mode")
                self.mode_3d = False
                # Reinitialize pygame display for 2D
                pygame.display.quit()
                pygame.display.init()
                self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        else:
            print("OpenGL not available, using 2D mode")
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        pygame.display.set_caption("War Thunder Offline")
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Game objects
        self.player = Tank(0, 0, PLAYER_COLOR, is_player=True)
        self.enemies = []
        self.bullets = []
        
        # Game state
        self.score = 0
        self.enemy_spawn_timer = 0
        self.game_over = False
        
        # Camera for 3D mode
        if self.mode_3d:
            self.camera_pos = Vector3(0, CAMERA_HEIGHT, CAMERA_DISTANCE)
            self.camera_rotation = Vector3(0, 0, 0)
            self.mouse_locked = True
        
        # Fonts for 2D mode
        if not self.mode_3d:
            self.font = pygame.font.Font(None, 36)
            self.big_font = pygame.font.Font(None, 72)
        
        print(f"Game initialized in {'3D' if self.mode_3d else '2D'} mode")
    
    def setup_opengl(self):
        """Initialize OpenGL settings"""
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        
        # Set up lighting
        glLightfv(GL_LIGHT0, GL_AMBIENT, AMBIENT_LIGHT)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, DIFFUSE_LIGHT)
        glLightfv(GL_LIGHT0, GL_POSITION, LIGHT_POSITION)
        
        # Set clear color (sky)
        glClearColor(*SKY_COLOR)
        
        # Set up perspective
        self.setup_perspective()
    
    def setup_perspective(self):
        """Set up 3D perspective projection"""
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        
        # Set up perspective projection
        from OpenGL.GLU import gluPerspective
        gluPerspective(60, SCREEN_WIDTH / SCREEN_HEIGHT, 0.1, 1000.0)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
    
    def handle_events(self):
        """Handle input events"""
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                elif event.key == K_r and self.game_over:
                    self.restart_game()
        
        # Handle continuous key presses
        keys = pygame.key.get_pressed()
        
        if not self.game_over:
            # Movement
            if keys[K_w]:
                self.player.move_forward()
            if keys[K_s]:
                self.player.move_backward()
            if keys[K_a]:
                self.player.rotate_left()
            if keys[K_d]:
                self.player.rotate_right()
            
            # Turret control (only in 3D mode)
            if self.mode_3d:
                if keys[K_LEFT]:
                    self.player.rotate_turret_left()
                if keys[K_RIGHT]:
                    self.player.rotate_turret_right()
            
            # Shooting
            if keys[K_SPACE]:
                bullet = self.player.shoot()
                if bullet:
                    self.bullets.append(bullet)
        
        # Mouse look (3D mode only)
        if self.mode_3d and self.mouse_locked and not self.game_over:
            mouse_rel = pygame.mouse.get_rel()
            self.camera_rotation.y -= mouse_rel[0] * MOUSE_SENSITIVITY
            self.camera_rotation.x -= mouse_rel[1] * MOUSE_SENSITIVITY
            
            # Clamp vertical rotation
            self.camera_rotation.x = max(-1.5, min(1.5, self.camera_rotation.x))
    
    def update(self):
        """Update game logic"""
        if self.game_over:
            return
        
        # Update player
        self.player.update()
        
        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update(self.player.position)
            bullet = enemy.try_shoot(self.player.position)
            if bullet:
                self.bullets.append(bullet)
            
            # Remove dead enemies
            if enemy.health <= 0:
                self.enemies.remove(enemy)
                self.score += 100
        
        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()
            
            # Remove bullets that are out of bounds or lifetime expired
            if (bullet.position.y < -5 or 
                abs(bullet.position.x) > WORLD_SIZE or 
                abs(bullet.position.z) > WORLD_SIZE or
                bullet.lifetime <= 0):
                self.bullets.remove(bullet)
                continue
            
            # Check collisions with tanks
            if bullet.is_player_bullet:
                # Check collision with enemies
                for enemy in self.enemies[:]:
                    if distance_3d(bullet.position, enemy.position) < 2.0:
                        enemy.take_damage(BULLET_DAMAGE)
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)
                        break
            else:
                # Check collision with player
                if distance_3d(bullet.position, self.player.position) < 2.0:
                    self.player.take_damage(BULLET_DAMAGE)
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
        
        # Spawn enemies
        self.enemy_spawn_timer += 1
        if self.enemy_spawn_timer >= ENEMY_SPAWN_RATE:
            self.spawn_enemy()
            self.enemy_spawn_timer = 0
        
        # Check if player is dead
        if self.player.health <= 0:
            self.game_over = True
        
        # Update camera position (3D mode)
        if self.mode_3d:
            self.update_camera()
    
    def update_camera(self):
        """Update camera position to follow player"""
        # Camera follows player with offset
        offset = Vector3(
            math.sin(self.player.rotation) * CAMERA_DISTANCE,
            CAMERA_HEIGHT,
            math.cos(self.player.rotation) * CAMERA_DISTANCE
        )
        self.camera_pos = self.player.position + offset
    
    def spawn_enemy(self):
        """Spawn a new enemy at a random position"""
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(30, 60)
        x = self.player.position.x + math.cos(angle) * distance
        z = self.player.position.z + math.sin(angle) * distance
        
        enemy = Enemy(x, z)
        self.enemies.append(enemy)
    
    def render(self):
        """Render the game"""
        if self.mode_3d:
            self.render_3d()
        else:
            self.render_2d()
    
    def render_3d(self):
        """Render in 3D OpenGL mode"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Set up camera
        from OpenGL.GLU import gluLookAt
        look_target = Vector3(
            self.camera_pos.x + math.sin(self.camera_rotation.y),
            self.camera_pos.y + math.sin(self.camera_rotation.x),
            self.camera_pos.z + math.cos(self.camera_rotation.y)
        )
        
        gluLookAt(
            self.camera_pos.x, self.camera_pos.y, self.camera_pos.z,
            look_target.x, look_target.y, look_target.z,
            0, 1, 0
        )
        
        # Render terrain
        self.render_terrain()
        
        # Render player
        self.render_tank_3d(self.player)
        
        # Render enemies
        for enemy in self.enemies:
            self.render_tank_3d(enemy)
        
        # Render bullets
        for bullet in self.bullets:
            self.render_bullet_3d(bullet)
        
        pygame.display.flip()
    
    def render_2d(self):
        """Render in 2D software mode"""
        self.screen.fill(SKY_COLOR)
        
        # Simple 2D top-down view
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        
        # Calculate screen positions relative to player
        def world_to_screen(world_pos):
            rel_x = world_pos.x - self.player.position.x
            rel_z = world_pos.z - self.player.position.z
            screen_x = center_x + rel_x * 10  # Scale factor
            screen_y = center_y + rel_z * 10
            return int(screen_x), int(screen_y)
        
        # Draw player (always in center)
        pygame.draw.circle(self.screen, PLAYER_COLOR, (center_x, center_y), 15)
        
        # Draw enemies
        for enemy in self.enemies:
            screen_pos = world_to_screen(enemy.position)
            if 0 <= screen_pos[0] < SCREEN_WIDTH and 0 <= screen_pos[1] < SCREEN_HEIGHT:
                pygame.draw.circle(self.screen, ENEMY_COLOR, screen_pos, 12)
        
        # Draw bullets
        for bullet in self.bullets:
            screen_pos = world_to_screen(bullet.position)
            if 0 <= screen_pos[0] < SCREEN_WIDTH and 0 <= screen_pos[1] < SCREEN_HEIGHT:
                color = BULLET_COLOR if bullet.is_player_bullet else RED
                pygame.draw.circle(self.screen, color, screen_pos, 3)
        
        # Draw UI
        self.render_ui_2d()
        
        pygame.display.flip()
    
    def render_ui_2d(self):
        """Render 2D UI elements"""
        # Health bar
        health_width = 200
        health_height = 20
        health_x = 10
        health_y = 10
        
        # Background
        pygame.draw.rect(self.screen, RED, (health_x, health_y, health_width, health_height))
        
        # Health
        health_ratio = max(0, self.player.health / self.player.max_health)
        pygame.draw.rect(self.screen, GREEN, (health_x, health_y, health_width * health_ratio, health_height))
        
        # Score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 40))
        
        # Enemy count
        enemy_text = self.font.render(f"Enemies: {len(self.enemies)}", True, WHITE)
        self.screen.blit(enemy_text, (10, 70))
        
        # Game over screen
        if self.game_over:
            game_over_text = self.big_font.render("GAME OVER", True, RED)
            restart_text = self.font.render("Press R to restart", True, WHITE)
            
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 60))
            
            self.screen.blit(game_over_text, text_rect)
            self.screen.blit(restart_text, restart_rect)
    
    def render_terrain(self):
        """Render 3D terrain"""
        glColor3f(0.4, 0.6, 0.2)  # Green ground color
        glBegin(GL_QUADS)
        size = TERRAIN_SIZE
        glVertex3f(-size, 0, -size)
        glVertex3f(size, 0, -size)
        glVertex3f(size, 0, size)
        glVertex3f(-size, 0, size)
        glEnd()
    
    def render_tank_3d(self, tank):
        """Render a 3D tank"""
        glPushMatrix()
        
        # Move to tank position
        glTranslatef(tank.position.x, tank.position.y, tank.position.z)
        glRotatef(math.degrees(tank.rotation), 0, 1, 0)
        
        # Set color
        glColor3f(*[c/255 for c in tank.color])
        
        # Draw tank hull (simple box)
        glPushMatrix()
        glScalef(TANK_LENGTH, TANK_HEIGHT, TANK_WIDTH)
        self.draw_cube()
        glPopMatrix()
        
        # Draw turret
        glPushMatrix()
        glTranslatef(0, TANK_HEIGHT * 0.7, 0)
        glRotatef(math.degrees(tank.turret_rotation), 0, 1, 0)
        glScalef(TANK_LENGTH * 0.8, TANK_HEIGHT * 0.6, TANK_WIDTH * 0.8)
        self.draw_cube()
        glPopMatrix()
        
        glPopMatrix()
    
    def render_bullet_3d(self, bullet):
        """Render a 3D bullet"""
        glPushMatrix()
        glTranslatef(bullet.position.x, bullet.position.y, bullet.position.z)
        glColor3f(*[c/255 for c in bullet.color])
        glScalef(0.2, 0.2, 0.2)
        self.draw_cube()
        glPopMatrix()
    
    def draw_cube(self):
        """Draw a simple cube"""
        glBegin(GL_QUADS)
        
        # Front face
        glVertex3f(-0.5, -0.5, 0.5)
        glVertex3f(0.5, -0.5, 0.5)
        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        
        # Back face
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(-0.5, 0.5, -0.5)
        glVertex3f(0.5, 0.5, -0.5)
        glVertex3f(0.5, -0.5, -0.5)
        
        # Top face
        glVertex3f(-0.5, 0.5, -0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(0.5, 0.5, -0.5)
        
        # Bottom face
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(0.5, -0.5, -0.5)
        glVertex3f(0.5, -0.5, 0.5)
        glVertex3f(-0.5, -0.5, 0.5)
        
        # Right face
        glVertex3f(0.5, -0.5, -0.5)
        glVertex3f(0.5, 0.5, -0.5)
        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(0.5, -0.5, 0.5)
        
        # Left face
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(-0.5, -0.5, 0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        glVertex3f(-0.5, 0.5, -0.5)
        
        glEnd()
    
    def restart_game(self):
        """Restart the game"""
        self.player = Tank(0, 0, PLAYER_COLOR, is_player=True)
        self.enemies = []
        self.bullets = []
        self.score = 0
        self.enemy_spawn_timer = 0
        self.game_over = False
    
    def run(self):
        """Main game loop"""
        print("Starting game loop...")
        print("Controls:")
        print("- WASD: Move")
        print("- Arrow keys: Turret (3D mode)")
        print("- Space: Shoot")
        print("- Escape: Quit")
        print("- R: Restart (when game over)")
        
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
        
        print("Game ended.")