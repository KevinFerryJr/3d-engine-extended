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
        matrix_projected = rendering.calculate_point(matrix_translated)
        matrix_adjusted = rendering.convert_to_screen_space(matrix_projected)
        
        self.world_coords = [matrix_translated[i] for i in range(3)]
        self.coords_2d = [matrix_adjusted[0], matrix_adjusted[1]]

class Polygon:
    def __init__(self, points, parent):
        self.mesh = parent
        self.verts = [Vec3D(point, self) for point in points]
        self.normal = Vec3D([0, 0, 0], self)
        
        # Initialize normal
        self.calculate_normal()
        
    def update_polygon(self):
        for vert in self.verts:
            if self.is_facing():
                vert.update_vec3d()
    
    def draw_polygon(self, surface):
        # Check if we should be rendering this polygon
        if self.is_facing():
        
            # Create a list of tuples with the vert coordinates translated into screen space
            screen_points = [tuple(v.coords_2d) for v in self.verts]
            
            # Draw the wire frame
            # draw.line(surface, config.LINE_COLOR, screen_points[0], screen_points[1], 3)
            # draw.line(surface, config.LINE_COLOR, screen_points[1], screen_points[2], 3)
            # draw.line(surface, config.LINE_COLOR, screen_points[2], screen_points[0], 3)
            
            poly_color = self.calculate_shading()
            draw.polygon(surface, poly_color, [(v.coords_2d) for v in self.verts])
        
    def is_facing(self):
        coords = self.verts[0].world_coords
        normal = self.calculate_normal()
        normal_matrix = [
            ([coords[i] - viewport.position[i], 0, 0]) for i in range(3)
        ]
        
        result = numpy.dot(normal, normal_matrix)[0]
        if result < 0:
            return True
        else:
            return False
    
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
        normal_direction = [self.calculate_normal()[i] for i in range(3)]
        
        # Calculate the difference between our normal and our light direction
        color_scalar = numpy.dot(normal_direction, light_direction)
        color_scalar_normalized = ((color_scalar / l_length) + 1) / 2

        shade = color_scalar_normalized * 255
        poly_color = [shade, shade, shade]
        return poly_color

class Mesh:
    def __init__(self, mesh_data, mesh_rotation=[0, 0, 0], mesh_position=[0, 0, 4]):
        self.rotation = mesh_rotation
        self.position = mesh_position
        self.polygons = self.define_mesh(mesh_data)
    
    def define_mesh(self, mesh_coords):
        polygons = [Polygon(poly, self) for poly in mesh_coords]
        # Return the new list of polygons
        return polygons

    def update_mesh(self):
        for poly in self.polygons:
            poly.update_polygon()
    
    def draw_mesh(self, surface):
        for poly in self.polygons:
            poly.draw_polygon(surface)

class Camera:
    def __init__(self):
        self.position = [0, 0, 0]

viewport = Camera()

unit_cube_polys = [
    # South
    [[-1, -1, -1], [-1, 1, -1], [1, 1, -1]],
    [[-1, -1, -1], [1, 1, -1], [1, -1, -1]],
    # East
    [[1, -1, -1], [1, 1, -1], [1, 1, 1]],
    [[1, -1, -1], [1, 1, 1], [1, -1, 1]],
    # North
    [[1, -1, 1], [1, 1, 1], [-1, 1, 1]],
    [[1, -1, 1], [-1, 1, 1], [-1, -1, 1]],
    # West
    [[-1, -1, 1], [-1, 1, 1], [-1, 1, -1]],
    [[-1, -1, 1], [-1, 1, -1], [-1, -1, -1]],
    # Up
    [[1, 1, 1], [1, 1, -1], [-1, 1, -1]],
    [[1, 1, 1], [-1, 1, -1], [-1, 1, 1]],
    # Down
    [[-1, -1, 1], [-1, -1, -1], [1, -1, -1]],
    [[1, -1, 1], [-1, -1, 1], [1, -1, -1]]
]

unit_cube_polys_centered = [
    # South
    [[0, 0, 0], [0, 1, 0], [1, 1, 0]],
    [[0, 0, 0], [1, 1, 0], [1, 0, 0]],
    # East
    [[1, 0, 0], [1, 1, 0], [1, 1, 1]],
    [[1, 0, 0], [1, 1, 1], [1, 0, 1]],
    # North
    [[1, 0, 1], [1, 1, 1], [0, 1, 1]],
    [[1, 0, 1], [0, 1, 1], [0, 0, 1]],
    # West
    [[0, 0, 1], [0, 1, 1], [0, 1, 0]],
    [[0, 0, 1], [0, 1, 0], [0, 0, 0]],
    # Up
    [[1, 1, 1], [1, 1, 0], [0, 1, 0]],
    [[1, 1, 1], [0, 1, 0], [0, 1, 1]],
    # Down
    [[1, 0, 0], [0, 0, 0], [0, 0, 1]],
    [[1, 0, 0], [0, 0, 1], [1, 0, 1]]
]

viewport = Camera()
cube_mesh = Mesh(rendering.read_obj_file("monkey.obj"))

