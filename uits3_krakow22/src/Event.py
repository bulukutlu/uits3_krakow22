class Event:
    def __init__(self):
        self.timestamp = 0
        self.clusters = []
    
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