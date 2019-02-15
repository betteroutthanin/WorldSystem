import Config
from Objects.Object import Object
from Core.Base import Base
from Core.Point import Point
from HandOfGod import HandOfGod
from Objects.GOB import GOB

import copy
import glob

class Universe(Base, HandOfGod):
    ##############################################################    
    def __init__(self):
        Base.__init__(self)
        self.loggingPrefix = "Universe"
        
        ### Core buckets
        self.objects = {}        
        
        ### Object ID related goodies
        self.NextID = 0
        self.IDGaps = []
                
        self.LogMe("booted")
    
    ##############################################################
    def LoadFromDisk(self):
        self.LogMe("LoadFromDisk: ******************* Started")
        fileList = glob.glob(Config.picklePath + "*.p")
        for filePath in fileList:
            self.LogMe("*** Loading " + filePath)
            object = Object.Load(self, filePath)
            self.LoadObjectToUniverse(object)
            if isinstance(object, GOB):
                if self.NextID <= object.id:
                    self.NextID = object.id + 1
            self.LogMe(object)
            self.LogMe("*** Loading " + filePath + " . . . . Completed")

        self.LogMe("LoadFromDisk: ******************* Ended")
        self.LogMe("LoadFromDisk: Next ID = " + str(self.NextID))

    ##############################################################
    def Tick(self):
        self.LogMe("Tick")

        # Must back a copy of the dict keys - the dict may change size
        # during the tick cycles
        objectIDsToTick = list(self.objects.keys())

        buffer = ""
        for objectID in objectIDsToTick:
            object = self.GetObjectByID(objectID)
            if object is not False:
                object.Tick()
                buffer += str(object) + "\n"

        # save time
        for object in self.objects.values():
            object.Save()
            
        # Dump States
        with open(Config.snapShotPath, "w") as myfile:
                myfile.write(buffer + "\n")
    
    ##############################################################
    def GetObjectByID(self, objectID):
        # quicker than looking through the entire object array for none
        if objectID is None:
            return False

        if objectID in self.objects:
            return self.objects[objectID]        

        self.LogMe("GetObjectByID: Failed to find object in objects dict, id=" + str(objectID))
        return False
    
    ##############################################################
    def AllocateObjectID(self):
        NewID = self.NextID
        self.NextID = self.NextID + 1
        return NewID