from math import sqrt
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
        
        self.neighbours = [None] * 3

        self.edges_to_neighbours = {[self.a, self.b] : self.neighbours[0],
                                    [self.b, self.c] : self.neighbours[1],
                                    [self.c, self.a] : self.neighbours[2]}


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


def dist(p1: Point, p2: Point) -> float:
    return sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)


def get_next_triangle(curr_triangle: Triangle, p: Point) -> Triangle:
    best_dist = float("inf")
    best_edge = None

    for edge in curr_triangle.edges:
        centre = get_edge_centre(edge)
        if best_dist > dist(centre, p):
            best_edge = edge
    
    return curr_triangle.edges_to_neighbours[best_edge]


class Delaunay_Triangulation:
    # class responsible for algorithm

    def __init__(self) -> None:
        # list of Triangles
        self.triangulation = []

        # TODO implement initial biggest triangle containing all of the points
    
    def add_point(self, p: Point) -> Triangle:
        # returns triangle which contains p after adding p to triangulation

        if len(self.triangulation) == 1:
            return self.triangulation[0]
        
        curr_triangle = random.choice(self.triangulation)

        while(not p.is_in_triangle(curr_triangle)):
            curr_triangle = get_next_triangle(curr_triangle)
        
        return curr_triangle






