from .point import Point, orientation
from .triangle import Triangle
from .neighbours import Neighbours
from .edge import Edge
from typing import List, Tuple
from math import log10, inf

class DelaunayTriangulation:
    # class responsible for algorithm

    def __init__(self, points) -> None:
        # list of Triangles
        self.points = points
        t1, t2 = gen_init_triangles(points)
        self.boundaries = [t1.a,t1.b,t1.c,t2.c]
        self.triangulation = {t1,t2}
        self.neighbours = Neighbours()
        self.neighbours.put(t1)
        self.neighbours.put(t2)
        self.inittriangle = t1

    def add(self, triangle : Triangle):
        self.triangulation.add(triangle)
        self.neighbours.put(triangle)

    def find_triangle(self, p: Point) -> Triangle:
        # returns triangle which contains p after adding p to triangulation
        curr_triangle = self.inittriangle

        while not curr_triangle.point_in_triangle(p):
            curr_triangle = find_next_triangle(self.neighbours,curr_triangle,p)
        
        return curr_triangle
    
    def find_neighbourhood(self, p : Point, curr : Triangle, visited : set, edge : Edge = None, neighbourhood : List = [], hull : List = []):
        visited.add(curr)
        if curr.circumcircle_contains(p):
            neighbourhood.append(curr)
        else: 
            hull.append(edge)
            return neighbourhood, hull, visited
        for i in range(3):
            neighbour = self.neighbours.find_neighbour(curr.edges[i],curr)
            if neighbour is not None and neighbour not in visited:
                neighbourhood, hull, visited = self.find_neighbourhood(p, neighbour, visited, curr.edges[i], neighbourhood, hull )
            elif neighbour is None:
                hull.append(curr.edges[i])
        return neighbourhood, hull, visited

    def delete_neighbourhood(self, neighbourhood) -> None:
        for triangle in neighbourhood:
            for i in range(3):
                self.neighbours.remove_neighbour(triangle.edges[i], triangle)
            self.triangulation.remove(triangle)
 
    def rebuild_neighbourhood(self, p : Point, hull):
        for edge in hull:
            t = Triangle(edge.p1,edge.p2,p)
            self.add(t)
        self.inittriangle = t

    def print_tri(self):
        return ', '.join(f"{triangle}" for triangle in list(self.triangulation))

    def triangulate(self):
        for point in self.points:
            curr = self.find_triangle(point)
            neighbourhood, hull = self.find_neighbourhood(point, curr, {})

    def clean_up(self):
        triangles = list(self.triangulation)
        for triangle in triangles:
            if triangle.contains(self.boundaries):
                for edge in triangle.edges:
                    self.neighbours.remove_neighbour(edge,triangle)
                self.triangulation.remove(triangle)


def find_next_triangle(neighbours : Neighbours, curr_triangle : Triangle, p : Point) -> Triangle:
    neighbour = neighbours.find_neighbour(curr_triangle.edges[0],curr_triangle)
    if orientation(curr_triangle.a,curr_triangle.b,p) == 1 and neighbour is not None: 
        return neighbour
    neighbour = neighbours.find_neighbour(curr_triangle.edges[1],curr_triangle)
    if orientation(curr_triangle.b,curr_triangle.c,p) == 1 and neighbour is not None: 
        return neighbour
    neighbour = neighbours.find_neighbour(curr_triangle.edges[2],curr_triangle)
    if orientation(curr_triangle.c,curr_triangle.a,p) == 1 and neighbour is not None: 
        return neighbour
    raise Exception("AAAAAAa")


def gen_init_triangles(points: List[Point]) -> Tuple[Triangle, Triangle]:
    min_x,min_y = inf,inf
    max_x, max_y = -inf,-inf 
    for i in range(len(points)):
        curr = points[i]
        max_x = max(curr.x,max_x)
        min_x = min(curr.x,min_x)
        max_y = max(curr.y,max_y)
        min_y = min(curr.y,min_y)
    magnitude = 10*max(log10(abs(max_y)),log10(abs(max_x)),log10(abs(min_x)),log10(abs(min_y)))
    bl,br = Point(min_x-magnitude,min_y-magnitude), Point(max_x+magnitude,min_y-magnitude)
    tr,tl = Point(max_x+magnitude,max_y+magnitude), Point(min_x-magnitude,max_y+magnitude)
    t1 = Triangle(bl,br,tr)
    t2 = Triangle(bl,tr,tl)
    return t1,t2