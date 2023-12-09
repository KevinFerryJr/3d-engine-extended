import math
import numpy
from config import SCREEN_HEIGHT, SCREEN_WIDTH

aspect_ratio = SCREEN_WIDTH/SCREEN_HEIGHT
fov_angle = 90
fov = 1.0 / math.tan(fov_angle/2.0)
z_far = 20
z_near = 3


# Precalculated starting points for a cube
points = [
(342.5, 257.5),
(342.5, 222.5),
(377.5, 222.5),
(377.5, 257.5),
(325, 275),
(325, 205),
(395, 205),
(395, 275)
]

unit_cube_points = [
[-1, 1, 1],
[-1, -1, 1],
[1, -1, 1],
[1, 1, 1],
[-1, 1, -1],
[-1, -1, -1],
[1, -1, -1],
[1, 1, -1]
]

def calculate_projection(points):
    
    # Make a copy of 3d points
	point_matrix = [int(point) for point in points]
	# Add 1 to the matrix array
	point_matrix.append(1)
    
    # Projection matrix formula
	projection_matrix = [
	[fov * aspect_ratio,0,0,0],
	[0,fov,0,0],
	[0,0,(z_far+z_near)/(z_far-z_near),1],
	[0,0,(2*z_near*z_far)/(z_near-z_far),0]
	]
    
    # Multiply matrices
	res = numpy.dot(point_matrix, projection_matrix)
	return res


print(calculate_projection([-5,5,5]))