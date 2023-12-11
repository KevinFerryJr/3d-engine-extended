from rendering import calculate_point, convert_to_screen_space
from pygame import draw

class vec3d:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.coord = (self.x,self.y,self.z)
        self.coord_trans = self.update_vec3d()
        
    def update_vec3d(self):
        point2d = calculate_point(self.coord)
        point2d = convert_to_screen_space(point2d)
        return (point2d[0], point2d[1])

class polygon:
    def __init__(self, points):
        self.verts = points
        
    def draw_polygon(self, surface):
        # Create a list of tuples with the vert coordinates translated into screen space
        screen_points = [tuple(v.coord_trans) for v in self.verts]
        
        draw.line(surface, (0,0,0), screen_points[0], screen_points[1], 3)
        draw.line(surface, (0,0,0), screen_points[1], screen_points[2], 3)
        draw.line(surface, (0,0,0), screen_points[2], screen_points[0], 3)
        

class mesh:
    def __init__(self, mesh_data):
        self.polygons = self.define_mesh(mesh_data)
    
    def define_mesh(self, mesh_data):
        # Container for all polygons in the mesh
        polygons = []
        # Loop through all the polygon point groups
        for poly in mesh_data:
            # container for new polygons vec3s
            poly_data = []
            #loop through all the points in the group
            for point in poly:
                new_vec = vec3d(point[0],point[1],point[2])
                poly_data.append(new_vec)
            
            # Init new poly and append it to the list
            new_polygon = polygon(poly_data)
            print(new_polygon)
            polygons.append(new_polygon)
            
        #return the new list of polygons
        return polygons
            
    def draw_mesh(self, surface):
        for poly in self.polygons:
            # print(poly)
            poly.draw_polygon(surface)
            

unit_cube_polys = [
#South
[[-1,-1,3],[-1,1,3],[1,1,3]],
[[-1,-1,3],[1,1,3],[1,-1,3]],
#East
[[1,-1,3],[1,1,3],[1,1,5]],
[[1,-1,3],[1,1,5],[1,-1,5]],
# # # # #North
[[1,-1,5],[1,1,5],[-1,1,5]],
[[1,-1,5],[-1,1,5],[-1,-1,5]],
# # # # #West
[[-1,-1,5],[-1,1,5],[-1,1,3]],
[[-1,-1,5],[-1,1,3],[-1,-1,3]],
# # # # #Up
[[1,1,3],[1,1,5],[-1,1,5]],
[[1,1,3],[-1,1,5],[-1,1,3]],
# # # # #Down
[[1,-1,5],[-1,-1,3],[1,-1,3]],
[[1,-1,5],[-1,-1,3],[-1,-1,5]]
]

cube_mesh = mesh(unit_cube_polys)
