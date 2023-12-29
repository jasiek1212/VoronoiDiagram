from triangle import Triangle
from util import *


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