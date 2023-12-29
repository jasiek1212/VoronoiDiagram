from point import Point
from neighbours import Neighbours
from triangle import Triangle
from typing import List
from util import *

class Voronoi_Diagram:
    def __init__(self, points : List[Point], neighbours : Neighbours, triangulation : List[Triangle]) -> None:
        self.points = points
        self.neighbours = neighbours
        self.triangles = triangulation