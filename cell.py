#!/usr/bin/env python3

from geo.point import Point
from geo.polygon import Polygon
class Cell:
    """
    Represents a cell in the Grid.
    """
    def __init__(self, x_min, x_max, y_min, y_max):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.edges = set()  # Set to store edges crossing the cell
        center_point_x, center_point_y = x_min + (x_max - x_min)/2 , y_min +(y_max - y_min)/2
        self.center_point: Point = Point((center_point_x, center_point_y))

        self.cell_point = [Point((x_min,y_min)), Point((x_max, y_max)) , Point((x_min, y_max)), Point((x_max, y_min ))]
        self.cell_polygon = Polygon([Point((x_min,y_min)) , Point((x_max, y_min )), Point((x_max, y_max)), Point((x_min, y_max))  ])