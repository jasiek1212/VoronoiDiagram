from typing import Optional
from .point import Point

class Edge:
    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def __str__(self) -> str:
        return f"Edge({self.p1}, {self.p2})"
    
    def __hash__(self):
        if self.p1.x < self.p2.x or (self.p1.x == self.p2.x and self.p1.y < self.p2.y):
            return hash((self.p1, self.p2))
        else:
            return hash((self.p2, self.p1))
    
    def __eq__(self, edge: "Edge"):
        if isinstance(edge, Edge):
            return (self.p1 == edge.p1 and self.p2 == edge.p2) or \
                (self.p1 == edge.p2 and self.p2 == edge.p1)
        raise Exception("Comparing Edge with non-Edge")

    def get_centre(self) -> Point:
        p1 = self.p1
        p2 = self.p2

        x = (p2.x + p1.x) / 2
        y = (p2.y + p1.y) / 2

        return Point(x, y)

    def get_slope(self):
        x1, y1 = self.p1.x, self.p1.y
        x2, y2 = self.p2.x, self.p2.y

        slope = (y2 - y1) / (x2 - x1)
        return slope
    
    def get_linear_equation_coefficients(self):
        x1, y1 = self.p1.x, self.p1.y
        x2, y2 = self.p2.x, self.p2.y

        a = y1 - y2
        b = x2 - x1
        c = x1 * y2 - x2 * y1

        return a, b, c
    

    def get_perpendicular_bisector(self):
        a, b, c = self.get_linear_equation_coefficients()

        new_a = b
        new_b = -a
        center = self.get_centre()
        new_c = - new_a * center.x - new_b * center.y

        return new_a, new_b, new_c


def find_intersection(a1, b1, c1, a2, b2, c2) -> Optional[Point]:
    main_det = a1 * b2 - b1 * a2
    if main_det == 0:
        return None
    
    x_det = - c1 * b2 + c2 * b1
    y_det = - a1 * c2 + a2 * c1

    return Point(x_det / main_det, y_det / main_det)

def linePoints(a=0,b=0,c=0,ref = [-0.001, 0.001]):
    """given a,b,c for straight line as ax+by+c=0, 
    return a pair of points based on ref values
    e.g linePoints(-1,1,2) == [(-1.0, -3.0), (1.0, -1.0)]
    """
    if (a==0 and b==0):
        raise Exception("linePoints: a and b cannot both be zero")
    return [(-c/a,p) if b==0 else (p,(-c-a*p)/b) for p in ref]
