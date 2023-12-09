import math
import numpy
from config import SCREEN_HEIGHT, SCREEN_WIDTH

aspect_ratio = SCREEN_WIDTH/SCREEN_HEIGHT
fov = 90


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

original_points = [
[-1, 1, 1],
[-1, -1, 1],
[1, -1, 1],
[1, 1, 1],
[-1, 1, -1],
[-1, -1, -1],
[1, -1, -1],
[1, 1, -1]
]

# Updated list of points are sotred here
rotated_3d_points = [list(point) for point in original_points]

def calculate_projection(points):
    
    # Make a copy of 3d points
	point_matrix = [int(point) for point in points]
	# Add 1 to the matrix array
	point_matrix.append(1)
    
    # Projection matrix formula
	projection_matrix = [
	[1,0,0,0],
	[0,1,0,0],
	[0,0,1,0],
	[0,0,1,0]
	]
    
	res = numpy.dot(point_matrix, projection_matrix)
    
	return res


print(calculate_projection([1,2,3]))