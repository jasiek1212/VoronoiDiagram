class Edge:
    def __init__(self, p1, p2):
        if p1.x < p2.x or (p1.x == p2.x and p1.y < p2.y):
            self.p1 = p1
            self.p2 = p2
        else:
            self.p1 = p2
            self.p2 = p1

    def __str__(self) -> str:
        return f"Edge({self.p1}, {self.p2})"
    
    def __hash__(self):
        return hash((self.p1,self.p2))
    
    def __eq__(self,edge):
        if isinstance(edge,Edge):
            if self.p1 == edge.p1 and self.p2 == edge.p2: return True
            return False
        return False