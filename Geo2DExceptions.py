#! /usr/bin/env python
#coding=utf-8

# define exceptions in 2D geometry

class CoordinateNotDigitException(Exception):
    pass

class CoincidedPointsException(Exception):
    pass

class CoincidedLinesException(Exception):
    pass

class ParallelLineException(Exception):
    pass

class VerticalLineException(Exception):
    pass

class HorizontalLineException(Exception):
    pass

class PolygonVertexNotCompleteException(Exception):
    pass

class NoIntersectError(Exception):
    pass

class CrossingLinesNoDistanceError(Exception):
    pass

class GeometryTypeError(Exception):
    pass

