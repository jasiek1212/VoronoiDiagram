class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def get(self):
        return (self.x, self.y)
    
    def __str__(self) -> str:
        return f"Point({self.x}, {self.y})"
    
    def __eq__(self, point):
        if isinstance(point, Point):
            if self.x == point.x and self.y == point.y: return True
            return False
        print("Comparing wrong objects - point")
        return False
    
    def __hash__(self):
        return hash((self.x, self.y))


def orientation(p1: Point, p2: Point, p3: Point): 
    det = (p2.y - p1.y)*(p3.x-p2.x) - (p2.x-p1.x)*(p3.y-p2.y)
    # det = (p.x - q.x) * (r.y - q.y) - (r.x - q.x) * (p.y - q.y)
  
    if det == 0: 
        return 0
    elif det > 0: 
        return 1
    else: 
        return 2


def distSq(p1: Point, p2: Point) -> float:
    return (p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2