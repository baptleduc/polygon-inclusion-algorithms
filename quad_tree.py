from geo.polygon import Polygon
from geo.quadrant import Quadrant
from geo.segment import Segment
from geo.point import Point
from geo.tycat import tycat
from ray_casting import RayCast

class QuadTree:
    def __init__(self, polygon) -> None:
        self.polygon: Polygon= polygon
        self.bounding_quadrant: Quadrant = polygon.bounding_quadrant()
        self.center_points = self.determining_center_points(10, 10)
        self.cache = []
        self.offset_x : int
        self.offset_y : int
        

    def determining_center_points(self, nb_rows: int, nb_columns: int) -> list:
        (x_min, y_min), (x_max, y_max) = self.bounding_quadrant.get_arrays()

        # Adjusting the grid’s bounding box a little bit bigger than the polygon’s bounding box
        # to avoid the problems caused by finite arithmetic.
        x_min -= 1
        x_max += 1


        self.offset_x = (x_max - x_min) / nb_columns
        self.offset_y = (y_max - y_min) / nb_rows

        center_points: dict = {}

        for i in range(nb_rows):
            y = y_min + i * self.offset_y
            y_center_point = y + self.offset_y / 2 
            for j in range(nb_columns):
                x = x_min + j * self.offset_x
                x_center_point = x + self.offset_x / 2 
                center_point = Point((x_center_point, y_center_point))
                center_points[(x,y)] = center_point
            
        return center_points
    

    def do_intersect(self, p1, q1, p2, q2):
        o1 = self.orientation(p1, q1, p2)
        o2 = self.orientation(p1, q1, q2)
        o3 = self.orientation(p2, q2, p1)
        o4 = self.orientation(p2, q2, q1)

        if o1 != o2 and o3 != o4:
            return True

        if o1 == 0 and self.on_segment(p1, p2, q1):
            return True

        if o2 == 0 and self.on_segment(p1, q2, q1):
            return True

        if o3 == 0 and self.on_segment(p2, p1, q2):
            return True

        if o4 == 0 and self.on_segment(p2, q1, q2):
            return True

        return False

    @staticmethod
    def on_segment(point_p, point_q, point_r):
        x_p, y_p = point_p
        x_q, y_q = point_q
        x_r, y_r = point_r
        return min(x_p, x_r) <= x_q <= max(x_p, x_r) and min(y_p, y_r) <= y_q <= max(y_p, y_r)

    @staticmethod
    def orientation(point_p, point_q, point_r):
        x_p, y_p = point_p
        x_q, y_q = point_q
        x_r, y_r = point_r
        val = (y_q - y_p) * (x_r - x_q) - (x_q - x_p) * (y_r - y_q)
        if val == 0:
            return 0  # colinear
        elif val > 0:
            return 1  # clockwise
        else:
            return 2  # counter-clockwise

    def inclusion_test(self, pointA: Point, pointB: Point):
        """_summary_

        Args:
            pointA (_type_): _description_
            pointB (_type_): _description_
        Pre-condition : 
            Know pointA.is_include
        """
        sum_intersection : int = 0
        for segment in self.polygon.segments():
            p1,q1 = segment.endpoints
            if self.do_intersect(p1.coordinates, q1.coordinates, pointA.coordinates, pointB.coordinates): 
                sum_intersection += 1
        if (not pointA.is_include and sum_intersection % 2 == 1) or (pointA.is_include and sum_intersection % 2 == 0) :
            pointB.is_include = True
            return True
        pointB.is_include = False 
        return False

    def center_points_inclusion_test(self):
        list_center_points = list(self.center_points.values())
        for i in range(len(list_center_points)-1):
            self.inclusion_test(list_center_points[i], list_center_points[i+1])
    
    def is_point_include(self, point : Point):
        x, y = point.coordinates
        for key, value in self.center_points.items():
            x_case, y_case = key
            center_point = value
            if (x_case <= x  and x <= x_case + self.offset_x) and (y_case <= y and y <= y_case + self.offset_y):
                break
        return self.inclusion_test(center_point, point)
    
    

            


    


            




                






    
        