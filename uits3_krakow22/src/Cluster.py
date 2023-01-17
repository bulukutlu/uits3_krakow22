import ROOT
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
    def __init__(self):
        self.detector = 0
        self.size = 0
        self.col = 0
        self.row = 0
        self.charge = 0
        self.localPos = [0,0]
        self.globalPos = [0,0,0]
        self.split = False
        self.colWidth = 0
        self.rowWidth = 0
    
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
