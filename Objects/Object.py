import Config
from Core.Base import Base
from Core.Point import Point

import copy
import pickle
import os

class Object(Base):
    ##############################################################    
    def __init__(self):
        Base.__init__(self)        
        self.loggingPrefix = "Object"

        self.id = None
        self.parentID = None
        self.pos = None
        self.childrenID = []
        
        self.universe = None        

        # self.LogMe("booted")

        
    ##############################################################
    def LogMe(self, message):
        buffer = "id=" + str(self.id) + ": " + message
        Base.LogMe(self, buffer)

    ##############################################################    
    def Tick(self):
        pass
    
    ##############################################################    
    def AddChildByID(self, childID):
        self.LogMe("AddChildByID: Attempting to add child object, id=" + str(childID))
        
        # Can't add the same child twice
        if childID in self.childrenID:
            self.Boom("AddChildByID: Already a child of mine, id=" + str(childID))
            return False
        
        # Can we resolve the child object
        childObject = self.universe.GetObjectByID(childID)
        if childObject is False:
            self.Boom("AddChildByID: Failed to get child object, id=" + str(childID))
            return False        

        # do the transaction
        self.childrenID.append(childID)        
        childObject.parentID = self.id        
        
        self.LogMe("AddChildByID: Child object added, id=" + str(childID))        
        return True
        
    ##############################################################    
    def RemoveChildByID(self, childID, noParentIsOk = False):
        # self.LogMe("RemoveChildByID: Attempting to remove child object, id=" + str(childID))            
        
        # Do we even own this child
        if childID not in self.childrenID:
            self.Boom("RemoveChildByID: Not a child of mine, id=" + str(childID))            
            return False

        # Can we resolve the child object
        childObject = self.universe.GetObjectByID(childID)        
        if childObject is False:
            self.Boom("RemoveChildByID: Failed to get child object, id=" + str(childID))
            return False

        # In some cases the universe will take care of parenting the object
        # the noParentIsOk of True implies that the universe is ok with
        # skipping these checks
        # If noParentIsOk then do the checks - this is the default option
        if noParentIsOk is False:
            # It is illegal to remove a child if you have nowhere to send it
            if self.parentID is None:            
                self.Boom("RemoveChildByID: Current object has no parent to pass the object to, id=" + str(childID))
                return False

            # Make sure the new parent is real
            newParentObject = self.universe.GetObjectByID(self.parentID)
            if newParentObject is False:
                self.Boom("RemoveChildByID: Failed to find new parent object, id=" + str(self.parentID))
                return False

            newParentObject.AddChildByID(childID)

        # do the transaction
        self.childrenID.remove(childID)        
        
        # self.LogMe("RemoveChildByID: Child object removed, id=" + str(childID))            
        return True
    
    ##############################################################    
    def GetAllIDsRecursive(self):
        listOfIDs = []

        # add ourselves to the list
        listOfIDs.append(self.id)

        for childID in self.childrenID:
            # Resolve the child
            childObject = self.universe.GetObjectByID(childID)
            if childObject is False:
                self.Boom("GetAllIDsRecursive: Failed to resolve the child object, id=" + childID)
                return False

            childResult = childObject.GetAllIDsRecursive()
            if childResult is False:
                self.Boom("GetAllIDsRecursive: Child object failed to return valid results, id=" + childID)

            # Join the party
            listOfIDs = listOfIDs + childResult
        return listOfIDs

    ##############################################################    
    def SelfDestuct(self):
        # So, you are going to die
        self.LogMe("SelfDestuct: Started")

        # This method is meant to be a suicide pack, ie kill the children first
        # We should have no children
        if len(self.childrenID) > 0:
            self.Boom("SelfDestuct: I have childern and I shouldn't have")
            return False        

        # Better tell my parents
        if self.parentID is not None:
            parentObject = self.universe.GetObjectByID(self.parentID)
            if parentObject is False:
                self.Boom("SelfDestuct: Failed to find parent object, id=" + str(self.parentID))
                return False

            parentObject.childrenID.remove(self.id)
            self.parentID = None

        self.Delete()

        self.LogMe("SelfDestuct: So it is done")
        return True
        
        
    ##############################################################    
    def IsValid(self):
        if self.id is None: return False
        return True
        
    ##############################################################    
    def __str__(self):
        buffer = ""
        buffer += "id:" + str(self.id)
        buffer += " parentID:" + str(self.parentID)
        buffer += " pos:{" + str(self.pos) + "}"
        buffer += " childrenID:{" + str(self.childrenID) + "}"
        
        return buffer

    ##############################################################
    ###### Loading and saving
    ##############################################################
    def Save(self):
        filePath = Config.picklePath + str(self.id) + ".p"
        file = open(filePath, 'wb')
        pickle.dump(self, file)
        file.close()

    ##############################################################
    def Load(self, fileName):
        file = open(fileName, 'rb')
        pickledObject = pickle.load(file)   
        file.close()
        return pickledObject

    ##############################################################
    def Delete(self):
        filePath = Config.picklePath + str(self.id) + ".p"
        os.remove(filePath)

 