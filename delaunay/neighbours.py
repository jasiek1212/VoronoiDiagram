from collections import defaultdict
from .triangle import Triangle
from .edge import Edge

class Neighbours:
    def __init__(self):
        self.edges = defaultdict(list)
    
    def put(self, triangle : Triangle):
        for edge in triangle.edges:
            self.edges[edge].append(triangle)
            assert len(self.edges[edge]) <= 2

    def remove_neighbours(self, edge : Edge):
        self.edges.pop(edge)

    def find_neighbour(self, edge : Edge, t: Triangle) -> Triangle:
        triangles = self.edges[edge]

        if len(triangles) == 1:
            return None
        if triangles[0] == t:
            return triangles[1]
        elif triangles[1] == t:
            return triangles[0]
        else:
            raise Exception("THE WHAT?")
    
    def remove_neighbour(self, edge : Edge, triangle : Triangle):
        triangles = self.edges.get(edge)
        triangles.remove(triangle)
        if len(triangles) == 0:
            self.edges.pop(edge)
    
    def print(self):
        for key, value in self.edges.items():
            print(f"{key}: {value}")

    def __str__(self):
        return ', '.join(f"{key}" for key in self.edges.keys())