from edge import Edge
from triangle import Triangle
from util import *

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