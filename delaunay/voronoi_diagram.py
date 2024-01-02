from typing import List, Optional
from .point import Point
from .neighbours import Neighbours
from .triangle import Triangle
from visualizer.figures.polygon import Polygon
from collections import defaultdict

class VoronoiDiagram:
    def __init__(self, points : List[Point], neighbours : Neighbours, triangulation : List[Triangle]) -> None:
        self.points = points
        self.neighbours = neighbours
        self.triangles = triangulation

    def create_point_to_edges_mapping(self):
        point_to_edges = defaultdict(set)
        for e in self.neighbours.edges.keys():
            point_to_edges[e.p1].add(e)
            point_to_edges[e.p2].add(e)
        
        return point_to_edges
    

    def create_boundary_for_points(self) -> tuple[int, int, int, int]:
        x_coords = [point.get()[0] for point in self.points]
        y_coords = [point.get()[1] for point in self.points]

        min_x = min(x_coords)
        max_x = max(x_coords)
        min_y = min(y_coords)
        max_y = max(y_coords)

        frame = 10


        return min_x, max_x, min_y, max_y
    
    def create_polygon_for_vertex(self, vertex: Point, point_to_edges: dict) -> Optional[list[Point]]:
        polygon = []
        edges = list(point_to_edges[vertex])
        first_edge = edges[0]
        edge = first_edge
        triangle = self.neighbours.edges[edge][0]
        circumcenter = triangle.find_circumcenter()
        polygon.append(circumcenter)
        
        while True:
            next_triangle = self.neighbours.find_neighbour(edge, triangle)
            if next_triangle is None:
                # edge is on outer border of triangulation
                # this vertex has an infinite polygon
                # TODO: handle this case
                return None
            circumcenter = next_triangle.find_circumcenter()
            polygon.append(circumcenter)
            
            # find next edge
            for temp_edge in next_triangle.edges:
                if (vertex == temp_edge.p1 or vertex == temp_edge.p2) and temp_edge != edge:
                    next_edge = temp_edge

            if next_edge == first_edge:
                break
            
            edge = next_edge
            triangle = next_triangle
        
        return polygon
    
    def create_diagram(self) -> list[Polygon]:
        point_to_edges = self.create_point_to_edges_mapping()
        diagram = []
        for vertex in self.points:
            polygon = self.create_polygon_for_vertex(vertex, point_to_edges)
            if polygon is not None:
                diagram.append(Polygon(
                    data=[(p.x, p.y) for p in polygon],
                    options={}
                ))
        
        return diagram

