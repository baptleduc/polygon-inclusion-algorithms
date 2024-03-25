
from geo.polygon import Polygon
from geo.point import Point
from geo.segment import Segment

class RayCast:

    @staticmethod
    def __is_intersection(point: Point, segment: Segment) -> bool:
        x, y = point.coordinates
        point1, point2 = segment.endpoints
        (x1, y1), (x2, y2) = point1.coordinates, point2.coordinates

        if (y < y1) != (y < y2) and x < (x2-x1)*(y-y1)/(y2-y1)+x1:
            return True
        return False




    @staticmethod
    def is_point_inside_polygon(point: Point, polygon) -> bool:
        sum_intersections: int = 0
        for segment in polygon.segments():
            sum_intersections += 1 if RayCast.__is_intersection(point, segment) else 0
        
        return False if sum_intersections % 2 == 0 else True
    
    @staticmethod
    def is_include(polygon1: Polygon, polygon2: Polygon) -> bool:
        """

        Args:
            polygon1 (Polygon): _description_
            polygon2 (Polygon): _description_

        Returns:
            bool: True if polygon1 is include in polygon2 else False
        """

        for point in polygon1.points:
            if RayCast.is_point_inside_polygon(point, polygon2): 
                return True
        
        return False






    
        