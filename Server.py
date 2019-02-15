import Config
from Core.Base import Base
from Universe import Universe
from Core.Point import Point

from Objects.Object import Object

import datetime
import time

class Server(Base):
    ##############################################################    
    def __init__(self):
        Base.__init__(self)
        self.loggingPrefix = "Server"

        self.universe = False
        
    ##############################################################    
    def Boot(self):
        self.LogMe("** Server booting")
        self.universe = Universe()
        # self.universe.LoadFromDisk()
        self.LogMe("** Server booted")        
        
        clean = False
        
        if clean is False:
            self.universe.LoadFromDisk()
        else:
            TO1 = self.MillNewObject('Objects.GOB.GOB')        
            TO1.id = self.universe.AllocateObjectID()
            TO1.pos = Point(0, 0, 0)        
            self.universe.AddObjectToUniverse(TO1)            
        ###### End Temp
        
    ##############################################################
    def Run(self):
        
        while(1):
            # Snap Shot of Time
            StartTime = datetime.datetime.now()

            self.universe.Tick()

            # so sleepy
            EndTime = datetime.datetime.now()
            TimeDiff = EndTime - StartTime
            TimeDiffMS = TimeDiff.microseconds / 1000
            SleepTimeMS = Config.ServerFrameMS - TimeDiffMS
            if (SleepTimeMS < 0):
                SleepTimeMS = 0
            SleepTimeSec = SleepTimeMS / 1000.0
            time.sleep(SleepTimeSec)