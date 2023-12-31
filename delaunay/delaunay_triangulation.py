from matplotlib import pyplot as plt
import numpy as np
from .point import Point, orientation
from .triangle import Triangle
from .neighbours import Neighbours
from .edge import Edge
from typing import List, Tuple
from math import log10, inf
from test_vis import my_vis

class DelaunayTriangulation:
    # class responsible for algorithm

    def __init__(self, points) -> None:
        # list of Triangles
        self.points = points
        self.super_triangle = gen_init_triangle(points)

        self.triangulation = {self.super_triangle}
        self.neighbours = Neighbours()
        self.neighbours.put(self.super_triangle)
        self.inittriangle = self.super_triangle
    
    def run(self) -> list[Triangle]:
        for i, point in enumerate(self.points):
            print("Adding point: ", i)
            triangle = self.find_triangle(point)
            neighbourhood, hull = self.find_neighbourhood(point, triangle)
            self.delete_neighbourhood(neighbourhood)
            self.rebuild_neighbourhood(point, hull)
        # self.clean_up()
        return self.triangulation

    def find_triangle(self, p: Point) -> Triangle:
        # returns triangle which contains p after adding p to triangulation
        # my_vis.clear()

        curr_triangle = self.inittriangle
        visited = {curr_triangle}
        # my_vis.add_line_segment(self.get_all_edges_for_vis())
        # my_vis.add_point([p.get() for p in self.points], color="grey")
        # my_vis.add_point(p.get(), color="green")
        # my_vis.add_polygon(curr_triangle.to_polygon().data, color=np.random.rand(3,), label="INIT")

        def _next_triangle(t, p):
            ns = []
            for edge in t.edges:
                neighbour = self.neighbours.find_neighbour(edge, t)
                if neighbour is not None and neighbour not in visited:
                    ns.append(neighbour)
                    if orientation(edge.p1, edge.p2, p) == 1:
                        return neighbour
            
            raise Exception("Here we go again")
            print([str(t) for t in ns])
            my_vis.show()
            plt.legend()
            plt.show()

        i = 0
        while not curr_triangle.point_in_triangle(p):
            print("Next triangle search, step: ", i)
            curr_triangle = _next_triangle(curr_triangle, p)
            # my_vis.add_polygon(curr_triangle.to_polygon().data, color=np.random.rand(3,), label=f"Step: {i}")
            visited.add(curr_triangle)
            i += 1
        
        return curr_triangle

    def find_neighbourhood(
        self,
        p: Point,
        curr: Triangle,
    ) -> tuple[list[Triangle], list[Edge]]:
        neighbourhood: set[Triangle] = set()
        hull: list[Edge] = []

        def _rec(t: Triangle):
            neighbourhood.add(t)
            for edge in t.edges:
                next_t = self.neighbours.find_neighbour(edge, t)
                if next_t is None:
                    hull.append(edge)
                    continue
                
                if next_t not in neighbourhood:
                    if next_t is not None and next_t.circumcircle_contains(p):
                        _rec(next_t)
                    else:
                        hull.append(edge)

        _rec(curr)

        return neighbourhood, hull

    def delete_neighbourhood(self, neighbourhood) -> None:
        for triangle in neighbourhood:
            for i in range(3):
                self.neighbours.remove_neighbour(triangle.edges[i], triangle)
            self.triangulation.remove(triangle)
 
    def rebuild_neighbourhood(self, p : Point, hull):
        # my_vis.clear()
        # my_vis.add_line_segment(self.get_all_edges_for_vis())
        # my_vis.add_point([p.get() for p in self.points], color="grey")
        # my_vis.add_point(p.get(), color="green")
        # my_vis.add_line_segment([
        #     (edge.p1.get(), edge.p2.get())
        #     for edge in hull
        # ], color="red")
        # my_vis.show()
        # plt.show()

        for edge in hull:
            t = Triangle(p, edge.p1, edge.p2)
            self.triangulation.add(t)
            self.neighbours.put(t)
        self.inittriangle = t

   
    def get_all_edges_for_vis(self) -> list[Edge]:
        return [
            (edge.p1.get(), edge.p2.get())
            for edge in self.neighbours.edges.keys()
        ]

    def print_tri(self):
        return ', '.join(f"{triangle}" for triangle in list(self.triangulation))

    def clean_up(self):
        triangles = list(self.triangulation)
        for triangle in triangles:
            if triangle.contains(self.super_triangle.to_point_list()):
                for edge in triangle.edges:
                    self.neighbours.remove_neighbour(edge,triangle)
                self.triangulation.remove(triangle)


def gen_init_triangle(points: List[Point]) -> Triangle:
    min_x,min_y = inf,inf
    max_x, max_y = -inf,-inf 
    for i in range(len(points)):
        curr = points[i]
        max_x = max(curr.x,max_x)
        min_x = min(curr.x,min_x)
        max_y = max(curr.y,max_y)
        min_y = min(curr.y,min_y)
    
    height = max_y - min_y
    width = max_x - min_x
    
    left_down = Point(
        x= min_x - 3 * width,
        y= min_y - height,
    )
    right_down = Point(
        x= max_x + 3 * width,
        y= min_y - height,
    )
    middle_up = Point(
        x= min_x + 0.5 * width,
        y= max_y + 1.5 * width,
    )
    return Triangle(left_down, middle_up, right_down)
