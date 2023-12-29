from math import inf, log10
from typing import List, Tuple
import random

class Edge:
    def __init__(self, p1, p2):
        if p1.x < p2.x or (p1.x == p2.x and p1.y < p2.y):
            self.p1 = p1
            self.p2 = p2
        else:
            self.p1 = p2
            self.p2 = p1

    def __str__(self) -> str:
        return f"Edge({self.p1}, {self.p2})"
    
    def __hash__(self):
        return hash((self.p1,self.p2))
    
    def __eq__(self,edge):
        if isinstance(edge,Edge):
            if self.p1 == edge.p1 and self.p2 == edge.p2: return True
            return False
        return False
    



class Triangle:
    def __init__(self, a, b, c) -> None:
        # coutnerclockwise
        if orientation(a,b,c) == 2:
            self.a = a
            self.b = b
            self.c = c
        else:
            self.a = a
            self.b = c
            self.c = b

        self.edges = [Edge(self.a, self.b),
                      Edge(self.b, self.c),
                      Edge(self.c, self.a)]
        
    def __str__(self):
        return f"Triangle({self.a}, {self.b}, {self.c})"
    
    # overwrites == comparator, equivalent of Java's equals() override
    def __eq__(self,other):
        if(isinstance(other,Triangle)):
            #points might be in different order
            temp = set()
            temp.add(self.a)
            temp.add(self.b)
            temp.add(self.c)
            temp.add(other.a)
            temp.add(other.b)
            temp.add(other.c)
            if len(temp) == 3:
                return True
            return False
        print("Comparing wrong objects - triangle")
        return False
    
    def __hash__(self):
        return hash((self.a, self.b, self.c))
    
    def contains(self,list):
        for p in list:
            if self.a == p or self.b == p or self.c == p: return True
        return False
    
    

def distance(point1, point2):
    return ((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2) ** 0.5



class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
    
    def is_in_circumcircle_of(self, triangle: Triangle) -> bool:
        a, b, c = triangle.a, triangle.b, triangle.c
        det = mat_det_3x3(a, b, c, self)

        return det > 0
    

    def is_in_triangle(self, triangle: Triangle) -> bool:
        a, b, c = triangle.a, triangle.b, triangle.c

        d1 = sign(self, a, b)
        d2 = sign(self, b, c)
        d3 = sign(self, c, a)

        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

        return not (has_neg and has_pos)

    def get(self):
        return (self.x,self.y)
    
    def __str__(self) -> str:
        return f"Point({self.x}, {self.y})"
    
    def __eq__(self,point):
        if isinstance(point,Point):
            if self.x == point.x and self.y == point.y: return True
            return False
        print("Comparing wrong objects - point")
        return False
    
    def __hash__(self):
        return hash((self.x,self.y))

    
class Neighbours:
    def __init__(self):
        self.edges = {}
    
    def put(self,triangle : Triangle):
        for edge in triangle.edges:
            if self.edges.get(edge) is not None:
                self.edges.get(edge).append(triangle)
            else: self.edges[edge] = [triangle]

    def remove_neighbours(self, edge : Edge):
        self.edges.pop(edge)

    def find_neighbour(self, edge : Edge, T1: Triangle) -> Triangle:
        if len(self.edges.get(edge)) == 1: return None
        if self.edges.get(edge)[0] == T1: return self.edges.get(edge)[1]
        else: return self.edges.get(edge)[0]
    
    def remove_neighbour(self, edge : Edge, triangle : Triangle):
        self.edges.get(edge).remove(triangle)
        if len(self.edges.get(edge)) == 0:
            self.edges.pop(edge)
    
    def print(self):
        for key, value in self.edges.items():
            print(f"{key}: {value}")
            

    def __str__(self):
        return ', '.join(f"{key}" for key in self.edges.keys())



def mat_det_3x3(a: Point, b: Point, c: Point, d: Point) -> float:
    # claculate determinant to check if point d is in circumcircle of a, b, c
    # assumption: a, b, c is coutterclockwise

    det = ((a.x - d.x) * (b.y - d.y) * ((c.x - d.x) ** 2 + (c.y - d.y) ** 2)) + \
    ((a.y - d.y) * ((b.x - d.x) ** 2 + (b.y - d.y) ** 2) * (c.x - d.x)) + \
    (((a.x - d.x) ** 2 + (a.y - d.y) ** 2) * (b.x - d.x) * (c.y - d.y)) - \
    ((c.x - d.x) * (b.y - d.y) * ((a.x - d.x) ** 2 + (a.y - d.y) ** 2) + 
     ((a.y - d.y) * (b.x - d.x) * ((c.x - d.x) ** 2 + (c.y - d.y) ** 2)) + 
     (a.x - d.x) * ((b.x - d.x) ** 2 + (b.y - d.y) ** 2) * (c.y - d.y))
    
    return det


def sign(p1: Point, p2: Point, p3: Point) -> float:
    return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)


def get_edge_centre(edge: Edge) -> Point:
    p1 = edge.p1
    p2 = edge.p2

    x = (p2.x - p1.x) / 2
    y = (p2.y - p1.y) / 2 if p2.y > p1.y else (p1.y - p2.y) / 2

    return Point(x, y)


def orientation(p, q, r): 
    det = (p.x - q.x)*(r.y - q.y) - (r.x - q.x)*(p.y - q.y)
  
    if det == 0: 
        return 0
    elif det > 0: 
        return 1
    else: 
        return 2

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

def distSq(p1: Point, p2: Point) -> float: #nie ma sensu liczyć pierwiastka, szkoda czasu
    return (p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2

def get_next_triangle(neighbours : Neighbours, curr_triangle: Triangle, p: Point) -> Triangle:
    best_dist = float("inf")
    best_edge = None

    for edge in curr_triangle.edges:
        centre = get_edge_centre(edge)
        if best_dist > distSq(centre, p):
            best_edge = edge
    
    return neighbours.find_neighbour(best_edge, curr_triangle)

def gen_init_triangles(points: List[Point]) -> Tuple[Triangle,Triangle]:
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


class Delaunay_Triangulation:
    # class responsible for algorithm

    def __init__(self, points : List[Point]) -> None:
        # list of Triangles
        self.points = points
        t1, t2 = gen_init_triangles(points)
        self.boundaries = [t1.a,t1.b,t1.c,t2.c]
        self.triangulation = {t1,t2}
        self.neighbours = Neighbours()
        self.neighbours.put(t1)
        self.neighbours.put(t2)
        self.inittriangle = t1

    def add(self,triangle : Triangle):
        self.triangulation.add(triangle)
        self.neighbours.put(triangle)

    def find_triangle(self, p: Point) -> Triangle:
        # returns triangle which contains p after adding p to triangulation
        curr_triangle = self.inittriangle

        while not p.is_in_triangle(curr_triangle):
            curr_triangle = find_next_triangle(self.neighbours,curr_triangle,p)
        
        return curr_triangle
    
    def find_neighbourhood(self, p : Point, curr : Triangle, visited : set, edge : Edge = None, neighbourhood : List[Triangle] = [], hull : List[Edge] = []):
        visited.add(curr)
        if p.is_in_circumcircle_of(curr):
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
            t = Triangle(p,edge.p1,edge.p2)
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


class Voronoi_Diagrams:

    def __init__(self, points : List[Point], neighbours : Neighbours, triangulation : List[Triangle]) -> None:
        self.points = points
        self.neighbours = neighbours
        self.triangles = triangulation

    






