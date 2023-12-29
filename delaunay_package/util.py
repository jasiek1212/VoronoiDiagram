from edge import Edge
from point import Point
from neighbours import Neighbours
from triangle import Triangle
from typing import List, Tuple
from math import inf, log10

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