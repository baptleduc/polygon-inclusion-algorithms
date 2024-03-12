
from geo.polygon import Polygon
from geo.point import Point
from geo.segment import Segment
from ray_casting import RayCast

class Find:

    @staticmethod
    def naif(polygones):
        inclusions : list = [-1 for _ in range(len(polygones))]
        for i, polygon1 in enumerate(polygones):
            for j, polygon2 in enumerate(polygones):
                if i != j and RayCast.is_include(polygon1, polygon2):        
                    inclusions[i] = j
                    break
        return inclusions
