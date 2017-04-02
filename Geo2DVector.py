#! /usr/bin/env python
#coding=utf-8

# vector class of 2d geometry

import math

from Geo2DElements import *


class Vector2D(PlaneGeometryComponent):
    def __init__(self,x,y):
        self.x = 0.0
        self.y = 0.0
        self.polarAngle = 0.0
        self.norm = 0.0
        
        if (not isinstance(x,int)) and (not isinstance(x,float)):
            raise CoordinateNotDigitException("Invalid parameter type for the x-coordinate to construct a vector.")
        if (not isinstance(y,int)) and (not isinstance(y,float)):
            raise CoordinateNotDigitException("Invalid parameter type for the y-coordinate to construct a vector.")
        self.x = float(x)
        self.y = float(y)
        
        self.polarAngle = math.atan2(self.y,self.x)
        self.norm = (self.x*self.x + self.y*self.y)**0.5
        
        
    def __add__(self,other):
        if not isinstance(other,Vector2D):
            raise GeometryTypeError("A non-vector object encountered when trying to determine equivalence of two vectors.")
        
        x = self.x+other.x
        y = self.y+other.y
        return Vector2D(x,y)
    
    
    def __eq__(self,other):
        return self.x==other.x and self.y==other.y
    
    
    def __str__(self):
        return "Vector2D <%.2f, %.2f>" %(self.x,self.y)
    
    

def getInnerProduct(v1,v2):
    if not isinstance(v1,Vector2D):
        raise GeometryTypeError("A non-vector object encountered as the first parameter to get the inner product.")
    if not isinstance(v2,Vector2D):
        raise GeometryTypeError("A non-vector object encountered as the second parameter to get the inner product.")
    
    return v1.x*v2.x + v1.y*v2.y




if __name__=='__main__':
    v1 = Vector2D(1,1)
    v2 = Vector2D(1,0)
    
    print v1
    print v1==v2
    print (v1+v2)
    print getInnerProduct(v1,v2)