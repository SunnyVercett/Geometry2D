#! /usr/bin/env python
#coding=utf-8

# functions such as determine whether a point is in a segment, or two lines are horizontal or vertical,
# or a point is in a polygon 

import math

from Geo2DExceptions import *
from Geo2DElements import *
        

def isInSegment(p,e):
    '''To determine whether a point is on a line segment. End point of the segment included.'''
    
    if not isinstance(p,Point2D):
        raise GeometryTypeError("A non-point object encountered in function 'isInSegment()'.")
    if not isinstance(e,Segment2D):
        raise GeometryTypeError("A non-segment object encountered in function 'isInSegment()'.")
    
    # if the segment is vertical or horizontal
    if e.slope==0:    # horizontal
        return p.y==e.startPoint.y and (e.startPoint.x<=p.x<=e.endPoint.x or e.endPoint.x<=p.x<=e.startPoint.x)
    elif e.slope==infinity:    # vertical
        return p.x==e.startPoint.x and (e.startPoint.y<=p.y<=e.endPoint.y or e.endPoint.y<=p.y<=e.startPoint.y)
    
    # if the point is the start point or end point of the segment
    if p==e.startPoint or p==e.endPoint:
        return True
    
    # if the point and the segment start point have either the same x displace or y displace, to avoid ZeroDivisionError
    if p.x==e.startPoint.x:
        return p.y==e.startPoint.y
    if p.y==e.startPoint.y:
        return p.x==e.startPoint.x
    
    # other circumstances
    c1 = ((e.endPoint.x-p.x)/(p.x-e.startPoint.x)==(e.endPoint.y-p.y)/(p.y-e.startPoint.y))    # this point is on the line in which the segment exists
    
    minX = min(e.startPoint.x,e.endPoint.x)
    maxX = max(e.startPoint.x,e.endPoint.x)
    minY = min(e.startPoint.y,e.endPoint.y)
    maxY = max(e.startPoint.y,e.endPoint.y)
    c2 = (minX<=p.x<=maxX and minY<=p.y<=maxY)
            
    return c1 and c2


def isParallel(l1,l2):
    '''Check whether two lines where two segments live in are parallel.'''
    if not isinstance(l1,Segment2D):
        raise GeometryTypeError("Error encountered in determine parallel-ness. First parameter is not a segment or line.")
    elif not isinstance(l2,Segment2D):
        raise GeometryTypeError("Error encountered in determine parallel-ness. Second parameter is not a segment or line.")
    elif l1.yIntercept==l2.yIntercept and l1.xIntercept==l2.xIntercept:    # a str ('infinity') and a float can compare
        raise CoincidedLinesException("Two lines are coincide.")
    else:
        return l1.slope==l2.slope# and l1.yIntercept!=l2.yIntercept and l1.xIntercept!=l2.xIntercept
    
    
def isVertical(l1,l2):
    '''Check whether two lines where two segments live in are vertical.'''
    if not isinstance(l1,Segment2D):
        raise GeometryTypeError("Error encountered in determine vertical-ness. First parameter is not a segment or line.")
    elif not isinstance(l2,Segment2D):
        raise GeometryTypeError("Error encountered in determine vertical-ness. Second parameter is not a segment or line.")
    elif l1.yIntercept==l2.yIntercept and l1.xIntercept==l2.xIntercept:    # a str ('infinity') and a float can compare
        raise CoincidedLinesException("Two lines are coincide.")
    elif l1.slope==0 and l2.slope==infinity:
        return True
    elif l1.slope==infinity and l2.slope==0:
        return True
    else:
        return l1.slope*l2.slope==-1


