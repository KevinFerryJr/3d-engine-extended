import math
import numpy
from config import SCREEN_HEIGHT, SCREEN_WIDTH

aspect_ratio = SCREEN_WIDTH / SCREEN_HEIGHT
fov_angle = math.radians(90)
fov = 1.0 / math.tan(fov_angle / 2.0)
z_far = 1000
z_near = 0.1

# convert a 3d point to screen space (2d)
def calculate_point(point_matrix):

    projection_matrix = [
        [1/fov, 0, 0, 0],
        [0,1/-fov * aspect_ratio, 0, 0],
        [0, 0, (z_far + z_near) / (z_far - z_near), 1],
        [0, 0, (2 * z_near * z_far) / (z_near - z_far), 0]
    ]
    
    # Multiply matrices
    res = numpy.dot(point_matrix, projection_matrix)
    return res

def convert_to_screen_space(coords):
    x, y, w = coords[0], coords[1], coords[3]
    
    # Position the coordinates relative to screen space
    new_x = (x * SCREEN_WIDTH) / (2.0 * w) + (SCREEN_WIDTH / 2)
    new_y = (y * SCREEN_HEIGHT) / (2.0 * w) + (SCREEN_HEIGHT / 2)
    
    return [new_x, new_y]

def rotate_vec3d(coords, rotation):
    # Convert angles from degrees to radians
    rotation = numpy.radians(rotation)
    coord_mat = [(coord) for coord in coords]
    coord_mat.append(1)

    # Z-axis rotation matrix
    z_rotation_matrix = numpy.array([
        [math.cos(rotation[2]), -math.sin(rotation[2]), 0, 0],
        [math.sin(rotation[2]), math.cos(rotation[2]), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

    # X-axis rotation matrix
    x_rotation_matrix = numpy.array([
        [1, 0, 0, 0],
        [0, math.cos(rotation[0] * 0.5), -math.sin(rotation[0] * 0.5), 0],
        [0, math.sin(rotation[0] * 0.5), math.cos(rotation[0] * 0.5), 0],
        [0, 0, 0, 1]
    ])

    # Y-axis rotation matrix
    y_rotation_matrix = numpy.array([
        [math.cos(rotation[1]), 0, math.sin(rotation[1]), 0],
        [0, 1, 0, 0],
        [-math.sin(rotation[1]), 0, math.cos(rotation[1]), 0],
        [0, 0, 0, 1]
    ])

    # Combine rotation matrices
    combined_rotation = numpy.dot(z_rotation_matrix, numpy.dot(x_rotation_matrix, y_rotation_matrix))

    # Apply rotation
    rotated_point = numpy.dot(combined_rotation, coord_mat)
    return rotated_point

def translate_vec3d(coord_mat, trans):
    trans_vecs = [(t) for t in trans]
    trans_vecs.append(1)
    
    if len(coord_mat) < 4:
        coord_mat.append(1)
    
    translate_matrix =[
    [1,0,0,0],
    [0,1,0,0],
    [0,0,1,1],
    [trans[0],trans[1],trans[2],0]
    ]
    
    translated_coord = numpy.dot(coord_mat, translate_matrix)
    
    return translated_coord