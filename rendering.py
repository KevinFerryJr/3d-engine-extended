import math
import numpy
from config import SCREEN_HEIGHT, SCREEN_WIDTH

aspect_ratio = SCREEN_WIDTH/SCREEN_HEIGHT
fov_angle = math.radians(90)
fov = 1.0 / math.tan(fov_angle/2.0)
z_far = 1000
z_near = .1

# convert a 3d point to screen space (2d)
def calculate_point(coords):
    
    # Make a copy of 3d points
	point_matrix = [float(coord) for coord in coords]
	# Add 1 to the matrix array
	point_matrix.append(1)
    
    # Projection matrix formula
	projection_matrix = [
	[fov,0,0,0],
	[0,-fov * aspect_ratio ,0,0],
	[0,0,(z_far+z_near)/(z_far-z_near),1],
	[0,0,(2*z_near*z_far)/(z_near-z_far),0]
	]
    
    # Multiply matrices
	res = numpy.dot(point_matrix, projection_matrix)
	return res

def convert_to_screen_space(coords):
    x,y,w = coords[0], coords[1], coords[3]
    
    # Position the coordinates relative to screen space
    new_x = (x * SCREEN_WIDTH ) / (2.0 * w) + (SCREEN_WIDTH/2)
    new_y = (y * SCREEN_HEIGHT) / (2.0 * w) + (SCREEN_HEIGHT/2)
    
    return [new_x,new_y]