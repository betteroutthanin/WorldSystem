from Objects.Object import Object
from Core.Point import Point

class GOB(Object):
    ##############################################################    
    def __init__(self):
        Object.__init__(self)
        self.loggingPrefix = "GOB"
       
        self.LogMe("booted")

    ##############################################################    
    def Tick(self):
        pass
        newPos = Point(self.pos.x, self.pos.y, self.pos.z)
        newPos.x += 0.1
        self.universe.MoveMeTo(self, newPos)
       
    ##############################################################    
    def AddChildByID(self, childID):        
        if Object.AddChildByID(self, childID):
            # Parent called was good, GOB specific hooks
            childObject = self.universe.GetObjectByID(childID)
            childObject.pos = None
            #self.LogMe("AddChildByID: Final Child = " + str(childObject))
            return True
        return False


    ##############################################################    
    def RemoveChildByID(self, childID):
        if Object.RemoveChildByID(self, childID):
            # Parent called was good, GOB specific hooks
            childObject = self.universe.GetObjectByID(childID)
            childObject.pos = self.pos
            #self.LogMe("RemoveChildByID: Final Child = " + str(childObject))
            return True
        return False
        