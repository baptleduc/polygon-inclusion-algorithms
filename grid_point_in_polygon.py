from geo.polygon import Polygon
from geo.quadrant import Quadrant
from geo.point import Point


class GridPointInPolygon:
    """
    Point-in-Polygon tests by determining grid center
    points in advance.
    """
    def __init__(self, polygon, nb_rows, nb_columns) -> None:
        """
        Initialize the GridPointInPolygon object with the given polygon.

        Args:
            polygon (Polygon): The polygon to be used for initializing the GridPointInPolygon.

        Returns:
            None
        """

        self.polygon: Polygon = polygon

        # Smallest enclosing quadrant for the polygon
        self.bounding_quadrant: Quadrant = polygon.bounding_quadrant() 
        
        self.center_points : dict
        self.offset_x : int
        self.offset_y : int

        self.__determining_center_points(nb_rows, nb_columns)
        self.__center_points_inclusion_test()


    def __determining_center_points(self, nb_rows: int, nb_columns: int) -> None:
        """
        Determine the center points of a grid within the bounding quadrant.

        Args:
            nb_rows (int): The number of rows in the grid.
            nb_columns (int): The number of columns in the grid.

        Returns:
            None

        Raises:
            ValueError: If nb_rows or nb_columns is less than or equal to zero.
        """

        if nb_rows <= 0 or nb_columns <= 0:
            raise ValueError("The number of rows and columns must be greater than zero.")

        (x_min, y_min), (x_max, y_max) = self.bounding_quadrant.get_arrays()

        # Adjust the grid’s bounding box slightly larger than the polygon’s bounding box
        # to avoid problems caused by finite arithmetic.

        x_min -= 0.2
        x_max += 0.2


        # Calculate the offsets in x and y
        self.offset_x = (x_max - x_min) / nb_columns
        self.offset_y = (y_max - y_min) / nb_rows
        
        x_start = x_min - self.offset_x
        self.center_points = {}

        # Iterate over each row
        for i in range(nb_rows):
            y = y_min + i * self.offset_y
            y_center_point = y + self.offset_y / 2 
            
            # Iterate over each column
            for j in range(nb_columns + 2):
                x = x_start + j * self.offset_x
                x_center_point = x + self.offset_x / 2 
                
                # Create a central Point and 
                center_point = Point((x_center_point, y_center_point))
                

                if x_center_point <= x_min or x_center_point >= x_max:
                    center_point.is_include = "OUT"
                    center_point.is_singular = False

                self.center_points[(x, y)] = center_point
            

    def __do_intersect(self, p1, q1, p2, q2):
        """
        Check if line segments p1q1 and p2q2 intersect.

        Args:
            p1 (Tuple[int, int]): Coordinates of the first endpoint of segment 1.
            q1 (Tuple[int, int]): Coordinates of the second endpoint of segment 1.
            p2 (Tuple[int, int]): Coordinates of the first endpoint of segment 2.
            q2 (Tuple[int, int]): Coordinates of the second endpoint of segment 2.

        Returns:
            bool: True if the line segments intersect, False otherwise.
        """
        o1 = self.__orientation(p1, q1, p2)
        o2 = self.__orientation(p1, q1, q2)
        o3 = self.__orientation(p2, q2, p1)
        o4 = self.__orientation(p2, q2, q1)

        if o1 != o2 and o3 != o4:
            return True
        return False

    @staticmethod
    def __on_segment(point_p, point_q, point_r):
        """
        Check if point_r lies on segment pq.

        Args:
            point_p (Tuple[int, int]): Coordinates of the first endpoint of the segment.
            point_q (Tuple[int, int]): Coordinates of the second endpoint of the segment.
            point_r (Tuple[int, int]): Coordinates of the point to be checked.

        Returns:
            bool: True if point_r lies on segment pq, False otherwise.
        """
        x_p, y_p = point_p
        x_q, y_q = point_q
        x_r, y_r = point_r
        return min(x_p, x_q) <= x_r <= max(x_p, x_q) and min(y_p, y_q) <= y_r <= max(y_p, y_q)

    @staticmethod
    def __orientation(point_p, point_q, point_r):
        """
        Determine the orientation of three points.

        Args:
            point_p (Tuple[int, int]): First point.
            point_q (Tuple[int, int]): Second point.
            point_r (Tuple[int, int]): Third point.

        Returns:
            int: 0 if points are collinear, 1 if clockwise, 2 if counter-clockwise.
        """
        x_p, y_p = point_p
        x_q, y_q = point_q
        x_r, y_r = point_r
        val = (y_q - y_p) * (x_r - x_q) - (x_q - x_p) * (y_r - y_q)
        if val == 0:
            return 0  # Collinear
        elif val > 0:
            return 1  # Clockwise
        else:
            return 2  # Counter-clockwise

    def __inclusion_test(self, pointA: Point, pointB: Point) -> None:
        """
        Test if pointB is included within the polygon by counting the number of intersections 
        between the line segment formed by pointA and pointB and all segments of the polygon.

        Updates the 'is_include' attribute of pointB based on these tests.

        Args:
            pointA (Point): The first endpoint of the line segment.
            pointB (Point): The second endpoint of the line segment.

        Returns:
            bool: True if pointB is inside the polygon, False otherwise.

        Preconditions:
            pointA.is_include must be known.
        """
        # Initialize the intersection count
        sum_intersection = 0
        
        # Iterate through each segment of the polygon
        for segment in self.polygon.segments():
            p1, q1 = segment.endpoints
            #Determine if pointB lies on segment
            if segment.contains(pointB):
                pointB.is_singular = True
                pointB.is_include = "MAYBE"
                return

            if self.__do_intersect(p1.coordinates, q1.coordinates, pointA.coordinates, pointB.coordinates):
                sum_intersection += 1
        
        # Determine if pointB is included based on the number of intersections
        if (pointA.is_include == "OUT" and sum_intersection % 2 == 1) or (pointA.is_include=="IN" and sum_intersection % 2 == 0):
            pointB.is_include = "IN"
        else:
            pointB.is_include = "OUT"

        pointB.is_singular = False
        return 
    
    def __center_points_inclusion_test(self) -> None:
        """
        Test inclusion between consecutive center points.

        This method tests the inclusion between each consecutive pair of center points
        in the grid.
        """
        list_center_points = list(self.center_points.values())
        for i in range(len(list_center_points)):
            pointA = list_center_points[i]
            for j in range(i+1, len(list_center_points)):
                pointB = list_center_points[j]
                self.__inclusion_test(pointA, pointB)
                if not pointB.is_singular:
                    break
                    

            
    def is_point_include(self, point: Point) -> None:
        """
        Check if a point is inside the polygon.

        This method determines the grid cell containing the given point and tests
        its inclusion by using the center-point of that grid cell. It modifies the 
        'is_include' attribute of the given point to indicate whether it is inside 
        (is_include = 'IN'), outside (is_include = 'OUT'), or lies on a segment 
        (is_include = 'MAYBE') of the polygon.

        Args:
            point (Point): The point to be checked.

        Returns:
            None
        """

        x, y = point.coordinates

        # Iterate through each grid cell
        for key, value in self.center_points.items():
            x_case, y_case = key
            center_point = value
            
            # Check if the point lies within the current grid cell
            if (x_case <= x <= x_case + self.offset_x) and (y_case <= y <= y_case + self.offset_y):
                # Test inclusion between the center point of the grid cell and the given point
                self.__inclusion_test(center_point, point)
                return
        point.is_include = "OUT"
    

    def is_polygon_include(self, test_polygon: Polygon) -> bool:
        """
        Check if test_polygon is included in self.polygon

        Args:
            test_polygon (Polygon): The polygon to be checked.

        Returns:
            bool: True if the entire test_polygon is included in self.polygon, False otherwise.
        """
        for point in test_polygon.points:
            self.is_point_include(point)
            if point.is_include == "IN":
                return True
            elif point.is_include == "OUT":
                return False
        return True


if __name__ == '__main__':
    p1 = (0,2)
    p2 = (0,4)
    r = (0.1,3)
    print(GridPointInPolygon.__on_segment(p1,p2, r))

                






    
        