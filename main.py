#!/usr/bin/env python3
"""
fichier principal pour la detection des inclusions.
ce fichier est utilise pour les tests automatiques.
attention donc lors des modifications.
"""
import sys
from geo.tycat import tycat
from geo.point import Point
from tycat import read_instance
from ray_casting import RayCast
from find import Find
from grid_point_in_polygon import GridPointInPolygon

def trouve_inclusions(polygones):
    """
    renvoie le vecteur des inclusions
    la ieme case contient l'indice du polygone
    contenant le ieme polygone (-1 si aucun).
    (voir le sujet pour plus d'info)
    """
    inclusions : list = [-1 for _ in range(len(polygones))]

    for i, polygon1 in enumerate(polygones):
        for j, polygon2 in enumerate(polygones):
            if i != j and RayCast.is_include(polygon1, polygon2):        
                inclusions[i] = j
                break
    return inclusions


def test_grid(polygones):
    polygon1 = polygones[0]
    #tycat(polygon1.segments())
    polygon2 = polygones[1]
    grid2 = GridPointInPolygon(polygon2)
    grid2.determining_center_points(10,10)
    grid2.center_points_inclusion_test()

    #tycat(polygon2.segments())
    grid1 = GridPointInPolygon(polygon1)
    grid1.determining_center_points(10, 10)
    grid1.center_points_incxlusion_test()
    print(grid1.is_polygon_include(polygon2))
    print(grid2.is_polygon_include(polygon1))
    
    # points = [Point(point) for point in quad_tree.bounding_quadrant.get_arrays()]
    # tycat(test_point,  list(grid.center_points.values()), polygon1.segments(), polygon2.segments())


    
def main():
    """
    charge chaque fichier .poly donne
    trouve les inclusions
    affiche l'arbre en format texte
    """
    for fichier in sys.argv[1:]:
        polygones = read_instance(fichier)
        inclusions: list = Find.area_local_vision(polygones)
        #print("naif :")
        print(inclusions)
        #inclusions = test_grid(polygones)
        #print(inclusions)

if __name__ == "__main__":
    main()
