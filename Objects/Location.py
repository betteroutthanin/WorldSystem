import Config
from Objects.Object import Object
from Core.Point import Point

import math

class Location(Object):
    ##############################################################    
    def __init__(self):
        Object.__init__(self)
        self.loggingPrefix = "Location"
        
        self.trf = False
        self.blf = False
       
        self.LogMe("booted")

    ##############################################################    
    def RemoveChildByID(self, childID, noParentIsOk = False):
        Object.RemoveChildByID(self, childID, noParentIsOk)
        if len(self.childrenID) == 0:            
            self.universe.RemoveObjectFromUniverseByID(self.id)
    
    ##############################################################    
    def SetUp(self, pointInSpace):
        # Locations are defined by two points
        # A = Top Right Front (TRF)
        # B = Bottom Left Rear (BLR)
        x = pointInSpace.x
        y = pointInSpace.y
        z = pointInSpace.z
        
        r = Config.locationRadius
        self.trf = Point(x+r, y+r, z-r)
        self.blf = Point(x-r, y-r, z+r)
        
        self.pos = pointInSpace
        self.id = str(x) + "^" + str(y) + "^" + str(z)
        self.LogMe("SetUp: Compete")

    ##############################################################    
    def PointToLocationLabel(self, point):
        # Location Labels are based on the center point of the location
        # point must be a Point
        if isinstance(point, Point) is False:
            self.Boom("PointToLocationLabel: point must be a Point but is not, " + str(point))
            return False

        # add radius to position
        # divide by size
        # floor
        x = float(point.x)
        y = float(point.y)
        z = float(point.z)

        x += Config.locationRadius
        y += Config.locationRadius
        z += Config.locationRadius

        x = x / Config.locationSize
        y = y / Config.locationSize
        z = z / Config.locationSize

        x = math.floor(x)
        y = math.floor(y)
        z = math.floor(z)
        locPoint = Point(x, y, z)    

        locationLabel = str(x) + "^" + str(y) + "^" + str(z)
        return locationLabel, locPoint