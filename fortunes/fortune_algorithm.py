import random
import math
import numpy as np

from .structures import Point, Event, Arc, Segment, PriorityQueue
from visualizer.main import Visualizer

class FortuneAlgorithm:
    def __init__(self, points, bound):
        self.output = []
        self.init_points = points
        self.arc = None 
        self.bound = bound

        self.points = PriorityQueue()
        self.event = PriorityQueue()

        
        self.x0 = -50.0
        self.x1 = -50.0
        self.y0 = 550.0
        self.y1 = 550.0

        
        for point in points:
            self.points.push(point)
            if point.x < self.x0: self.x0 = point.x
            if point.y < self.y0: self.y0 = point.y
            if point.x > self.x1: self.x1 = point.x
            if point.y > self.y1: self.y1 = point.y

        dx = (self.x1 - self.x0 + 1) / 5.0
        dy = (self.y1 - self.y0 + 1) / 5.0
        self.x0 = self.x0 - dx
        self.x1 = self.x1 + dx
        self.y0 = self.y0 - dy
        self.y1 = self.y1 + dy

    def process(self):
        while not self.points.empty():
            if not self.event.empty() and (self.event.top().x <= self.points.top().x):
                self.process_event() 
            else:
                self.process_point() 

        while not self.event.empty():
            self.process_event()

        self.finish_edges()

    def process_point(self):
        p = self.points.pop()
        self.arc_insert(p)

    def process_event(self):
        e = self.event.pop()

        if e.valid:
            s = Segment(e.p)
            self.output.append(s)

            a = e.a
            if a.pprev is not None:
                a.pprev.pnext = a.pnext
                a.pprev.s1 = s
            if a.pnext is not None:
                a.pnext.pprev = a.pprev
                a.pnext.s0 = s

            if a.s0 is not None: a.s0.finish(e.p)
            if a.s1 is not None: a.s1.finish(e.p)

            if a.pprev is not None: self.check_circle_event(a.pprev, e.x)
            if a.pnext is not None: self.check_circle_event(a.pnext, e.x)

    def arc_insert(self, p):
        if self.arc is None:
            self.arc = Arc(p)
        else:
            i = self.arc
            while i is not None:
                flag, z = self.intersect(p, i)
                if flag:
                    flag, zz = self.intersect(p, i.pnext)
                    if (i.pnext is not None) and (not flag):
                        i.pnext.pprev = Arc(i.p, i, i.pnext)
                        i.pnext = i.pnext.pprev
                    else:
                        i.pnext = Arc(i.p,i)
                    i.pnext.s1 = i.s1
                    i.pnext.pprev = Arc(p, i, i.pnext)
                    i.pnext = i.pnext.pprev
                    i = i.pnext 
                    seg = Segment(z)
                    self.output.append(seg)
                    i.pprev.s1 = i.s0 = seg
                    seg = Segment(z)
                    self.output.append(seg)
                    i.pnext.s0 = i.s1 = seg
                    self.check_circle_event(i, p.x)
                    self.check_circle_event(i.pprev, p.x)
                    self.check_circle_event(i.pnext, p.x)

                    return
                        
                i = i.pnext

            i = self.arc
            while i.pnext is not None:
                i = i.pnext
            i.pnext = Arc(p, i)
            
            x = self.x0
            y = (i.pnext.p.y + i.p.y) / 2.0
            start = Point(x, y)

            seg = Segment(start)
            i.s1 = i.pnext.s0 = seg
            self.output.append(seg)

    def check_circle_event(self, i, x0):
        if (i.e is not None) and (i.e.x  != self.x0):
            i.e.valid = False
        i.e = None

        if (i.pprev is None) or (i.pnext is None): return

        flag, x, o = self.circle(i.pprev.p, i.p, i.pnext.p)
        if flag and (x > self.x0):
            i.e = Event(x, o, i)
            self.event.push(i.e)

    def circle(self, a, b, c):
        if ((b.x - a.x)*(c.y - a.y) - (c.x - a.x)*(b.y - a.y)) > 0: return False, None, None

        A = b.x - a.x
        B = b.y - a.y
        C = c.x - a.x
        D = c.y - a.y
        E = A*(a.x + b.x) + B*(a.y + b.y)
        F = C*(a.x + c.x) + D*(a.y + c.y)
        G = 2*(A*(c.y - b.y) - B*(c.x - b.x))

        if (G == 0): return False, None, None

        ox = 1.0 * (D*E - B*F) / G
        oy = 1.0 * (A*F - C*E) / G

        x = ox + math.sqrt((a.x-ox)**2 + (a.y-oy)**2)
        o = Point(ox, oy)
           
        return True, x, o
        
    def intersect(self, p: Point, i: Arc):
        if (i is None): return False, None
        if (i.p.x == p.x): return False, None

        a = 0.0
        b = 0.0

        if i.pprev is not None:
            a = (self.intersection(i.pprev.p, i.p, 1.0*p.x)).y
        if i.pnext is not None:
            b = (self.intersection(i.p, i.pnext.p, 1.0*p.x)).y

        if (((i.pprev is None) or (a <= p.y)) and ((i.pnext is None) or (p.y <= b))):
            py = p.y
            px = 1.0 * ((i.p.x)**2 + (i.p.y-py)**2 - p.x**2) / (2*i.p.x - 2*p.x)
            res = Point(px, py)
            return True, res
        return False, None

    def intersection(self, p0, p1, l):
        p = p0
        if (p0.x == p1.x):
            py = (p0.y + p1.y) / 2.0
        elif (p1.x == l):
            py = p1.y
        elif (p0.x == l):
            py = p0.y
            p = p1
        else:
            z0 = 2.0 * (p0.x - l)
            z1 = 2.0 * (p1.x - l)

            a = 1.0/z0 - 1.0/z1
            b = -2.0 * (p0.y/z0 - p1.y/z1)
            c = 1.0 * (p0.y**2 + p0.x**2 - l**2) / z0 - 1.0 * (p1.y**2 + p1.x**2 - l**2) / z1

            py = 1.0 * (-b-math.sqrt(b*b - 4*a*c)) / (2*a)
            
        px = 1.0 * (p.x**2 + (p.y-py)**2 - l**2) / (2*p.x-2*l)
        res = Point(px, py)
        return res

    def finish_edges(self):
        l = self.x1 + (self.x1 - self.x0) + (self.y1 - self.y0)
        i = self.arc
        while i.pnext is not None:
            if i.s1 is not None:
                p = self.intersection(i.p, i.pnext.p, l*2.0)
                i.s1.finish(p)
            i = i.pnext

    def get_output(self):
        res = []
        correct_out = []
        for o in self.output:
            p0 = o.start
            p1 = o.end
            res.append(((p0.x, p0.y), (p1.x, p1.y)))
        for segment in res:
            if  bound(self.bound,segment) is not None:
                correct_out.append(bound(self.bound,segment))
        return correct_out
    
    def visualize(self):
        self.process()
        segments = self.get_output()
        vis = Visualizer()
        vis.add_line_segment(segments, color="purple")
        vis.add_line_segment([((0,0),(10**self.bound,0)),((10**self.bound,0),(10**self.bound,10**self.bound)),
                              ((10**self.bound,10**self.bound),(0,10**self.bound)),((0,10**self.bound),(0,0))])
        for point in self.init_points:
            vis.add_point((point.x,point.y),color=np.random.rand(3,))
        vis.show()

