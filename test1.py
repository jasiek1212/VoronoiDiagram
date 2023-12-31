from random import uniform
import matplotlib.pyplot as plt
import numpy as np

from delaunay import *
from test_vis import my_vis



def gen_random_test_case(n: int) -> list[Point]:
    return [
        Point(uniform(0, 100), uniform(0, 100))
        for _ in range(n)
    ]

def test_case_1() -> list[Point]:
    raw = [
        (2.2524623530691845, 68.8213389679894),
        (10.856841406710927, 13.27883179718109),
        (83.95981130461654, 9.98735185702273),
        (24.211261716189338, 33.702247503084834),
        (10.091229932290503, 56.747396380047235),
        (64.14884770958908, 43.556686927138735),
        (22.176838566423783, 17.773165538986426),
        (82.88614980391803, 73.40387431731749),
    ]
    return [Point(r[0], r[1]) for r in raw]


if __name__ == "__main__":
    vis = my_vis

    random_points = gen_random_test_case(10)
    vis.add_point([p.get() for p in random_points])

    delaunay = DelaunayTriangulation(random_points)
    triangles = delaunay.run()
    vis.add_line_segment(delaunay.get_all_edges_for_vis())

    triangle_centers = [t.find_circumcenter() for t in triangles]
    vis.add_point([p.get() for p in triangle_centers], color="red")

    # VORONOI
    voronoi = VoronoiDiagram(
        points=random_points,
        neighbours=delaunay.neighbours,
        triangulation=list(triangles),
    )
    diagram = voronoi.create_diagram()

    vis.add_point([p.get() for p in random_points])
    vis.add_line_segment(delaunay.get_all_edges_for_vis())

    cmap = plt.cm.get_cmap("hsv", len(diagram))
    for i, polygon in enumerate(diagram):
        vis.add_polygon(polygon.data, alpha=0.3, color=np.random.rand(3,))
    vis.show()
    plt.show()