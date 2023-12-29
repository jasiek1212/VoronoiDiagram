from edge import Edge
from point import Point
from neighbours import Neighbours
from triangle import Triangle
from typing import List
from util import *

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