def getDistance(e1,e2):    # could be either of two points or two lines, or a mixture of the two
    '''Get distance between two points or two parallel lines or a point to a line.'''
    
    if isinstance(e1,Point2D):
        if isinstance(e2,Point2D):    # generate the distance between two points
            dx = float(e1.x)-e2.x
            dy = float(e1.y)-e2.y
            return math.sqrt(dx*dx+dy*dy)
    
        elif isinstance(e2,Segment2D):    #     # generate the distance of a segment to a point, where a segment is equal to a line
            if e2.slope==0:
                return abs(e1.y-e2.startPoint.y)
            elif e2.slope==infinity:
                return abs(e1.x-e2.startPoint.x)
            else:
                k1 = e2.slope
                b1 = e2.yIntercept
                k2 = -1.0/k1      # k2 and b2 are to describe the vertical line to e2
                b2 = e1.y-e1.x*k2
                _x = (b2-b1)/(k2-k1)
                _y = k2*_x+b2    # _x and _y are the coordinates of the intersect
                dx = e1.x-_x
                dy = e1.y-_y
                return math.sqrt(dx*dx+dy*dy)
            
        else:
            raise GeometryTypeError("Could not generate distance with given parameters (second one).")
    
    elif isinstance(e1,Segment2D):
        if isinstance(e2,Point2D):    # generate the distance of a line to a point
            if e1.slope==0:
                return abs(e1.startPoint.y-e2.y)
            elif e1.slope==infinity:
                return abs(e1.startPoint.x-e2.x)
            else:
                k1 = e1.slope
                b1 = e1.yIntercept
                k2 = -1.0/k1
                b2 = e2.y-e2.x*k2
                _x = (b2-b1)/(k2-k1)
                _y = k2*_x+b2
                dx = e2.x-_x
                dy = e2.y-_y
                return math.sqrt(dx*dx+dy*dy)
        
        elif isinstance(e2,Segment2D):    # generate the distance of two parallel lines
            if e1.slope!=e2.slope:
                raise CrossingLinesNoDistanceError("Two given lines are not parallel, and thus they have no distance.")
            elif e1.slope==0:
                return abs(e1.startPoint.y-e2.startPoint.y)
            elif e1.slope==infinity:
                return abs(e1.startPoint.x-e2.startPoint.x)
            else:
                #k11 = e1.slope     # k11 and b11 are to describe the e1 segment
                #b11 = e1.yIntercept
                #k12 = e2.slope          # k12 and b12 are to describe the e2 segment
                #b12 = e2.yIntercept
                x1 = 2.0
                y1 = x1*e1.slope+e1.yIntercept    # x1 and y1 are the coordinates if a point (2.0, y1) on the e1 segment
                k2 = -1.0/e1.slope
                b2 = y1-k2*x1                     # k2 and b2 are to describe the vertical line
                x2 = (e2.yIntercept-b2)/(e2.slope-k2)
                y2 = e2.slope*x2+e2.yIntercept
                dx = x2-x1
                dy = y2-y1
                return math.sqrt(dx*dx+dy*dy)
            
        else:
            raise GeometryTypeError("Could not generate distance with given parameters (second one).")
            
    else:
        raise GeometryTypeError("Could not generate distance with given parameters (first one).")


def getIntersect(s1,s2,onLine=0):
    '''receive two segment objects, 3rd parameter is to decide whether intersect on the line but not the segment is acceptable.'''
    if not isinstance(s1,Segment2D):
        raise GeometryTypeError("A non-segment object encountered as the first parameter to get the intersect.")
    if not isinstance(s2,Segment2D):
        raise GeometryTypeError("A non-segment object encountered as the second parameter to get the intersect.")
    if isParallel(s1,s2):
        raise ParallelLineException("Cannot get intersection of the two segments as they are parallel.")
    
    if not s1.yIntercept:    # s1 is vertical
        _intersect = Point2D(s1.startPoint.x,s2.slope*s1.startPoint.x+float(s2.yIntercept))
    elif not s2.yIntercept:    # s2 is vertical
        _intersect = Point2D(s2.startPoint.x,s1.slope*s2.startPoint.x+float(s1.yIntercept))
    else:
        k1 = float(s1.slope)
        b1 = float(s1.yIntercept)
        k2 = float(s2.slope)
        b2 = float(s2.yIntercept)
        x = -(b2-b1)/(k2-k1)
        y = k1*x+b1
        _intersect = Point2D(x,y)
    
    if isInSegment(_intersect,s1) and isInSegment(_intersect,s2):
        return _intersect
    else:
        if onLine:
            return _intersect
        else:
            raise NoIntersectError("Given segments have an intersect not in either of the segments.")


def getIntersect_horizontal(p,e):    # this function is only used in "isInPolygon" function. It should not be uesd else where.
    '''Get the intersect of a horizontal line through the point p and another line. Return a Point2D object.'''
    
    if not isinstance(p,Point2D):
        raise GeometryTypeError("A non-point object encountered in function 'isInSegment()'.")
    if not isinstance(e,Segment2D):
        raise GeometryTypeError("A non-segment object encountered in function 'isInSegment()'.")
    
    #if e.slope==0:
    #    raise HorizontalLineException("This line is horizontal. No intersect can be found.")
    # 
    #minY = min(e.startPoint.y,e.endPoint.y)
    #maxY = max(e.startPoint.y,e.endPoint.y)
    #if minY>p.y or maxY<p.y:
    #    raise NoIntersectError("No intersect between horizontal line through this point and the segment.")
    # these two conditions are excluded in 'isInPolygon' function before call this function
    
    if p.y==e.startPoint.y:
        return e.startPoint    # the intersect is the start point of the segment
    
    if e.yIntercept:    # has a valid y-axis intercept
        return Point2D((p.y-e.yIntercept)/e.slope,p.y)
    else:    # vertical edge
        return Point2D(e.startPoint.x,p.y)


def getIntersect_vertical(p,e):    # this function is only used in "isInPolygon" function. It should not be uesd else where.
    '''Get the intersect of a vertical line through the point p and another line. Return a Point2D object.'''
    
    if not isinstance(p,Point2D):
        raise GeometryTypeError("A non-point object encountered in function 'isInSegment()'.")
    if not isinstance(e,Segment2D):
        raise GeometryTypeError("A non-segment object encountered in function 'isInSegment()'.")
    
    if p.x==e.startPoint.x:
        return e.startPoint    # the intersect is the start point of the segment
    
    if e.xIntercept:
        return Point2D(p.x,e.yIntercept+e.slope*p.x)
    else:
        return Point2D(p.x,e.startPoint.y)


