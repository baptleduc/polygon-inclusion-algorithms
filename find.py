
from geo.polygon import Polygon
from geo.point import Point
from geo.segment import Segment
from ray_casting import RayCast
from tree import Tree
from liste_doublement_chainee import ListeChainee
from grid_point_in_polygon import GridPointInPolygon

#variables gloables
IN = True
OUT = False

class Find:

    @staticmethod
    def __poly_abs_extremis(polygones,coord):
        liste = []
        for polygone in enumerate(polygones):
            point_min,point_max = polygone[1].bounding_quadrant().limits(coord)
            liste.append((point_min,IN,polygone[0]))
            liste.append((point_max,OUT,polygone[0]))
        return sorted(liste)

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

    
    @staticmethod
    def __potential_inclusions(liste_point):
        currentlist = ListeChainee()
        inclusion_possible = [[] for _ in range(len(liste_point)//2)]
        for (_, IN, id) in liste_point:
            if IN:
                currentlist = currentlist.insert(id)
                #currentlist.affiche()
            else:
                #print("delete ",id)
                currentlist = currentlist.delete(id)
                #currentlist.affiche()
                while currentlist.prec:
                    inclusion_possible[id].append(currentlist.value)
                    currentlist = currentlist.prec
                if currentlist.value is not None:
                    inclusion_possible[id].append(currentlist.value)
                currentlist = currentlist.go_end()
        return inclusion_possible           

    @staticmethod
    def __intersection(tab1,tab2):
        assert(len(tab1) == len(tab2))
        tab = [[] for _ in range(len(tab1))]
        for i in range(len(tab1)):
            tab[i] = [id for id in tab1[i] if id in tab2[i]]
        return tab
    
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
        x = 0
        y = 1
        liste_abscisse = Find.__poly_abs_extremis(polygones,x)
        liste_ordonne = Find.__poly_abs_extremis(polygones,y)      

        inclusions : list = [-1 for _ in range(len(polygones))]
        inclusions_possibles_abscisse = Find.__potential_inclusions(liste_abscisse)
        inclusions_possibles_ordonne =  Find.__potential_inclusions(liste_ordonne)
        inclusions_possibles =Find.__intersection(inclusions_possibles_ordonne, inclusions_possibles_abscisse)
        for polygone1 in range(len(inclusions_possibles)):
            for polygone2 in inclusions_possibles[polygone1]:
                grid = GridPointInPolygon(polygones[polygone2])
                grid.determining_center_points(10,10)
                grid.center_points_inclusion_test()
                if grid.is_polygon_include(polygones[polygone1]):
                    inclusions[polygone1] = polygone2
                    break
        return inclusions
