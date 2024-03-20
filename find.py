
from geo.polygon import Polygon
from geo.point import Point
from geo.segment import Segment
from ray_casting import RayCast
from tree import Tree
from grid_point_in_polygon import GridPointInPolygon

#variables gloables
IN = True
OUT = False

class Find:

    @staticmethod
    def __poly_abs_extremis(polygones):
        liste = []
        for polygone in enumerate(polygones):
            point_min,point_max = polygone[1].bounding_quadrant().limits(0)
            liste.append((point_min,IN,polygone[0]))
            liste.append((point_max,OUT,polygone[0]))
        return sorted(liste)

    @staticmethod
    def __get_potential_tree(liste_point):
        current = Tree()
        forest = []
        for (_, IN, id) in liste_point:
            #print(IN,id)
            new_branch = Tree()
            if current.parent :
                if IN:
                    current.set_value(id)
                    current.add_childs(new_branch)
                else:
                    while current.value != id:
                        if current.parent == None:
                            break
                        current = current.parent
                    if current.parent is not None:
                        current.parent.add_childs(new_branch)
            else:
                current.set_value(id)
                current.add_childs(new_branch)
                forest.append(current)
            current = new_branch
        return forest
    
    @staticmethod
    def __list_with_area(polygones):
        tab = []
        for (i,polygone) in enumerate(polygones):
            tab.append((abs(polygone.area()),i))
        return(tab)

    # def naif(polygones):
    #     inclusions : list = [-1 for _ in range(len(polygones))]
    #     for i, polygon1 in enumerate(polygones):
    #         for j, polygon2 in enumerate(polygones):
    #             if i != j :
    #                 grid = GridPointInPolygon(polygon1)
    #                 grid.determining_center_points(10,10)
    #                 grid.center_points_inclusion_test()
    #                 if grid.is_polygon_include(polygon2):        
    #                     inclusions[i] = j
    #                     break
    #     return inclusions

    def area_check(polygones):
        inclusions : list = [-1 for _ in range(len(polygones))]
        polygones_sorted = sorted(Find.__list_with_area(polygones))
        count = 0
        #print(polygones_sorted)
        for i in range(len(polygones_sorted)):
            for j in range(i+1,len(polygones_sorted)):
                _,polygone1 = polygones_sorted[i]
                _,polygone2 = polygones_sorted[j]
                #print("test ", polygone1, " dans ",polygone2)
                grid = GridPointInPolygon(polygones[polygone2])
                grid.determining_center_points(10,10)
                grid.center_points_inclusion_test()
                if grid.is_polygon_include(polygones[polygone1]):
                    #print("pass")
                    inclusions[polygone1] = polygone2
                    break
        return inclusions

    def area_local_vision(polygones):
        liste = Find.__poly_abs_extremis(polygones)
        forest_inclusion = Find.__get_potential_tree(liste)
        #for tree in forest_inclusion:
            #print(forest_inclusion[0])
            #print("arbre suivant")
        inclusions : list = [-1 for _ in range(len(polygones))]
        for tree in forest_inclusion:
            tree.test_inclusion_with_childs(inclusions,polygones)
        return inclusions

