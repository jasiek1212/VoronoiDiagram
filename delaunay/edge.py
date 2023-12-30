from .point import Point

class Edge:
    def __init__(self, p1: Point, p2: Point):
        if p1.x < p2.x or (p1.x == p2.x and p1.y < p2.y):
            self.p1 = p1
            self.p2 = p2
        else:
            self.p1 = p2
            self.p2 = p1

    def __str__(self) -> str:
        return f"Edge({self.p1}, {self.p2})"
    
    def __hash__(self):
        return hash((self.p1, self.p2))
    
    def __eq__(self, edge: "Edge"):
        if isinstance(edge, Edge):
            if self.p1 == edge.p1 and self.p2 == edge.p2: return True
            return False
        return False

    def get_centre(self) -> Point:
        p1 = self.p1
        p2 = self.p2

        x = (p2.x - p1.x) / 2
        y = (p2.y - p1.y) / 2 if p2.y > p1.y else (p1.y - p2.y) / 2

        return Point(x, y)