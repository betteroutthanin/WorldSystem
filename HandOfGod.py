import Config
from Core.Base import Base
from Core.Point import Point
from Objects.Location import Location
from Objects.GOB import GOB

class HandOfGod():
    ##############################################################
    def MoveMeTo(self, object, newPos):
        self.LogMe("MoveMeTo: Object is going to be moved, id=" + str(object.id))
        self.LogMe("MoveMeTo: newPos, id=" + str(newPos))
        # Can't move objects with a pos of None - would imply they are in
        # a location object.  All code below this assumes that the parent
        # will be a location        
        if object.pos is None:
            return False

        # Is the current and newPos the same, if so no work needs to be done        
        if object.pos == newPos:
            return True

        ### Do we need a new location?                
        # Parent object (as a location) will be needed        
        parentObject = self.GetObjectByID(object.parentID)   
        if isinstance(parentObject, Location) is False:
            self.Boom("MoveMeTo: parentObject must be a location and is not")
            return False

        # Get the new parent - it may end up being the same as the current parent                
        newParentObject = self.GetLocationOrCreate(newPos)

        if newParentObject.id != parentObject.id:
            # Out of the old and into the new            
            parentObject.RemoveChildByID(object.id, noParentIsOk = True)
            newParentObject.AddChildByID(object.id)            

        ### Finally update the pos of the object
        object.pos = newPos
        return True

    ##############################################################
    def AddObjectToUniverse(self, object):
        self.LogMe("AddObjectToUniverse: Attempting to add object = " + str(object))
        # Validate objects
        if object.IsValid() is False:
            self.Boom("AddObjectToUniverse: Object is not valid, id=" + str(object.id))
            return
        
        # We must register the object with the universe first.
        # Some of the following actions may make reference to it
        # via the GetObjectByID
        object.universe = self
        self.objects[object.id] = object
        
        # Must be a gob.  Gobs can live in two places
        # - Inside another gob
        # - In space    
        if isinstance(object, GOB):        
            if object.parentID is not None:
                # I live at my parents place
                parentObject = self.GetObjectByID(object.parentID)
                if parentObject is False:
                    self.Boom("AddObjectToUniverse: Parent object can not be found")
                    return False
                    
                # Add it in
                parentObject.AddChildByID(object.id)
                self.LogMe("AddObjectToUniverse: Add to parent")

            elif object.pos is not None:
                # I live in space
                locationObject = self.GetLocationOrCreate(object.pos)
                locationObject.AddChildByID(object.id)
                self.LogMe("AddObjectToUniverse: Add to location")
            else:                
                self.Boom("AddObjectToUniverse:  GOB has neither a parentID or pos, id=" + str(object.id))
                return False

        self.LogMe("AddObjectToUniverse: Object added, details = " + str(object))
    
    ##############################################################
    def LoadObjectToUniverse(self, object):
        '''Ensures that an object is loaded into the unviverse correctly - differs from AddObjectToUniverse'''
        self.LogMe("LoadObjectToUniverse: Attempting to add object = " + str(object))
        # Validate objects
        if object.IsValid() is False:
            self.Boom("LoadObjectToUniverse: Object is not valid, id=" + str(object.id))
            return        
       
        object.universe = self
        self.objects[object.id] = object

    ##############################################################
    def GetLocationOrCreate(self, posOfObject):
        '''Returns a valid location, will create a location if needed'''
        targetLocID, targetLocPos = Location.PointToLocationLabel(self, posOfObject)        
        locationObject = self.GetObjectByID(targetLocID)
        
        # Failed to find, so we need to make
        if locationObject is False:
            locationObject = self.MillNewObject('Objects.Location.Location')
            locationObject.SetUp(targetLocPos)
            self.AddObjectToUniverse(locationObject)
            
        return locationObject
        
    ##############################################################
    def RemoveObjectFromUniverseByID(self, objectID):
        '''This will remove / destroy the objects and its childern'''

        # Can we resolve child objects
        childObject = self.GetObjectByID(objectID)
        if childObject is False:
            self.Boom("RemoveObjectFromUniverseByID: Failed to resolve child object")

        # Time to trigger a recusive detruction
        listOfIDs = childObject.GetAllIDsRecursive()
        if listOfIDs is False:
            self.Boom("RemoveObjectFromUniverseByID: Failed to get valid list of ids to remove")
            return False
        
        # Time to work through the list, but in reverse
        listOfIDs = listOfIDs[::-1]
        
        # Before we start we want to make sure we can resolve all of the objects
        objectsToDestroy = []
        for objectID in listOfIDs:
            object = self.GetObjectByID(objectID)
            if object is False:
                self.Boom("RemoveObjectFromUniverseByID: 1")
                return False
            
            # Else all good
            objectsToDestroy.append(object)
        
        # Loop and Kill, loop and Kill    
        for object in objectsToDestroy:
            outcome = object.SelfDestuct()
            if outcome is False: 
                self.Boom("RemoveObjectFromUniverseByID: 2")
                return False

            #else, the universe can forget about it
            del self.objects[object.id]
        return True


        
