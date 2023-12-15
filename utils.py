import rendering
from pygame import draw
import numpy
from math import sqrt
import config

class Vec3D:
    def __init__(self, coords, parent):
        self.polygon = parent
        self.x, self.y, self.z = coords
        self.coords = (self.x, self.y, self.z)
        self.coords_2d = []
        self.world_coords = []  # Property for world space coordinates
        
        # Initialize first 2D value
        self.update_vec3d()
        
    def update_vec3d(self):
        matrix_rotated = rendering.rotate_vec3d(self.coords, self.polygon.mesh.rotation)
        matrix_translated = rendering.translate_vec3d(matrix_rotated, self.polygon.mesh.position)
        self.world_coords = [matrix_translated[i] for i in range(3)]
        
        if self.polygon.facing:
            matrix_projected = rendering.calculate_point(matrix_translated)
            matrix_adjusted = rendering.convert_to_screen_space(matrix_projected)
            self.coords_2d = [matrix_adjusted[0], matrix_adjusted[1]]

class Polygon:
    def __init__(self, points, parent):
        self.mesh = parent
        self.normal = [0,0,0]
        self.facing = False
        self.verts = [Vec3D(point, self) for point in points]
        self.z_depth = [0,0,0]
        self.update_polygon()
        
    def update_polygon(self):
        self.normal = self.calculate_normal()
        self.facing = self.is_facing()
        self.z_depth = self.calculate_z_depth()
        for vert in self.verts:
                vert.update_vec3d()
    
    def draw_polygon(self, surface):
        # Check if we should be rendering this polygon
        if self.facing:
            poly_color = self.calculate_shading()
            draw.polygon(surface, poly_color, [(v.coords_2d) for v in self.verts])
        
    def is_facing(self):
        coords = self.verts[0].world_coords
        normal_matrix = [
            ([coords[i] - viewport.position[i], 0, 0]) for i in range(3)
        ]
        
        result = numpy.dot(self.normal, normal_matrix)[0]
        if result < 0:
            return True
        else:
            return False
    
    def calculate_z_depth(self):
        z_coords = [(v.world_coords[2]) for v in self.verts]
        new_z_depth = 0

        for c in z_coords:
            new_z_depth += c
            
        new_z_depth /= 3
        return new_z_depth
    
    def calculate_normal(self):
        coords = [vert.coords for vert in self.verts]
        line_1 = [coords[1][i] - coords[0][i] for i in range(len(coords[0]))]
        line_2 = [coords[2][i] - coords[0][i] for i in range(len(coords[0]))]
        
        normal = numpy.cross(line_1, line_2)
        matrix_rotated = rendering.rotate_vec3d(normal, self.mesh.rotation)
        
        n_length = sqrt(pow(normal[0], 2) + pow(normal[1], 2) + pow(normal[2], 2))
        
        normal_rotated = [(matrix_rotated[i] / n_length) for i in range(3)]
        
        return normal_rotated
    
    def calculate_shading(self):
        # Define a light direction and get its length
        light_direction = [0, 0, -1]
        l_length = sqrt(pow(light_direction[0], 2) + pow(light_direction[1], 2) + pow(light_direction[2], 2))
        
        # Normalize light direction
        light_direction = [coord / l_length for coord in light_direction]
        
        # Get current normal direction
        normal_direction = [self.normal[i] for i in range(3)]
        
        # Calculate the difference between our normal and our light direction
        color_scalar = numpy.dot(normal_direction, light_direction)
        color_scalar_normalized = ((color_scalar / l_length) + 1) / 2

        shade = color_scalar_normalized * 230 + 25
        poly_color = [shade, shade, shade]
        return poly_color

class Mesh:
    def __init__(self, mesh_data, name="unknown", mesh_rotation=[0, 0, 0], mesh_position=[0, 0, 4]):
        self.name = name
        self.rotation = mesh_rotation
        self.position = mesh_position
        self.polygons = self.define_mesh(mesh_data)
    
    def define_mesh(self, mesh_coords):
        polygons = [Polygon(poly, self) for poly in mesh_coords]
        # Return the new list of polygons
        return polygons

    def update_mesh(self):
        # Sort polygons from furthest to nearest
        self.polygons.sort(key=lambda poly: poly.z_depth, reverse=True)
        # Update all the polygons in order
        for poly in self.polygons:
            poly.update_polygon()
    
    def draw_mesh(self, surface):
        for poly in self.polygons:
            poly.draw_polygon(surface)

class Camera:
    def __init__(self):
        self.position = [0, 0, 0]

# Create a single instance of the Camera
viewport = Camera()

sphere_mesh = Mesh(rendering.read_obj_file("sphere.obj"),"sphere",[0,0,0],[0,0,4])
cube_mesh = Mesh(rendering.read_obj_file("cube.obj"),"cube",[0,0,0],[0,0,4])
meshes = [sphere_mesh, cube_mesh]