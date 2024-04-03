#!/usr/bin/env python3
"""
fichier principal pour la detection des inclusions.
ce fichier est utilise pour les tests automatiques.
attention donc lors des modifications.
"""
from geo.tycat import tycat
from geo.point import Point
from tycat import read_instance
from tycat import print_polygons
from ray_casting import RayCast
from find import Find
from grid_point_in_polygon import GridPointInPolygon
import sys



    
def main():
    """
    charge chaque fichier .poly donne
    trouve les inclusions
    affiche l'arbre en format texte
    """
    for fichier in sys.argv[1:]:
        polygones = read_instance(fichier)
        inclusions = Find.area_local_vision(polygones, "grid", display_center_point = False, display_fast_voxel = False)
        print(inclusions)

if __name__ == "__main__":
    main()
