from Core.Base import Base

class Point(Base):
    ##############################################################    
    def __init__(self, x, y, z):
        Base.__init__(self)
        self.loggingPrefix = "Point"
        
        self.x = x
        self.y = y
        self.z = z
                
        # self.LogMe("booted")
    
    ##############################################################    
    def __str__(self):
        buffer =  "x:"  + str(self.x)
        buffer += " y:" + str(self.y)
        buffer += " z:" + str(self.z)
        return buffer
    
    ##############################################################    
    def __eq__(self, other):
        if self.x != other.x: return False
        if self.y != other.y: return False
        if self.z != other.z: return False
        return True