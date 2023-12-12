import pygame
from __init__ import initialize_game
import config
import utils
import math

def main():
    # Initialize Pygame and game entities
    screen, clock = initialize_game()
    
    # Game loop
    running = True
    translate_counter = 0
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw graphics
        screen.fill(config.BACKGROUND_COLOR)  # Fill the screen with a black color (adjust as needed)

        utils.cube_mesh.update_mesh()
        utils.cube_mesh.draw_mesh(screen)
        
        utils.cube_mesh.rotation[0] += 0
        utils.cube_mesh.rotation[1] += 1
        
        translate_counter +=0.01
        utils.cube_mesh.position[0] = math.sin(translate_counter)*2.5
        utils.cube_mesh.position[1] = math.cos(translate_counter)
        
        # Refresh the screen
        pygame.display.flip()

        # Control the frame rate
        clock.tick(config.FRAMERATE)  # Adjust the frame rate as needed

    pygame.quit()

if __name__ == "__main__":
    main()