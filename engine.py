import pygame
from __init__ import initialize_game
import config
import utils
import math
import cProfile

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

        for m in utils.meshes:
            m.update_mesh()

        utils.meshes.sort(key=lambda meshes: meshes.position[2], reverse=True)
        print(utils.meshes[0].position[2])
        print(utils.meshes[0].name)        
        for m in utils.meshes:
            m.draw_mesh(screen)
        
        utils.cube_mesh.rotation[0] += 1
        utils.cube_mesh.rotation[1] += 1
        utils.sphere_mesh.rotation[0] += -1
        utils.sphere_mesh.rotation[1] += -1
        
        translate_counter +=0.01
        utils.cube_mesh.position[0] = math.sin(translate_counter)*4
        #utils.sphere_mesh.position[1] = math.cos(translate_counter)
        utils.cube_mesh.position[2] = math.cos(translate_counter) + 4
        
        # print(utils.sphere_mesh.position)
        # print(utils.cube_mesh.position)
        # Refresh the screen
        pygame.display.flip()
            
        # Control the frame rate
        clock.tick(config.FRAMERATE)  # Adjust the frame rate as needed
    pygame.quit()

if __name__ == "__main__":
    # cProfile.run("main()", sort="cumtime")
    main()