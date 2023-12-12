import pygame
from __init__ import initialize_game
import config
import utils

def main():
    # Initialize Pygame and game entities
    screen, clock = initialize_game()
    
    # Game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw graphics
        screen.fill(config.BACKGROUND_COLOR)  # Fill the screen with a black color (adjust as needed)

        utils.cube_mesh.update_mesh()
        utils.cube_mesh.draw_mesh(screen)
        
        utils.cube_mesh.rotation[0] += 1
        utils.cube_mesh.rotation[1] += 1
        
        print(utils.cube_mesh.rotation)
        
        # Refresh the screen
        pygame.display.flip()

        # Control the frame rate
        clock.tick(config.FRAMERATE)  # Adjust the frame rate as needed

    pygame.quit()

if __name__ == "__main__":
    main()