#!/usr/bin/env python3

from geo.polygon import Polygon
from ray_casting import RayCast
from grid_point_in_polygon import GridPointInPolygon
from listWithTab import ListeTab
from geo.tycat import tycat
import time

#variables gloables
IN = True
OUT = False

class Find:
    @staticmethod
    def __poly_extrem_coord(polygones,coord):
        """
        Return limits coordinate in abscissa or ordinate of each polygon in polygones sorted 

        Args:
             polygones (array of Polygon)
        
        Returns:
            liste of tuple : (abscissa or ordiate extrem value of polygon i) * (enter or get out 
                              of the polygoni) * i   
            sorted by the value
        """
        liste = []
        for polygone in enumerate(polygones):
            point_min,point_max = polygone[1].bounding_quadrant().limits(coord)
            liste.append((point_min,IN,polygone[0]))
            liste.append((point_max,OUT,polygone[0]))
        return sorted(liste)

    @staticmethod
    def __list_with_area(polygones):
        """
        Args:
            polygones (array of Polygon)
        Returns;
            liste of Polygone sorted by area
        """
        tab = []
        for (i,polygone) in enumerate(polygones):
            tab.append((abs(polygone.area()),i))
        return(tab)

    
    @staticmethod
    def __potential_inclusions(liste_point,taille):
        """
        Brows the list of points sorted by value and when it's the first time that we see a polygon we add it to a linked list and when we see it for the second time it is deleted fom the list and all         its childs in an array    
        Args:
            liste_point : list of tuple of point min and max of each polygon sorted by value
            taille : number of polygon 
        Return: 
            An array of array where ith element is a array of value that represent the polygons where the ith polygon can be inclued in
        """
        currentlist = ListeTab(taille)
        inclusion_possible = [[] for _ in range(len(liste_point)//2)]
        for (_, IN, id) in liste_point:
            if IN:
                currentlist.insert(id)
            else:
                inclusion_possible[id] = currentlist.delete(id)
        return inclusion_possible           

    @staticmethod
    def __intersection(tab1,tab2):
        """
        Args:
            tab1, tab2 :  array of array with the same lenght
        Returns:
            An array where the i-th element is the intersection between the i-th element of tab1 and tab2
        """
        assert(len(tab1) == len(tab2))
        tab = [[] for _ in range(len(tab1))]
        for i in range(len(tab1)):
            tab[i] = [id for id in tab1[i] if id in tab2[i]]
        return tab

    
    def area_check(polygones):
        """
        Args: 
             polygones: array of Polygon
        Returns:
             An array where the i-th element is the number of polygon that the i-th is inclued in using the area of each polygon to order the tests
        """
        inclusions : list = [-1 for _ in range(len(polygones))]
        polygones_sorted = sorted(Find.__list_with_area(polygones))
        tab_grid = [None for _ in range(len(polygones))]
        # each polygon is tested whith others polygon which have a bigger area to see if it's included or not
        for i in range(len(polygones_sorted)):
            for j in range(i+1,len(polygones_sorted)):
                _,polygone1 = polygones_sorted[i]
                _,polygone2 = polygones_sorted[j]
                if tab_grid[polygone2] == None:
                    tab_grid[polygone2] = GridPointInPolygon(polygones[polygone2], 20)
                if tab_grid[polygone2].is_polygon_include(polygones[polygone1]):
                    inclusions[polygone1] = polygone2
                    break
        return inclusions
    
    def area_local_vision(polygones, algo, display_center_point = False, display_fast_voxel = False):
        """
        use poly_extrem_coord to create to array of potential inclusion for each polygon, one in the horizontal way and the other in the vertival way. Finally the both result are intersected and we 
        find exctly which polygon is included in the other.
        
        Args:
            polygones: array of Polygon
            display_center_point : bool to display center points IN, OUT and MAYBE
            display_fast_voxel : bool to display each voxel intersected by all polygons
        Return:
            An array where the i-th element represent the polygone that the i-th polygone is inclued in"""
        x = 0
        y = 1
        # step 1
        # Brows the plan in the horizontal then in the vertival way to determine potential inclusion for each polygon
        assert(algo == "raycast" or algo == "grid")
        liste_abscisse = Find.__poly_extrem_coord(polygones,x)
        liste_ordonne = Find.__poly_extrem_coord(polygones,y)      
        inclusions_possibles_abscisse = Find.__potential_inclusions(liste_abscisse,len(polygones))
        inclusions_possibles_ordonne =  Find.__potential_inclusions(liste_ordonne,len(polygones))
        # intersection of results
        inclusions_possibles =Find.__intersection(inclusions_possibles_ordonne, inclusions_possibles_abscisse)
        tab_grid = [None for _ in range(len(polygones))]
        inclusions : list = [-1 for _ in range(len(polygones))]
        # state 2
        # Each polygon is tested whith other polygon determined in inclusion_possible
        for polygone1 in range(len(inclusions_possibles)):
            for polygone2 in inclusions_possibles[polygone1]:
                if algo == "raycast":
                    if RayCast.is_include(polygones[polygone1],polygones[polygone2]):
                        inclusions[polygone1] = polygone2
                        break
                if algo == "grid":                
                    if tab_grid[polygone2] == None:
                        tab_grid[polygone2] = GridPointInPolygon(polygones[polygone2], 400)
                        # display for debug
                        affiche_fast_voxel = []
                        if display_fast_voxel:
                            for grid in tab_grid:
                                if grid is not None:
                                    for temp_cell in grid.cells:
                                        for cell in temp_cell:
                                            if cell.edges :
                                                affiche_fast_voxel.append(cell.cell_polygon)
                    if tab_grid[polygone2].is_polygon_include(polygones[polygone1]):
                            inclusions[polygone1] = polygone2
                            break
        #display for debug
        if display_fast_voxel and display_center_point :
            for grid in tab_grid:
                if grid:
                    tycat(polygones,grid.sure_in,grid.sure_out, grid.sure_maybe, affiche_fast_voxel)
        elif display_fast_voxel and not display_center_point:
            tycat(polygones, affiche_fast_voxel)
        elif not display_fast_voxel and display_center_point:
            for grid in tab_grid:
                if grid:
                    tycat(polygones,grid.sure_in,grid.sure_out, grid.sure_maybe)
                    
                
        return inclusions
