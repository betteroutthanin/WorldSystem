import Config


class Base(object):
    lastLogPrefix = ""
    quiteMode = False

    ##############################################################
    def __init__(self):
        self.loggingPrefix = "Base"
     
    ##############################################################    
    ###### Logging
    ##############################################################
    def LogMe(self, message):
        prefix = ""
        
        if (Base.lastLogPrefix == self.loggingPrefix):
            prefix =  " " * len(self.loggingPrefix)
        else:
            prefix = self.loggingPrefix
    
        Base.lastLogPrefix = self.loggingPrefix
        logMessage = "- " + prefix + ": " + str(message)
                
        if Base.quiteMode == False:            
            print(logMessage)
            
        if Config.LogToDisk:
            with open(Config.logPath, "a") as myfile:
                myfile.write(logMessage + "\n")
            
    ##############################################################
    def Boom(self, message):
        self.LogMe(message)
        self.LogMe("Boom: Application has quit - see comments above for insights")
        quit()
    
    ##############################################################
    ###### Object Creation
    ##############################################################
    def MillNewObject(self, type):
        self.LogMe("Attempting to Mill new object: " + type)
        m = self.GetClass(type)
        object = m()
        return object
        
    ##############################################################
    def GetClass(self, name):
        parts = name.split('.')
        module = ".".join(parts[:-1])
        m = __import__( module )
        for comp in parts[1:]:
            m = getattr(m, comp)
        return m