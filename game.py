import pygame
from pygame.locals import *
from OpenGL.GL import *
import random
import math
from entities.tank import Tank
from entities.enemy import Enemy
from entities.bullet import Bullet
from utils.constants import *
from utils.math3d import Vector3, distance_3d
from utils.renderer import Renderer

class Game:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        
        # Set up display with OpenGL
        self.screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        pygame.display.set_mode(self.screen_size, DOUBLEBUF | OPENGL)
        pygame.display.set_caption("War Thunder Offline - 3D")
        
        # Hide mouse cursor and capture it
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        
        # Initialize 3D renderer
        self.renderer = Renderer()
        self.renderer.setup_perspective(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Game state
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        self.paused = False
        
        # Initialize game objects
        self.player = Tank(0, 0, PLAYER_COLOR, is_player=True)
        self.enemies = []
        self.bullets = []
        
        # Game stats
        self.score = 0
        self.enemy_spawn_timer = 0
        
        # Camera system
        self.camera_pos = Vector3(0, CAMERA_HEIGHT, -CAMERA_DISTANCE)
        self.camera_target = Vector3(0, 0, 0)
        self.camera_yaw = 0.0
        self.camera_pitch = -0.3
        
        # Mouse control
        self.mouse_sensitivity = MOUSE_SENSITIVITY
        self.last_mouse_pos = pygame.mouse.get_pos()
        
        # UI
        self.font_initialized = False
        self.setup_ui()
        
    def setup_ui(self):
        """Setup UI rendering"""
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        self.font_initialized = True
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_over:
                        self.running = False
                    else:
                        self.paused = not self.paused
                        pygame.event.set_grab(not self.paused)
                        pygame.mouse.set_visible(self.paused)
                elif event.key == pygame.K_SPACE and not self.game_over and not self.paused:
                    # Player shoots
                    bullet = self.player.shoot()
                    if bullet:
                        self.bullets.append(bullet)
                elif event.key == pygame.K_r and self.game_over:
                    # Restart game
                    self.restart_game()
            elif event.type == pygame.MOUSEMOTION and not self.paused:
                # Mouse look
                mouse_x, mouse_y = event.pos
                rel_x, rel_y = event.rel
                
                self.camera_yaw += rel_x * self.mouse_sensitivity
                self.camera_pitch -= rel_y * self.mouse_sensitivity
                
                # Clamp pitch
                self.camera_pitch = max(-math.pi/2 + 0.1, min(math.pi/2 - 0.1, self.camera_pitch))
    
    def update(self):
        """Update game state"""
        if self.game_over or self.paused:
            return
        
        # Get pressed keys for continuous input
        keys = pygame.key.get_pressed()
        
        # Update player
        self.player.update(keys)
        
        # Update camera to follow player
        self.update_camera()
        
        # Update bullets
        for bullet in self.bullets[:]:
            if bullet.update():
                self.bullets.remove(bullet)
        
        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update(self.player.position)
            
            # Enemy shooting
            if enemy.should_shoot():
                bullet = enemy.shoot()
                if bullet:
                    self.bullets.append(bullet)
        
        # Spawn enemies
        self.enemy_spawn_timer += 1
        if self.enemy_spawn_timer >= ENEMY_SPAWN_RATE and len(self.enemies) < MAX_ENEMIES:
            self.spawn_enemy()
            self.enemy_spawn_timer = 0
        
        # Check collisions
        self.check_collisions()
    
    def update_camera(self):
        """Update camera position to follow player"""
        # Calculate camera position based on yaw and pitch
        camera_distance = CAMERA_DISTANCE
        
        # Camera position relative to player
        camera_x = math.sin(self.camera_yaw) * math.cos(self.camera_pitch) * camera_distance
        camera_y = math.sin(self.camera_pitch) * camera_distance + CAMERA_HEIGHT
        camera_z = math.cos(self.camera_yaw) * math.cos(self.camera_pitch) * camera_distance
        
        # Position camera relative to player
        self.camera_pos = Vector3(
            self.player.position.x + camera_x,
            self.player.position.y + camera_y,
            self.player.position.z + camera_z
        )
        
        # Look at player
        self.camera_target = Vector3(
            self.player.position.x,
            self.player.position.y + 1.0,
            self.player.position.z
        )
    
    def spawn_enemy(self):
        """Spawn a new enemy tank"""
        # Spawn enemy at random position around the edge of the world
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(30, WORLD_SIZE / 2 - 10)
        
        x = math.sin(angle) * distance
        z = math.cos(angle) * distance
        
        enemy = Enemy(x, z)
        self.enemies.append(enemy)
    
    def check_collisions(self):
        """Check for collisions between objects"""
        # Player bullets hitting enemies
        for bullet in self.bullets[:]:
            if bullet.is_player_bullet:
                for enemy in self.enemies[:]:
                    if bullet.check_collision(enemy):
                        self.bullets.remove(bullet)
                        if enemy.take_damage(BULLET_DAMAGE):
                            self.enemies.remove(enemy)
                            self.score += 100
                        break
            else:
                # Enemy bullets hitting player
                if bullet.check_collision(self.player):
                    self.bullets.remove(bullet)
                    if self.player.take_damage(BULLET_DAMAGE):
                        self.game_over = True
                    break
        
        # Enemies colliding with player
        for enemy in self.enemies:
            if self.player.check_collision(enemy):
                if self.player.take_damage(COLLISION_DAMAGE):
                    self.game_over = True
                break
    
    def render(self):
        """Render the 3D scene"""
        # Clear screen
        self.renderer.clear_screen()
        
        # Set camera
        self.renderer.set_camera(self.camera_pos, self.camera_target)
        
        # Draw terrain
        self.renderer.draw_terrain(TERRAIN_SIZE)
        
        # Draw player
        self.player.draw(self.renderer)
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.renderer)
        
        # Draw bullets
        for bullet in self.bullets:
            bullet.draw(self.renderer)
        
        # Draw UI (switch to 2D mode)
        self.draw_ui()
        
        # Swap buffers
        pygame.display.flip()
    
    def draw_ui(self):
        """Draw 2D UI elements over 3D scene"""
        # Save current matrices
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, -1, 1)
        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        # Disable depth testing for UI
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        
        # Draw score
        self.draw_text(f"Score: {self.score}", 10, 10, (1, 1, 1, 1))
        
        # Draw health bar
        self.draw_health_bar()
        
        # Draw crosshair
        self.draw_crosshair()
        
        # Draw controls
        if not self.game_over:
            self.draw_text("WASD: Move | QE: Turret | Mouse: Look | Space: Shoot", 10, SCREEN_HEIGHT - 30, (1, 1, 1, 1))
        
        # Draw game over screen
        if self.game_over:
            self.draw_game_over()
        
        # Draw pause screen
        if self.paused:
            self.draw_pause_screen()
        
        # Restore matrices and settings
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
    
    def draw_text(self, text, x, y, color):
        """Draw text at given position"""
        # Simple text rendering using OpenGL
        glColor4f(*color)
        glRasterPos2f(x, y)
        
        # Note: This is a simplified text rendering
        # In a real implementation, you'd want to use texture-based text rendering
        
    def draw_health_bar(self):
        """Draw player health bar"""
        bar_width = 200
        bar_height = 20
        bar_x = 10
        bar_y = 50
        
        # Background
        glColor4f(0.8, 0.0, 0.0, 1.0)
        glBegin(GL_QUADS)
        glVertex2f(bar_x, bar_y)
        glVertex2f(bar_x + bar_width, bar_y)
        glVertex2f(bar_x + bar_width, bar_y + bar_height)
        glVertex2f(bar_x, bar_y + bar_height)
        glEnd()
        
        # Health
        health_width = (self.player.health / self.player.max_health) * bar_width
        glColor4f(0.0, 0.8, 0.0, 1.0)
        glBegin(GL_QUADS)
        glVertex2f(bar_x, bar_y)
        glVertex2f(bar_x + health_width, bar_y)
        glVertex2f(bar_x + health_width, bar_y + bar_height)
        glVertex2f(bar_x, bar_y + bar_height)
        glEnd()
        
        # Border
        glColor4f(1.0, 1.0, 1.0, 1.0)
        glBegin(GL_LINE_LOOP)
        glVertex2f(bar_x, bar_y)
        glVertex2f(bar_x + bar_width, bar_y)
        glVertex2f(bar_x + bar_width, bar_y + bar_height)
        glVertex2f(bar_x, bar_y + bar_height)
        glEnd()
    
    def draw_crosshair(self):
        """Draw crosshair in center of screen"""
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        size = 10
        
        glColor4f(1.0, 1.0, 1.0, 1.0)
        glBegin(GL_LINES)
        # Horizontal line
        glVertex2f(center_x - size, center_y)
        glVertex2f(center_x + size, center_y)
        # Vertical line
        glVertex2f(center_x, center_y - size)
        glVertex2f(center_x, center_y + size)
        glEnd()
    
    def draw_game_over(self):
        """Draw game over screen"""
        # Semi-transparent overlay
        glColor4f(0.0, 0.0, 0.0, 0.7)
        glBegin(GL_QUADS)
        glVertex2f(0, 0)
        glVertex2f(SCREEN_WIDTH, 0)
        glVertex2f(SCREEN_WIDTH, SCREEN_HEIGHT)
        glVertex2f(0, SCREEN_HEIGHT)
        glEnd()
        
        # Game over text (simplified)
        self.draw_text("GAME OVER", SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 50, (1, 0, 0, 1))
        self.draw_text(f"Final Score: {self.score}", SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT//2, (1, 1, 1, 1))
        self.draw_text("Press R to Restart or ESC to Quit", SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT//2 + 50, (1, 1, 1, 1))
    
    def draw_pause_screen(self):
        """Draw pause screen"""
        # Semi-transparent overlay
        glColor4f(0.0, 0.0, 0.0, 0.5)
        glBegin(GL_QUADS)
        glVertex2f(0, 0)
        glVertex2f(SCREEN_WIDTH, 0)
        glVertex2f(SCREEN_WIDTH, SCREEN_HEIGHT)
        glVertex2f(0, SCREEN_HEIGHT)
        glEnd()
        
        self.draw_text("PAUSED", SCREEN_WIDTH//2 - 50, SCREEN_HEIGHT//2, (1, 1, 1, 1))
        self.draw_text("Press ESC to Resume", SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT//2 + 30, (1, 1, 1, 1))
    
    def restart_game(self):
        """Restart the game"""
        self.player = Tank(0, 0, PLAYER_COLOR, is_player=True)
        self.enemies = []
        self.bullets = []
        self.score = 0
        self.enemy_spawn_timer = 0
        self.game_over = False
        self.paused = False
        
        # Reset camera
        self.camera_yaw = 0.0
        self.camera_pitch = -0.3
        
        # Re-grab mouse
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
        
        pygame.quit()