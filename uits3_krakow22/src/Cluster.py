import ROOT
import math
ROOT.gSystem.Load("$CORRYVRECKAN_DIR/lib/libCorryvreckanObjects.so")

getGlobal = """
std::vector<double> getGlobal(corryvreckan::Cluster* cluster) {
    double x,y,z;
    cluster->global().GetCoordinates(x,y,z);
    std::vector<double> out{x,y,z};
    return out;
}
"""
ROOT.gInterpreter.ProcessLine(getGlobal)

getLocal = """
std::vector<double> getLocal(corryvreckan::Cluster* cluster) {
    double x,y,z;
    cluster->local().GetCoordinates(x,y,z);
    std::vector<double> out{x,y,z};
    return out;
}
"""
ROOT.gInterpreter.ProcessLine(getLocal)

class Cluster:
    def __init__(self,detector=None,size=None,col=None,row=None,charge=None,localPos=None,globalPos=None,split=None,colWidth=None,rowWidth=None):
        if detector : self.detector = detector
        else : self.detector = 0

        if size : self.size = size
        else : self.size = 0
        
        if col : self.col = col
        else : self.col = 0
        
        if row : self.row = row
        else : self.row = 0
        
        if charge : self.charge = charge
        else : self.charge = 0
        
        if localPos : self.localPos = localPos
        else : self.localPos = [0,0,0]
        
        if globalPos : self.globalPos = globalPos
        else : self.globalPos = [0,0,0]
        
        if split : self.split = split
        else : self.split = False
        
        if colWidth : self.colWidth = colWidth
        else : self.colWidth = 0
        
        if rowWidth : self.rowWidth = rowWidth
        else : self.rowWidth = 0
    
    def setData(self,corryCluster):
        self.detector = corryCluster.getDetectorID()
        self.size = corryCluster.size()
        self.col = corryCluster.column()
        self.row = corryCluster.row()
        self.charge = corryCluster.charge()
        self.localPos = ROOT.getLocal(corryCluster)
        self.globalPos = ROOT.getGlobal(corryCluster)
        self.split = corryCluster.isSplit()
        self.colWidth = corryCluster.columnWidth()
        self.rowWidth = corryCluster.rowWidth()

    def setPositionGlobal(self,globalPos,isSim=True):
        # For creating clusters at target global position
        # Mainly used in simulation where the global position of track is known and the local position of clusters are wanted
        def arm(phi):
            if abs(phi) < math.pi/2:
                return "Right"
            else:
                return "Left"

        def phiRange(radius):
            widthRad = 30/radius #ALPIDE is 30 mm wide
            if arm(phi) == "Right":
                out = [-widthRad/2,widthRad/2]
            else:
                out = [-widthRad/2 +math.pi,widthRad/2+math.pi]
            return out

        def getDetector(radius, arm):
            detector = ""
            if arm == "Left":
                if radius == 30:
                    detector = "ALPIDE_4"
                elif radius == 18:
                    detector = "ALPIDE_3"
            elif arm == "Right":
                if radius == 30:
                    detector = "ALPIDE_0"
                elif radius == 24:
                    detector = "ALPIDE_1"
                elif radius == 18:
                    detector = "ALPIDE_2"
            return detector

        zRange = {
            18 : [0 - 7.5, 0 + 7.5],
            24 : [6.25 - 7.5, 6.25 + 7.5],
            30 : [12.5 - 7.5, 12.5 + 7.5]
        }

        self.globalPos = globalPos
        
        R = math.sqrt(globalPos[0]**2+globalPos[1]**2)
        phi = math.atan2(globalPos[1],globalPos[0])
        Z = globalPos[2]

        if isSim:
            self.detector = getDetector(round(R),arm(phi))

        globalCylinderical = [R,phi,Z]
        allowedPhiRange = phiRange(round(R))
        allowedZRange = zRange.get(round(R))
        
        localX = 0
        if arm(phi) == "Right":
            localX = -1*phi*round(R)
        else:
            localX = math.copysign((abs(phi)-math.pi)*round(R),phi)

        localY = (allowedZRange[1]-7.5)-Z
        localPos = [localX,localY,0]
        self.localPos = localPos

    
    def isClusterIn(self):
        if (-15 < self.localPos[0] < 15) and (-7.5 < self.localPos[1] < 7.5):
            return True
        else :
            return False

    def alignLocal(self, localDisplacement):

        globalPosUpdated = [0,0,0]
        R = math.sqrt(self.globalPos[0]**2+self.globalPos[1]**2)

        self.localPos[0] += localDisplacement[0]
        self.localPos[1] += localDisplacement[1]

        globalPosUpdated[0]=  R*math.cos((self.localPos[0])/(R)) #global x
        globalPosUpdated[1]= -R*math.sin((self.localPos[0])/(R)) #global y
        globalPosUpdated[2]=  self.globalPos[2] - localDisplacement[1]  #global z

        if self.detector in ["ALPIDE_0","ALPIDE_1","ALPIDE_2"]:
            globalPosUpdated[0] *= -1
            globalPosUpdated[1] *= -1

        self.globalPos = globalPosUpdated

        return self

    def alignGlobal(self, globalDisplacement):  
        globalPosUpdated = self.globalPos
        globalPosUpdated[0] += globalDisplacement[0]
        globalPosUpdated[1] += globalDisplacement[1]
        globalPosUpdated[2] += globalDisplacement[2]
        
        self.globalPos = globalPosUpdated
        return self

    def flipYaxis(self):
        globalPosUpdated = [0,0,0]
        R = math.sqrt(self.globalPos[0]**2+self.globalPos[1]**2)

        self.localPos[1] = -self.localPos[1] 

        globalPosUpdated[0]=  R*math.cos((self.localPos[0])/(R)) #global x
        globalPosUpdated[1]= -R*math.sin((self.localPos[0])/(R)) #global y
        globalPosUpdated[2]=  self.globalPos[2] + 2*self.localPos[1]  #global z

        if self.detector in ["ALPIDE_0","ALPIDE_1","ALPIDE_2"]:
            globalPosUpdated[0] *= -1
            globalPosUpdated[1] *= -1

        self.globalPos = globalPosUpdated

        return self
    #def getPositio
    #def applyCorrection(self,geometry):


        #self.localPos = [self.localPos[0]-localCorrection[0],self.localPos[1]-localCorrection[1],0]
        # to do calculate new global positions