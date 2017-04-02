#! /usr/bin/env python
#coding=utf-8

# define classes (points, lines, segments, polygons, etc) of 2D geometry

from Geo2DExceptions import *


infinity = "infinity"


class PlaneGeometryComponent(object):    # a visual class for geometry objects
    pass


class Point2D(PlaneGeometryComponent):
    def __init__(self,x,y):    # receive two floats
        self.x = 0.0
        self.y = 0.0
        
        if (type(x)!=type(0)) and (type(x)!=type(0.0)):
            raise CoordinateNotDigitException("Invalid parameter type for the x-coordinate to construct a point.")
        if (type(y)!=type(0)) and (type(y)!=type(0.0)):
            raise CoordinateNotDigitException("Invalid parameter type for the y-coordinate to construct a point.")
        self.x = float(x)
        self.y = float(y)
        
    def __eq__(self,other):    # receive a point2d object
        if not isinstance(other,Point2D):
            raise GeometryTypeError("A non-point object encountered when trying to determine equivalence of two points.")
        
        return (other.x==self.x) and (other.y==self.y)
    
    
    def __str__(self):
        return "Point2D <%.2f, %.2f>" %(self.x,self.y)
        
        
class Segment2D(PlaneGeometryComponent):
    def __init__(self,p1,p2):    # receive two point2d objects
        self.startPoint = Point2D(0,0)
        self.endPoint = Point2D(0,0)
        self.slope = 0.0
        self.xIntercept = 0.0
        self.yIntercept = 0.0
        
        # convert to point if it can, else raise an error
        if not isinstance(p1,Point2D):    # can only be a tuple or a list with two ints or floats, otherwise an error will be raised
            try:
                p1 = Point2D(p1[0],p1[1])
            except CoordinateNotDigitException:
                raise GeometryTypeError("Can not form a segment with the given parameters as no point can be constructed.")
            
        if not isinstance(p2,Point2D):
            try:
                p2 = Point2D(p2[0],p2[1])
            except CoordinateNotDigitException:
                raise GeometryTypeError("Can not form a segment with the given parameters as no point can be constructed.")
        
        if p1==p2:
            raise CoincidedPointsException("The two points have the same coordinates. Cannot construct a line.")
        
        self.startPoint = p1
        self.endPoint = p2
        
        if self.startPoint.y==self.endPoint.y:    # vertical segment
            self.slope = 0.0
            self.xIntercept = None
            self.yIntercept = 1.0*self.startPoint.y
        elif self.startPoint.x==self.endPoint.x:    # horizontal segment
            self.slope = infinity
            self.xIntercept = 1.0*self.startPoint.x
            self.yIntercept = None
        else:
            self.slope = (self.endPoint.y*1.0-self.startPoint.y)/(self.endPoint.x*1.0-self.startPoint.x)
            self.yIntercept = self.startPoint.y-self.slope*self.startPoint.x
            self.xIntercept = 0-(1.0/self.slope)*self.yIntercept
            
            
    def __eq__(self,other):
        if not isinstance(other,Segment2D):
            raise GeometryTypeError("A non-segment object encountered when trying to determine equivalence of two segments.")
        
        return (self.startPoint==other.startPoint and self.endPoint==other.endPoint)
    
    
    def __str__(self):
        return "Segment2D <%.2f, %.2f> <%.2f, %.2f>" %(self.startPoint.x,self.startPoint.y,self.endPoint.x,self.endPoint.y)
            
            
