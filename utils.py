import rendering
from pygame import draw
from numpy import cross
from math import sqrt

class vec3d:
    def __init__(self, coords, parent):
        self.polygon = parent
        self.x = coords[0]
        self.y = coords[1]
        self.z = coords[2]
        self.coords = (self.x,self.y,self.z)
        self.coords_2d = []
        self.world_coords = []  # Added property for world space coordinates

        
        # Initialize first 2d value
        self.update_vec3d()
        
    def update_vec3d(self):
        matrix_rotated = rendering.rotate_vec3d(self.coords, self.polygon.mesh.rotation)
        matrix_translated = rendering.translate_vec3d(matrix_rotated, self.polygon.mesh.position)
        matrix_projected = rendering.calculate_point(matrix_translated)
        matrix_adjusted = rendering.convert_to_screen_space(matrix_projected)
        
        self.world_coords = [matrix_translated[i] for i in range (3)]
        self.coords_2d = [matrix_adjusted[0], matrix_adjusted[1]]
        

class polygon:
    def __init__(self, points, parent):
        self.mesh = parent
        self.verts = [vec3d(point, self) for point in points]
        self.normal = vec3d([0,0,0],self)
        
        #Initialize normal
        self.calculate_normal()
        
    def update_polygon(self):
        for vert in self.verts:
            vert.update_vec3d()
    
    def draw_polygon(self, surface):
        # Create a list of tuples with the vert coordinates translated into screen space
        screen_points = [tuple(v.coords_2d) for v in self.verts]
        
        draw.line(surface, (0,0,0), screen_points[0], screen_points[1], 3)
        draw.line(surface, (0,0,0), screen_points[1], screen_points[2], 3)
        draw.line(surface, (0,0,0), screen_points[2], screen_points[0], 3)
        
        draw.circle(surface, (0,0,0), self.normal.coords_2d, 3)
        
    def calculate_normal(self):
        coords = [(vert.coords)for vert in self.verts]
        line_1 = []
        line_2 = []
        for i in range (len(coords[0])):
            line_1.append(coords[1][i] - coords[0][i])
            line_2.append(coords[2][i] - coords[0][i])
        
        normal = cross(line_1, line_2)
        n_length = sqrt(pow(normal[0],2) + pow(normal[1],2) + pow(normal[2],2))
        
        for i in range(len(normal)):
            normal[i] /= n_length
        
        matrix_rotated = rendering.rotate_vec3d(normal, self.mesh.rotation)
        
        normal_rotated = [(matrix_rotated[i]) for i in range(3)]
        
        return(normal_rotated)
        
class mesh:
    def __init__(self, mesh_data, mesh_rotation = [0,0,0], mesh_position = [2,0,4]):
        self.rotation = mesh_rotation
        self.position = mesh_position
        self.polygons = self.define_mesh(mesh_data)
    
    def define_mesh(self, mesh_coords):
        polygons = [polygon(poly, self) for poly in mesh_coords]
        #return the new list of polygons
        return polygons

    def update_mesh(self):
        for poly in self.polygons:
            poly.update_polygon()
    
    def draw_mesh(self, surface):
        for poly in self.polygons:
            #If z value of our normal is less than 0
            if poly.calculate_normal()[2] < 0:
                poly.draw_polygon(surface)

unit_cube_polys = [
#South
[[-1,-1,-1],[-1,1,-1],[1,1,-1]],
[[-1,-1,-1],[1,1,-1],[1,-1,-1]],
#East
[[1,-1,-1],[1,1,-1],[1,1,1]],
[[1,-1,-1],[1,1,1],[1,-1,1]],
# # # # #North
[[1,-1,1],[1,1,1],[-1,1,1]],
[[1,-1,1],[-1,1,1],[-1,-1,1]],
# # # # #West
[[-1,-1,1],[-1,1,1],[-1,1,-1]],
[[-1,-1,1],[-1,1,-1],[-1,-1,-1]],
# # # # #Up
[[1,1,1],[1,1,-1],[-1,1,-1]],
[[1,1,1],[-1,1,-1],[-1,1,1]],
# # # # #Down
[[-1,-1,1],[-1,-1,-1],[1,-1,-1]],
[[1,-1,1],[-1,-1,1],[1,-1,-1]]
]

unit_cube_polys_centered = [
#South
[[0,0,0],[0,1,0],[1,1,0]],
[[0,0,0],[1,1,0],[1,0,0]],
#East
[[1,0,0],[1,1,0],[1,1,1]],
[[1,0,0],[1,1,1],[1,0,1]],
# # # # #North
[[1,0,1],[1,1,1],[0,1,1]],
[[1,0,1],[0,1,1],[0,0,1]],
# # # # #West
[[0,0,1],[0,1,1],[0,1,0]],
[[0,0,1],[0,1,0],[0,0,0]],
# # # # #Up
[[1,1,1],[1,1,0],[0,1,0]],
[[1,1,1],[0,1,0],[0,1,1]],
# # # # #Down
[[1,0,0],[0,0,0],[0,0,1]],
[[1,0,0],[0,0,1],[1,0,1]]
]

cube_mesh = mesh(unit_cube_polys)