def bound(n: int, seg: tuple[tuple[float, float], tuple[float, float]]):
    if seg[0][0] < 0 and seg[1][0] < 0: return None
    if seg[0][0] > 10**n and seg[1][0] > 10**n: return None
    if seg[0][1] < 0 and seg[1][1] < 0: return None
    if seg[0][1] > 10**n and seg[1][1] > 10**n: return None

    intersection = find_intersection_with_vertical_line(seg,0)
    if intersection is not None:
        if seg[0][0] < 0: seg = (intersection,seg[1])
        elif seg[1][0] < 0: seg = (seg[0],intersection)
    intersection = find_intersection_with_vertical_line(seg,10**n)
    if intersection is not None:
        if seg[0][0] > 10**n: seg = (intersection,seg[1])
        elif seg[1][0] > 10**n: seg = (seg[0],intersection)
    intersection = find_intersection_with_horizontal_line(seg,0)
    if intersection is not None:
        if seg[0][1] < 0: seg = (intersection,seg[1])
        elif seg[1][1] < 0: seg = (seg[0],intersection)
    intersection = find_intersection_with_horizontal_line(seg,10**n)
    if intersection is not None:
        if seg[0][1] > 10**n: seg = (intersection,seg[1])
        elif seg[1][1] > 10**n: seg = (seg[0],intersection)
    return seg

def find_intersection_with_horizontal_line(segment, y_coordinate):
    x1, y1 = segment[0]
    x2, y2 = segment[1]

    if y1 == y2:
        return None

    if min(y1, y2) <= y_coordinate and y_coordinate <= max(y1, y2):
        slope = (x2 - x1) / (y2 - y1)
        x_intersection = x1 + slope * (y_coordinate - y1)
        
        return (x_intersection, y_coordinate)
    else:
        return None
    
def find_intersection_with_vertical_line(segment, x_coordinate):
    x1, y1 = segment[0]
    x2, y2 = segment[1]

    if x1 == x2:
        return None

    if min(x1, x2) <= x_coordinate and x_coordinate <= max(x1, x2):
        slope = (y2 - y1) / (x2 - x1)
        y_intersection = y1 + slope * (x_coordinate - x1)
        
        return (x_coordinate, y_intersection)
    else:
        return None