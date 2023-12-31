from random import uniform
import matplotlib.pyplot as plt

from delaunay import *
from test_vis import my_vis

def test_case_1() -> list[Point]:
    raw = [
        (2, 4),
        (-1, -1),
        (7, -1)
        # (4, 2),
        # (10, -4)
    ]
    return [Point(r[0], r[1]) for r in raw]

if __name__ == "__main__":
    vis = my_vis

    random_points = test_case_1()
    vis.add_point([p.get() for p in random_points])

    delaunay = DelaunayTriangulation(random_points)
    triangles = delaunay.run()
    vis.add_line_segment(delaunay.get_all_edges_for_vis())

    triangle_centers = [t.find_circumcenter() for t in triangles]
    vis.add_point([p.get() for p in triangle_centers], color="red")
    for point in triangle_centers: 
        print(point)

    vis.show()
    plt.show()