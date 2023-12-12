from rendering import calculate_point, convert_to_screen_space
from pygame import draw

class vec3d:
    def __init__(self, coords, parent):
        self.polygon = parent
        self.x = coords[0]
        self.y = coords[1]
        self.z = coords[2]
        self.coords = (self.x,self.y,self.z)
        self.coords_2d = []
        
        # Initialize first 2d value
        self.update_vec3d()
        
    def update_vec3d(self):
        point2d = calculate_point(self)
        point2d = convert_to_screen_space(point2d)
        res = [point2d[0], point2d[1]]
        self.coords_2d = res

class polygon:
    def __init__(self, points, parent):
        self.mesh = parent
        self.verts = [vec3d(point, self) for point in points]
        
    def update_polygon(self):
        for vert in self.verts:
            vert.update_vec3d()
    
    def draw_polygon(self, surface):
        # Create a list of tuples with the vert coordinates translated into screen space
        screen_points = [tuple(v.coords_2d) for v in self.verts]
        
        draw.line(surface, (0,0,0), screen_points[0], screen_points[1], 3)
        draw.line(surface, (0,0,0), screen_points[1], screen_points[2], 3)
        draw.line(surface, (0,0,0), screen_points[2], screen_points[0], 3)
        

class mesh:
    def __init__(self, mesh_data, mesh_rotation = [30,0,0], mesh_position = [0,0,4]):
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
[[1,1,-1],[1,1,1],[-1,1,1]],
[[1,1,-1],[-1,1,1],[-1,1,-1]],
# # # # #Down
[[1,-1,1],[-1,-1,-1],[1,-1,-1]],
[[1,-1,1],[-1,-1,-1],[-1,-1,1]]
]

cube_mesh = mesh(unit_cube_polys)
