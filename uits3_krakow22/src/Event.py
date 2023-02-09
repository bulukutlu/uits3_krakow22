from uits3_krakow22.src.Vertex import Vertex

class Event:
    def __init__(self,timestamp = None,clusters = None,tracks = None,vertex = None,dca=None):
        if timestamp : self.timestamp = timestamp
        else : self.timestamp = 0
        
        if clusters : self.clusters = clusters
        else : self.clusters = []
        
        if tracks : self.tracks = tracks
        else : self.tracks = []

        if vertex : self.vertex = vertex
        else : self.vertex = []

        if dca : self.dca = dca
        else : self.dca = -1

    def clearData(self):
        for var in self:
            del var
    
    def setTimestamp(self,time):
        self.timestamp = time
    
    def addCluster(self,cluster):
        self.clusters.append(cluster)
    
    def getNClusters(self):
        return len(self.clusters)
    
    def selectDetector(self,detector):
        selectedClusters = []
        for cluster in self.clusters:
            if cluster.detector == detector:
                selectedClusters.append(cluster)
        return selectedClusters

    def addTrack(self,track):
        self.tracks.append(track)

    def calculateVertex(self):
        self.vertex = Vertex().fromTracks(self.tracks)