import pygame
import random
import math
from entities.tank import Tank
from entities.enemy import Enemy
from entities.bullet import Bullet
from utils.constants import *

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("War Thunder Offline")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Game objects
        self.player = Tank(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100, PLAYER_COLOR)
        self.enemies = []
        self.bullets = []
        self.enemy_bullets = []
        
        # Game state
        self.score = 0
        self.enemy_spawn_timer = 0
        self.game_over = False
        
        # Fonts
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        
        # Generate terrain
        self.terrain = self.generate_terrain()
        
    def generate_terrain(self):
        """Generate simple terrain as a list of heights"""
        terrain = []
        for x in range(0, SCREEN_WIDTH, 10):
            height = random.randint(50, 150)
            terrain.append((x, SCREEN_HEIGHT - height))
        return terrain
    
    def spawn_enemy(self):
        """Spawn a new enemy tank"""
        x = random.randint(50, SCREEN_WIDTH - 50)
        y = random.randint(50, 200)
        enemy = Enemy(x, y)
        self.enemies.append(enemy)
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.game_over:
                    # Player shoots
                    bullet = self.player.shoot()
                    if bullet:
                        self.bullets.append(bullet)
                elif event.key == pygame.K_r and self.game_over:
                    # Restart game
                    self.restart_game()
    
    def update(self):
        """Update game state"""
        if self.game_over:
            return
            
        # Get pressed keys for continuous input
        keys = pygame.key.get_pressed()
        
        # Update player
        self.player.update(keys)
        
        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.y < 0 or bullet.y > SCREEN_HEIGHT:
                self.bullets.remove(bullet)
        
        # Update enemy bullets
        for bullet in self.enemy_bullets[:]:
            bullet.update()
            if bullet.y < 0 or bullet.y > SCREEN_HEIGHT:
                self.enemy_bullets.remove(bullet)
        
        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update(self.player.x, self.player.y)
            
            # Enemy shooting
            if random.randint(1, 120) == 1:  # Random shooting
                bullet = enemy.shoot(self.player.x, self.player.y)
                if bullet:
                    self.enemy_bullets.append(bullet)
        
        # Spawn enemies
        self.enemy_spawn_timer += 1
        if self.enemy_spawn_timer >= ENEMY_SPAWN_RATE:
            self.spawn_enemy()
            self.enemy_spawn_timer = 0
        
        # Check collisions
        self.check_collisions()
    
    def check_collisions(self):
        """Check for collisions between objects"""
        # Player bullets hitting enemies
        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                if bullet.check_collision(enemy):
                    self.bullets.remove(bullet)
                    if enemy.take_damage(BULLET_DAMAGE):
                        self.enemies.remove(enemy)
                        self.score += 100
                    break
        
        # Enemy bullets hitting player
        for bullet in self.enemy_bullets[:]:
            if bullet.check_collision(self.player):
                self.enemy_bullets.remove(bullet)
                if self.player.take_damage(BULLET_DAMAGE):
                    self.game_over = True
                break
        
        # Enemies hitting player
        for enemy in self.enemies:
            if self.player.check_collision(enemy):
                if self.player.take_damage(COLLISION_DAMAGE):
                    self.game_over = True
                break
    
    def draw(self):
        """Draw everything to the screen"""
        # Clear screen
        self.screen.fill(SKY_COLOR)
        
        # Draw terrain
        if len(self.terrain) > 1:
            pygame.draw.polygon(self.screen, GROUND_COLOR, 
                               self.terrain + [(SCREEN_WIDTH, SCREEN_HEIGHT), (0, SCREEN_HEIGHT)])
        
        # Draw player
        self.player.draw(self.screen)
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        # Draw bullets
        for bullet in self.bullets:
            bullet.draw(self.screen)
        
        for bullet in self.enemy_bullets:
            bullet.draw(self.screen)
        
        # Draw UI
        self.draw_ui()
        
        # Draw game over screen
        if self.game_over:
            self.draw_game_over()
        
        pygame.display.flip()
    
    def draw_ui(self):
        """Draw user interface elements"""
        # Score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Health bar
        health_width = 200
        health_height = 20
        health_x = 10
        health_y = 50
        
        # Background
        pygame.draw.rect(self.screen, RED, (health_x, health_y, health_width, health_height))
        
        # Health
        current_health_width = (self.player.health / self.player.max_health) * health_width
        pygame.draw.rect(self.screen, GREEN, (health_x, health_y, current_health_width, health_height))
        
        # Border
        pygame.draw.rect(self.screen, WHITE, (health_x, health_y, health_width, health_height), 2)
        
        # Health text
        health_text = self.font.render(f"Health: {self.player.health}/{self.player.max_health}", True, WHITE)
        self.screen.blit(health_text, (health_x, health_y + 25))
    
    def draw_game_over(self):
        """Draw game over screen"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.big_font.render("GAME OVER", True, WHITE)
        score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        restart_text = self.font.render("Press R to Restart", True, WHITE)
        
        # Center the text
        self.screen.blit(game_over_text, 
                        (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
                         SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(score_text, 
                        (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 
                         SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(restart_text, 
                        (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 
                         SCREEN_HEIGHT // 2))
    
    def restart_game(self):
        """Restart the game"""
        self.player = Tank(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100, PLAYER_COLOR)
        self.enemies = []
        self.bullets = []
        self.enemy_bullets = []
        self.score = 0
        self.enemy_spawn_timer = 0
        self.game_over = False
        self.terrain = self.generate_terrain()
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)