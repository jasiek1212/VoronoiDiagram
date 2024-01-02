from .edge import Edge, find_intersection, linePoints
from .point import Point, orientation
from visualizer.figures.polygon import Polygon
from visualizer.figures.line_segment import LineSegment
from visualizer.main import Visualizer

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
        
        if not orientation(self.a, self.b, self.c) == 2:
            raise Exception("NOT GOOD")
    

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
        raise Exception("Comparing wrong objects - triangle")
    
    def __hash__(self):
        return hash((self.a, self.b, self.c))
    
    def contains(self, list: list[Point]):
        for point in list:
            if self.a == point or self.b == point or self.c == point: return True
        return False
    
    def find_circumcenter(self) -> Point:
        first_bisector = self.edges[0].get_perpendicular_bisector()
        second_bisector = self.edges[1].get_perpendicular_bisector()

        return find_intersection(*first_bisector, *second_bisector)

    def to_point_list(self) -> list[Point]:
        return [Point(self.a.x, self.a.y), Point(self.b.x, self.b.y), Point(self.c.x, self.c.y)]

    def to_polygon(self) -> Polygon:
        return Polygon(
            data=[p.get() for p in self.to_point_list()],
            options={},
        )
    
    def to_visualisation_lines(self, vis: Visualizer, color="red") -> list[LineSegment]:
        figures = []
        for edge in self.edges:
            figures.append(vis.add_line_segment((edge.p1.get(),edge.p2.get()), color=color))
        
        return figures

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





