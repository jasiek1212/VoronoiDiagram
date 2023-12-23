from math import sqrt, inf, log10
from typing import List
import random

class Triangle:
    def __init__(self, a, b, c) -> None:
        # coutnerclockwise
        self.a = a
        self.b = b
        self.c = c

        self.edges = [[self.a, self.b],
                      [self.b, self.c],
                      [self.c, self.a]]
    
    # overwrites == comparator, equivalent of Java's equals() override
    def __eq__(self,other ) -> bool:
        if(isinstance(other,Triangle)):
            #points might be in different order
            temp = {}
            temp.update(self.a)
            temp.update(self.b)
            temp.update(self.c)
            temp.update(other.a)
            temp.update(other.b)
            temp.update(other.c)
            if len(temp) == 3:
                return True
            return False
        print("Comparing wrong objects - triangle")
        return False



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
    
    def __eq__(self,point):
        if isinstance(point,Point):
            if self.x == point.x and self.y == point.y: return True
            return False
        print("Comparing wrong objects - point")
        return False
    
class Neighbours:
    def __init__(self) -> None:
        self.edges = {}

    def put(self,edge,T1 : Triangle, T2 : Triangle):
        self.edges.update({edge : (T1,T2)})
    
    def remove_neighbours(self, edge : tuple(Point,Point)):
        self.edges.pop(edge)

    def findNeighbour(self, edge : tuple(Point,Point), T1: Triangle) -> Triangle:
        if self.edges.get(edge)[0] == T1: return self.edges.get(edge)[1]
        else: return self.edges.get[edge][0]


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


def get_edge_centre(edge: tuple[Point, Point]) -> Point:
    p1 = edge[0]
    p2 = edge[1]

    x = (p2.x - p1.x) / 2 if p2.x > p1.x else (p1.x - p2.x) / 2
    y = (p2.y - p1.y) / 2 if p2.y > p1.y else (p1.y - p2.y) / 2

    return Point(x, y)


def distSq(p1: Point, p2: Point) -> float: #nie ma sensu liczyć pierwiastka, szkoda czasu
    return (p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2


def get_next_triangle(neighbours : Neighbours, curr_triangle: Triangle, p: Point) -> Triangle:
    best_dist = float("inf")
    best_edge = None

    for edge in curr_triangle.edges:
        centre = get_edge_centre(edge)
        if best_dist > distSq(centre, p):
            best_edge = edge
    
    return neighbours.findNeighbour(best_edge, curr_triangle)

def gen_init_triangles(points: List[Point]) -> tuple(Triangle,Triangle,tuple(Point,Point)):
    min_x,min_y = inf,inf
    max_x, max_y = -inf,-inf 
    for i in range(len(points)):
        curr = points[i]
        max_x = max(curr.x,max_x)
        min_x = min(curr.x,min_x)
        max_y = max(curr.y,max_y)
        min_y = min(curr.y,min_y)
    magnitude = max(log10(abs(max_y)),log10(abs(max_x)),log10(abs(min_x)),log10(abs(min_y)))
    br,bl = Point(min_x-magnitude,min_y-magnitude), Point(max_x+magnitude,min_y-magnitude)
    tr,tl = Point(max_x+magnitude,max_y+magnitude), Point(min_x-magnitude,max_y+magnitude)
    t1 = Triangle(bl,br,tr)
    t2 = Triangle(bl,tr,tl)
    diagonal = (bl,tr)
    return t1,t2,diagonal


class Delaunay_Triangulation:
    # class responsible for algorithm

    def __init__(self, points : List[Point]) -> None:
        # list of Triangles
        t1, t2, diagonal = gen_init_triangles(points)
        self.triangulation = [t1,t2]
        # dictionary edge : T1, T2 where T1 neighbours T2 with edge
        self.neighbours = Neighbours()
        self.neighbours.put(diagonal,t1,t2)

    def add_point(self, p: Point) -> Triangle:
        # returns triangle which contains p after adding p to triangulation
        curr_triangle = random.choice(self.triangulation)

        while not p.is_in_triangle(curr_triangle):
            curr_triangle = get_next_triangle(curr_triangle)
        
        return curr_triangle






