from util import *

class Triangle:
    def __init__(self, a, b, c) -> None:
        # coutnerclockwise
        if orientation(a,b,c) == 2:
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
    
    def contains(self,list):
        for p in list:
            if self.a == p or self.b == p or self.c == p: return True
        return False