from .edge import Edge
from .point import Point, orientation

class Triangle:
    def __init__(self, a, b, c) -> None:
        # coutnerclockwise
        if orientation(a, b, c) == 2:
            self.a = a
            self.b = b
            self.c = c
        else:
            self.a = a
            self.b = c
            self.c = b

        self.edges = [Edge(self.a, self.b),
                      Edge(self.b, self.c),
                      Edge(self.c, self.a)]
    

    def circumcircle_contains(self, point: Point) -> bool:
        a, b, c = self.a, self.b, self.c
        det = mat_det_3x3(a, b, c, point)

        return det > 0
    

    def point_in_triangle(self, point: Point) -> bool:
        a, b, c = self.a, self.b, self.c

        d1 = sign(point, a, b)
        d2 = sign(point, b, c)
        d3 = sign(point, c, a)

        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

        return not (has_neg and has_pos)
        

    def __str__(self):
        return f"Triangle({self.a}, {self.b}, {self.c})"
    
    # overwrites == comparator, equivalent of Java's equals() override
    def __eq__(self,other):
        if(isinstance(other,Triangle)):
            #points might be in different order
            temp = set()
            temp.add(self.a)
            temp.add(self.b)
            temp.add(self.c)
            temp.add(other.a)
            temp.add(other.b)
            temp.add(other.c)
            if len(temp) == 3:
                return True
            return False
        print("Comparing wrong objects - triangle")
        return False
    
    def __hash__(self):
        return hash((self.a, self.b, self.c))
    
    def contains(self, list):
        for p in list:
            if self.a == p or self.b == p or self.c == p: return True
        return False


def sign(p1: Point, p2: Point, p3: Point) -> float:
    return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)


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




