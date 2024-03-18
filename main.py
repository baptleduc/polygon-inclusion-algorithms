#!/usr/bin/env python3
"""
fichier principal pour la detection des inclusions.
ce fichier est utilise pour les tests automatiques.
attention donc lors des modifications.
"""
import sys
from tycat import read_instance
from ray_casting import RayCast
from find import Find

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


def main():
    """
    charge chaque fichier .poly donne
    trouve les inclusions
    affiche l'arbre en format texte
    """
    for fichier in sys.argv[1:]:
        polygones = read_instance(fichier)
        Find.area_check(polygones)
        #inclusions: list = Find.naif(polygones)
        #print("naif :")
        #print(inclusions)
        inclusions = Find.area_check(polygones)
        
        print(inclusions)

if __name__ == "__main__":
    main()