def isInPolygon(p,polygon):
    '''To determine whether a point is in a polygon, including its edge.'''
    
    if not isinstance(p,Point2D):
        raise GeometryTypeError("A non-point object encountered in function 'isInPolygon()'.")
    if not isinstance(polygon,Polygon2D):
        raise GeometryTypeError("A non-polygon object encountered in function 'isInPolygon()'.")
    
    intersectHorizontal_infinite = 0
    intersectVertical_infinite = 0
    intersectsUp = 0
    intersectsUp_infinite = 0    # an edge is vertical so there are actually infinite intersects
    intersectsDown = 0
    intersectsDown_infinite = 0
    intersectsRight = 0
    intersectsRight_infinite = 0    # an edge is horizontal se there are actually infinite intersects
    intersectsLeft = 0
    intersectsLeft_infinite = 0
    
    for thisEdge in polygon.edgeList:     # segments of the polygon one by one   
        if isInSegment(p,thisEdge):    # if this point is on the edge of the polygon:
            return True
        
        intersect = None
        intersect_infinite = None
        
        if (thisEdge.startPoint.y-p.y)*(thisEdge.endPoint.y-p.y) <= 0:    # cast a horizontal line
            if thisEdge.slope==0:    # this edge is horizontal. only happens if the edge is a part of the horizontal line, in which case there are infinite intersects
                intersect_infinite = thisEdge.startPoint
            else:
                if p.y==thisEdge.endPoint.y:    # exclude end point of each edge, to avoid repeat
                    intersect = None
                else:
                    intersect = getIntersect_horizontal(p,thisEdge)
                    
            if intersect:    # the horizontal line through this point has an intersect with this edge
                if intersect.x<p.x:
                    intersectsLeft += 1
                else:
                    intersectsRight += 1
                    
            if intersect_infinite:
                if intersect_infinite.x<p.x:
                    intersectsLeft_infinite += 1
                else:
                    intersectsRight_infinite += 1
                
        if (thisEdge.startPoint.x-p.x)*(thisEdge.endPoint.x-p.x) <= 0:    # cast a vertical line
            if thisEdge.slope==infinity:    # this edge is vertical. only happens if the edge is on the vertical line, in which case there are infinite intersects
                intersect_infinite = thisEdge.startPoint    # then the start point of the edge is counted as the only intersect
            else:
                if p.x==thisEdge.endPoint.x:    # exclude end point of each edge, to avoid repeat
                    intersect = None
                else:
                    intersect = getIntersect_vertical(p,thisEdge)
                
            if intersect:
                if intersect.y<p.y:
                    intersectsDown += 1
                else:
                    intersectsUp += 1
                    
            if intersect_infinite:
                if intersect_infinite.y<p.y:
                    intersectsDown_infinite += 1
                else:
                    intersectsUp_infinite += 1
                    
    if intersectsRight_infinite:     # if on right side there is edge(s) coincident with the line
        if not intersectsRight&1:    # if it's even
            intersectsRight += 1      # then change to odd
    if intersectsLeft_infinite:
        if not intersectsLeft&1:
            intersectsLeft += 1
    if intersectsUp_infinite:
        if not intersectsUp&1:
            intersectsUp += 1
    if intersectsDown_infinite:
        if not intersectsDown&1:
            intersectsDown += 1
    
    c1 =  intersectsUp&1 and intersectsDown&1 and intersectsLeft&1 and intersectsRight&1
    return bool(c1)#,intersectsUp,intersectsDown,intersectsLeft,intersectsRight
    
    


if __name__=='__main__':
    p1 = Point2D(2,2)
    p2 = Point2D(2,4)
    #print getDistance(p1,p2)
    l1 = Segment2D(p1,p2)
    p3 = Point2D(1,3)
    #print getDistance(l1,p3)
    p4 = Point2D(3,3)
    l2 = Segment2D(p3,p4)
    print isVertical(l1,l2)
    intersect = getIntersect(l1,l2)
    print intersect.x,intersect.y
    
    p71 = Point2D(0,0)
    p72 = Point2D(0,1)
    p73 = Point2D(-1,1)
    p74 = Point2D(-1,-1)
    p75 = Point2D(3,-1)
    p76 = Point2D(3,0)
    p77 = Point2D(2,0)
    p78 = Point2D(2,1)
    p79 = Point2D(1,1)
    p80 = Point2D(1,0)
    #p71 = Point2D(2,0)
    #p72 = Point2D(0,0)
    #seg = Segment2D(p71,p72)
    polygon = Polygon2D(p71,p72,p73,p74,p75,p76,p77,p78,p79,p80)
    p7 = Point2D(-1.5,0)
    #intersectsDown = getIntersect_vertical(p7,seg)
    #print intersectsDown.x,intersectsDown.y
    print isInPolygon(p7,polygon)