class Polygon2D(PlaneGeometryComponent):
    # edges could intersect with each other, and could partly coincide with each other. 
    # could still be counted as a 'generalized' polygon. So far.
    #vertexList = []
    #edgeList = []    # DO NOT declare attributes here. Declare them in __init__ function
    
    def __init__(self,*pList):    # all parameters are in 'pList' tuple
        self.vertexList = []    # declare attributes here. HERE!
        self.edgeList = []
        
        # pList is a list of floats, the count of which must be even
        if isinstance(pList[0],int) or isinstance(pList[0],float):
            if len(pList)&1 or len(pList)<6:    # length of the list is a odd number, or less than 6 (meaning less than 3 points)
                raise PolygonVertexNotCompleteException("Cannot construct a polygon from the parameters as not enough vertexex.")
            
            lastVertex = None
            for eachFloatIndex in xrange(0,len(pList),2):
                thisVertex = Point2D(pList[eachFloatIndex],pList[eachFloatIndex+1])    # convert these two floats to a point object
                if thisVertex in self.vertexList:
                    raise CoincidedPointsException("Cannot form a polygon with given parameters as the vertexes are coincided.")
                self.vertexList += [thisVertex]
                if lastVertex:
                    if thisVertex==lastVertex:
                        continue    # skip overlapped points
                    thisEdge = Segment2D(lastVertex,thisVertex)    # in this case the last edge will not join into the edgeList
                    if thisEdge in self.edgeList:
                        raise CoincidedLinesException("Cannot form a polygon with given parameters as the edges are coincided.")
                    self.edgeList += [thisEdge]
                lastVertex = thisVertex
                
            finalVertex = Point2D(pList[-2],pList[-1])
            firstVertex = Point2D(pList[0],pList[1])
            finalEdge = Segment2D(finalVertex,firstVertex)
            self.edgeList += [finalEdge]    # fill on the final edge that goes from the final vertex to the first vertex
         
        # pList is a list of tuple or list, each represent a point
        elif isinstance(pList[0],tuple) or isinstance(pList[0],list):
            if len(pList)<3:    # length of the list is less than 3
                raise PolygonVertexNotCompleteException("Cannot construct a polygon from the parameters as not enough vertexex.")
            
            lastVertex = None
            for eachPoint in pList:
                thisVertex = Point2D(eachPoint[0],eachPoint[1])    # convert this tuple or list representing a point to a point object
                if thisVertex in self.vertexList:
                    raise CoincidedPointsException("Cannot form a polygon with given parameters as the vertexes are coincided.")
                self.vertexList += [thisVertex]
                if lastVertex:
                    if thisVertex==lastVertex:
                        continue    # skip overlapped points
                    thisEdge = Segment2D(lastVertex,thisVertex)
                    if thisEdge in self.edgeList:
                        raise CoincidedLinesException("Cannot form a polygon with given parameters as the edges are coincided.")
                    self.edgeList += [thisEdge]
                lastVertex = thisVertex
                
            finalVertex = Point2D(pList[-1][0],pList[-1][1])
            firstVertex = Point2D(pList[0][0],pList[0][1])
            finalEdge = Segment2D(finalVertex,firstVertex)
            self.edgeList += [finalEdge]    # fill on the final edge that goes from the final vertex to the first vertex
            
        # pList is a list of point objects
        elif isinstance(pList[0],Point2D):
            if len(pList)<3:
                raise PolygonVertexNotCompleteException("Cannot construct a polygon from the parameters as not enough vertexex.")
                
            lastVertex = None
            for eachPoint in pList:
                if eachPoint in self.vertexList:
                    raise CoincidedPointsException("Cannot form a polygon with given parameters as the vertexes are coincided.")
                thisVertex = eachPoint
                self.vertexList += [thisVertex]
                if lastVertex:
                    if thisVertex==lastVertex:
                        continue    # skip overlapped points
                    thisEdge = Segment2D(lastVertex,thisVertex)
                    if thisEdge in self.edgeList:
                        raise CoincidedLinesException("Cannot form a polygon with given parameters as the edges are coincided.")
                    self.edgeList += [thisEdge]
                lastVertex = thisVertex
                
            finalEdge = Segment2D(pList[-1],pList[0])
            self.edgeList += [finalEdge]    # fill on the final edge that goes from the final vertex to the first vertex
            
        else:
            raise GeometryTypeError("Can not form a polygon with the given parameters.")
        
                
    def __eq__(self,other):
        if not isinstance(other,Polygon2D):
            raise GeometryTypeError("A non-polygon object encountered when trying to determine equivalence of two polygons.")
        
        condition = 0
        for eachEdge in self.edgeList:
            if eachEdge not in other.edgeList:
                condition += 1    # each vertex in this polygon is in other polygon
        for eachEdge in other.edgeList:
            if eachEdge not in self.edgeList:
                condition += 1    # each vertex in other polygon is in this polygon
                
        return (not condition)
    
    
    def __str__(self):
        strPrint = "Pokygon2D"
        for eachVertex in self.vertexList:
            strPrint += " <%.2f, %.2f>" %(eachVertex.x,eachVertex.y)
            
        return strPrint




if __name__=='__main__':
    p1 = Point2D(1,1)
    p2 = Point2D(0,2)
    p3 = Point2D(-1,1)
    p4 = Point2D(-1,-1)
    p5 = Point2D(0,-2)
    p6 = Point2D(1,-1)
    
    s1 = Segment2D(p1,p2)
    print s1.slope
    s2 = Segment2D(p1,p4)
    print s1.slope
    
    pg1 = Polygon2D(p1,p2,p3,p4,p5,p6)
    pg2 = Polygon2D(p1,p2,p3,p6,p5,p4)
    print pg1
    print pg1==pg2