
from geo.polygon import Polygon
from geo.point import Point
from geo.segment import Segment
from ray_casting import RayCast

class Find:

    def __list_with_area(polygones):
        tab = []
        for (i,polygone) in enumerate(polygones):
            tab.append((abs(polygone.area()),i))
        return(tab)

    @staticmethod
    def naif(polygones):
        inclusions : list = [-1 for _ in range(len(polygones))]
        for i, polygon1 in enumerate(polygones):
            for j, polygon2 in enumerate(polygones):
                if i != j and RayCast.is_include(polygon1, polygon2):        
                    inclusions[i] = j
                    break
        return inclusions

    def area_check(polygones):
        inclusions : list = [-1 for _ in range(len(polygones))]
        polygones_sorted = sorted(Find.__list_with_area(polygones))
        count = 0
        for i in range(len(polygones_sorted)):
            for j in range(i+1,len(polygones_sorted)):
                _,polygone1 = polygones_sorted[i]
                _,polygone2 = polygones_sorted[j]
                if RayCast.is_include(polygones[polygone1],polygones[polygone2]):
                    inclusions[polygone1] = polygone2
                    break
        return inclusions
