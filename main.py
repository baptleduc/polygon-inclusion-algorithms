#!/usr/bin/env python3
"""
fichier principal pour la detection des inclusions.
ce fichier est utilise pour les tests automatiques.
attention donc lors des modifications.
"""
from tycat import read_instance
from find import Find
from sys import argv


    
def main():
    """
    charge chaque fichier .poly donne
    trouve les inclusions
    affiche l'arbre en format texte
    """
    for fichier in argv[1:]:
        polygones = read_instance(fichier)
        inclusions = Find.area_local_vision(polygones, "raycast", display_center_point = False, display_fast_voxel = False)
        print(inclusions)

if __name__ == "__main__":
    main()
