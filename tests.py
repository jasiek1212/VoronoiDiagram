from delaunay import *
from random import uniform
from typing import List
from timeit import default_timer as timer

def gen_points(n : int) -> List[Point]:
    list = []
    for i in range(n):
        list.append(Point(uniform(0,100),uniform(0,100)))
    return list

def main_test(points):
    tri = DelaunayTriangulation(points)
    for i in range(len(points)):
        curr = tri.find_triangle(points[i])
        neighbourhood, hull, _ = tri.find_neighbourhood(points[i],curr,set(),neighbourhood=[], hull=[])
        tri.delete_neighbourhood(neighbourhood)
        tri.rebuild_neighbourhood(points[i], hull)
    tri.clean_up()  
    return tri, points

def tests(num_of_points, iterations_num):
    failed = 0
    start = timer()
    for i in range(iterations_num):
        points = gen_points(num_of_points)
        try:
            a, b = main_test(points)
        except: 
            failed += 1
    end = timer()
    print("Passed: ", iterations_num-failed, " out of ", iterations_num, " with time ", end-start, "s.")
    return failed

tests(num_of_points=7,iterations_num=1000) #wybierz liczbę punktów oraz ilość testów