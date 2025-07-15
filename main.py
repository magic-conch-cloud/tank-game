#!/usr/bin/env python3
"""
War Thunder Offline - A simplified 2D tank combat game
Inspired by the popular vehicular combat game War Thunder
"""

import pygame
import sys
from game import Game

def main():
    # Initialize Pygame
    pygame.init()
    
    # Create and run the game
    game = Game()
    game.run()
    
    # Quit
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()