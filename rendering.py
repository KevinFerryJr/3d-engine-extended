import math
import numpy
from config import SCREEN_HEIGHT, SCREEN_WIDTH
import os

# Constants for projection
aspect_ratio = SCREEN_WIDTH / SCREEN_HEIGHT
fov_angle = math.radians(90)
fov = 1.0 / math.tan(fov_angle / 2.0)
fov_inv = 1.0 / fov
z_far = 1000
z_near = 0.1

def calculate_point(point_matrix):
    #Common Matrices
    projection_matrix = [
    [fov_inv, 0, 0, 0],
    [0, 1 / -fov * aspect_ratio, 0, 0],
    [0, 0, (z_far + z_near) / (z_near - z_far), 1],
    [0, 0, (2 * z_near * z_far) / (z_near - z_far), 0]
    ]
    
    # Multiply matrices
    res = numpy.dot(point_matrix, projection_matrix)
    return res

# Function to convert coordinates to screen space
def convert_to_screen_space(coords):
    x, y, w = coords[0], coords[1], coords[3]
    
    # Position the coordinates relative to screen space
    new_x = (x * SCREEN_WIDTH) / (2.0 * w) + (SCREEN_WIDTH / 2)
    new_y = (y * SCREEN_HEIGHT) / (2.0 * w) + (SCREEN_HEIGHT / 2)
    
    return [new_x, new_y]

# Function to rotate a 3D point in space
def rotate_vec3d(coords, rotation):
    # Convert angles from degrees to radians
    rotation = numpy.radians(rotation)
    coord_mat = numpy.append(coords, 1)

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

# Function to translate a 3D point
def translate_vec3d(coord_mat, trans):
    if len(coord_mat) < 4:
        coord_mat = numpy.append(coord_mat, 1)
    
    translate_matrix = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 1],
        [trans[0], trans[1], trans[2], 0]
    ]
    
    # Apply translation
    translated_coord = numpy.dot(coord_mat, translate_matrix)
    return translated_coord

# Convert an obj file into readable mesh data
def read_obj_file(file_name):
    file_path = os.path.join('models', file_name)
    points = []
    faces = []  # List to store coordinates for the current face
        
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith('v'):
                # Extracting vertex coordinates
                _, x, y, z = line.split()
                point = [float(x), float(y), float(z)]
                points.append(point)
            elif line.startswith('f'):
                _, x, y, z = line.split()
                x = int(x) -1
                y = int(y) -1
                z = int(z) -1
                current_face = [points[x],points[y], points[z]]
                faces.append(current_face)

    return faces