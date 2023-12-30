from typing import List
from .point import Point
from .neighbours import Neighbours

class Voronoi_Diagram:
    def __init__(self, points : List[Point], neighbours : Neighbours, triangulation : List[Triangle]) -> None:
        self.points = points
        self.neighbours = neighbours
        self.triangles = triangulation