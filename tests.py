from classes.classes import *
from visualizer.main import Visualizer
from random import uniform

points = [Point(2,5),Point(7,2),Point(4,6)]
t = Triangle(points[0],points[1],points[2])
vis = Visualizer()
vis.add_polygon(points)
vis.add_point((t.find_incenter))