#!/usr/bin/env python3

from geo.polygon import Polygon
from geo.point import Point
from ray_casting import RayCast

class Tree:

    def __init__(self):
        self.parent = None
        self.value = None
        self.childs = []

    def __str__(self):
        char = ""
        if self.value is not None :
            char += str(self.value) + " -> [ "
            for child in self.childs:
                char += str(child)
            char += " ]"
        return char

    def set_value(self,value):
        self.value = value

    def add_childs(self,child):
        self.childs.append(child)
        child.parent = self
        
    def set_parent(self,parent):
        self.parent = parent

    def test_inclusion_with_childs(self,inclusions,polygones):
        i = self.value
        for child in self.childs:
            if child.value != None:
                #print(child)
                j = child.value
                #print("test ", j , " dans ",i)
                if RayCast.is_include(polygones[j],polygones[i]):
                    inclusions[j] = i
                    #print("pass")
                child.test_inclusion_with_childs(inclusions,polygones)
