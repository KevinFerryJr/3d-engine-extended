# initialize.py

import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT

def initialize_game():
    pygame.init()

    # Set up the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('3D Engine Extended')

    # Set up the clock for controlling the frame rate
    clock = pygame.time.Clock()

    return screen, clock
