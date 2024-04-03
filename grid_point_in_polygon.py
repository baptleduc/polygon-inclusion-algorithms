from geo.polygon import Polygon
from geo.quadrant import Quadrant
from geo.segment import Segment
from geo.point import Point
import math
from cell import Cell

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

        self.offset_x: int
        self.offset_y: int
        self.x_min: int
        self.y_min: int
        self.cells: list

        #To display
        self.sure_in = []
        self.sure_out = []
        self.sure_maybe = []


        self.__determining_center_points(nb_rows, nb_columns)
        self.__marked_transversed_cells()
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
            raise ValueError(
                "The number of rows and columns must be greater than zero."
            )

        (x_min, y_min), (x_max, y_max) = self.bounding_quadrant.get_arrays()

        # Adjust the grid’s bounding box slightly larger than the polygon’s bounding box
        # to avoid problems caused by finite arithmetic.
        x_min -= (x_max-x_min)   /1000
        x_max += (x_max-x_min)   / 1000
        y_min -= (y_max-y_min)   / 1000
        y_max += (y_max-y_min)   / 1000

        # Calculate the offsets in x and y
        self.offset_x = (x_max - x_min) / nb_columns
        self.offset_y = (y_max - y_min) / nb_rows

        x_start = x_min - self.offset_x
        self.y_min = y_min
        self.x_min = x_start

        self.cells = []

        for i in range(nb_rows):
            y = y_min + i * self.offset_y
            cells_row = []

            for j in range(nb_columns + 1):
                x = x_start + j * self.offset_x

                cell = Cell(x, x + self.offset_x, y, y + self.offset_y)
                cells_row.append(cell)

                # Create a central Point and
                center_point = cell.center_point
                center_point_x, center_point_y = center_point.coordinates

                if center_point_x <= x_min or center_point_x >= x_max:
                    self.sure_out.append(center_point)
                    center_point.is_include = "OUT"
                    center_point.is_singular = False
            self.cells.append(cells_row)
            

    def dda_to_cells(self, segment: Segment) -> None:
        """
        [UNUSED]

        Traverse the grid along a segment, adding the segment to every cell it intersects by using
        Digital Differential Analyzer (DDA) algorithm.

        Args:
            segment (Segment): The segment to traverse
        """
        (x1, y1), (x2, y2) = (
            segment.endpoints[0].coordinates,
            segment.endpoints[1].coordinates,
        )
        dx, dy = (x2 - x1), (y2 - y1)
        steps = max(abs(dx), abs(dy))

        dx, dy = dx / steps, dy / steps
        x, y = x1, y1
        i = 0
        while i <= steps:

            idx_cell_crossed_x, idx_cell_crossed_y = (
                self.__get_idx_cell_containing_point(x, y)
            )

            if (
                0 <= idx_cell_crossed_x <= len(self.cells[0]) - 1
                and 0 <= idx_cell_crossed_y <= len(self.cells) - 1
            ):
                self.cells[idx_cell_crossed_y][idx_cell_crossed_x].edges.add(segment)

            x += dx
            y += dy
            i += 1

    def __marked_transversed_cells(self) -> None:
        """
        Perfom the segment_grid_traversal for each segment of the polygon.
        """
        for segment in self.polygon.segments():
            self.segment_grid_traversal(segment)

    def __get_idx_cell_containing_point(self, x: int, y: int) -> tuple:
        """
        Get the index of the cell in self.cells containing the point (x, y).

        Args:
            x (int): The x-coordinate of the point.
            y (int): The y-coordinate of the point.

        Returns:
            tuple: A tuple (idx_x, idx_y) representing the indices of the cell containing the point.
        """

        idx_cell_crossed_x = math.floor((x - self.x_min) / self.offset_x)
        idx_cell_crossed_y = math.floor((y - self.y_min) / self.offset_y)
        return idx_cell_crossed_x, idx_cell_crossed_y

    def segment_grid_traversal(self, segment) -> None:
        """
        Traverse the grid along a segment, adding the segment to every cell it intersects by
        using Fast Voxel Traversal Algorithm.

        Args:
            segment (Segment) : The segment to traverse
        """

        def SIGN(x):
            return 1 if x > 0 else -1 if x < 0 else 0

        def FRAC1(x):
            return 1.0 - (x - math.floor(x))

        def FRAC0(x):
            return x - math.floor(x)

        (x1, y1), (x2, y2) = (
            segment.endpoints[0].coordinates,
            segment.endpoints[1].coordinates,
        )
        segment_dx, segment_dy = (x2 - x1), (y2 - y1)
        segment_direction_x, segment_direction_y = SIGN(segment_dx), SIGN(segment_dy)

        # Add the segment to the cell initially containing the point (x1, y1).
        current_X_index, current_Y_index = self.__get_idx_cell_containing_point(x1, y1)
        current_cell: Cell = self.cells[current_Y_index][current_X_index]
        current_cell.edges.add(segment)

        if segment_direction_x != 0:
            t_delta_x = min(
                segment_direction_x * self.offset_x / segment_dx, 10000000.0
            )
        else:
            t_delta_x = 10000000.0

        if segment_direction_x > 0:
            t_max_x = t_delta_x * FRAC1(x1)
        else:
            t_max_x = t_delta_x * FRAC0(x1)

        if segment_direction_y != 0:
            t_delta_y = min(
                segment_direction_y * self.offset_y / segment_dy, 10000000.0
            )
        else:
            t_delta_y = 10000000.0

        if segment_direction_y > 0:
            t_max_y = t_delta_y * FRAC1(y1)
        else:
            t_max_y = t_delta_y * FRAC0(y1)

        step_x, step_y = (
            segment_direction_x  ,
            segment_direction_y  ,
        )
        x, y = x1, y1
        while 1:
            
            if (
                current_cell.x_min <= x2 <= current_cell.x_max
                and current_cell.y_min <= y2 <= current_cell.y_max
            ):
                break
            if t_max_x < t_max_y:
                t_max_x += t_delta_x
                current_X_index += step_x
                if not (0 <= current_X_index < len(self.cells[0])):
                    break
                current_cell = self.cells[current_Y_index][current_X_index ]
                current_cell.edges.add(segment)

            else:
                t_max_y += t_delta_y
                current_Y_index += step_y
                if not (0 <= current_Y_index < len(self.cells)):
                    break    
                current_cell = self.cells[current_Y_index ][current_X_index  ]
                current_cell.edges.add(segment)

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
        [UNUSED]

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
        return min(x_p, x_q) <= x_r <= max(x_p, x_q) and min(y_p, y_q) <= y_r <= max(
            y_p, y_q
        )

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

    def __inclusion_test(self, cellA: Cell, cellB: Cell, pointA: Point, pointB: Point) -> None:
        """
        Test if 'pointB' is included within the polygon by counting the number of intersections
        between the line segment formed by pointA and pointB and all segments of cellA.edges U cellB.edges.

        Updates the 'is_include' attribute of pointB based on these tests.

        Args:
            pointA (Point): The first endpoint of the line segment.
            pointB (Point): The second endpoint of the line segment.

        Returns:
            bool: True if pointB is inside the polygon, False otherwise.

        Preconditions:
            pointA.is_include must be known.
        """

        sum_intersection = 0

        all_edges = cellA.edges | cellB.edges
        # Iterate through each segments of cellA and cellB
        for segment in all_edges:
            p1, q1 = segment.endpoints

            if segment.contains(pointB):
                pointB.is_singular = True
                pointB.is_include = "MAYBE"
                self.sure_maybe.append(pointB)
                return

            if self.__do_intersect(
                p1.coordinates, q1.coordinates, pointA.coordinates, pointB.coordinates
            ):
                sum_intersection += 1

        if (pointA.is_include == "OUT" and sum_intersection % 2 == 1) or (
            pointA.is_include == "IN" and sum_intersection % 2 == 0
        ):
            self.sure_in.append(pointB)
            pointB.is_include = "IN"
        else:
            self.sure_out.append(pointB)
            pointB.is_include = "OUT"
        pointB.is_singular = False
        return

    def __center_points_inclusion_test(self) -> None:
        """
        Test inclusion between consecutive center points.

        This method tests the inclusion between each consecutive pair of center points
        in the grid.
        """
        num_columns = len(self.cells[0])

        for row_idx, row in enumerate(self.cells):

            for col_idx, cellA in enumerate(row):
                if cellA.center_point.is_singular:
                    continue

                for next_col_idx in range(col_idx + 1, num_columns):
                    cellB = self.cells[row_idx][next_col_idx]
                    self.__inclusion_test(
                        cellA, cellB, cellA.center_point, cellB.center_point
                    )

                    # If cellB is singular, update cellA's edges.
                    # This is needed to count the intersections of the segment from pointA to next point pointB' passing through singular pointB.
                    if cellB.center_point.is_singular:
                        cellA.edges.update(cellB.edges)
                    else:
                        # If  not cellB.center_point.is_singular, move on to the next pair
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
        idx_cell_x, idx_cell_y = self.__get_idx_cell_containing_point(x, y)
        if (
            0 <= idx_cell_x <= len(self.cells[0]) - 1
            and 0 <= idx_cell_y <= len(self.cells) - 1
        ):
            cell_with_point: Cell = self.cells[idx_cell_y][idx_cell_x]
            self.__inclusion_test(
                cell_with_point, cell_with_point, cell_with_point.center_point, point
            )
            return
        self.sure_out(point)
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
