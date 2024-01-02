from fortuneJas import *
from random import uniform
from visualizer.main import Visualizer

def gen_points(n):
    list = []
    for _ in range(n):
        list.append(Point(uniform(0,100),uniform(0,100)))
    return list

def length(edge):
    return (edge[1][0] - edge[0][0])**2 + (edge[1][1] - edge[0][1])**2

fortune = Voronoi(gen_points(10))
fortune.process()
segments = fortune.get_output()
corr_out = []
for segment in segments:
    if length(segment) < 1000:
        corr_out.append(segment)
vis = Visualizer()
vis.add_line(corr_out)
vis.show()