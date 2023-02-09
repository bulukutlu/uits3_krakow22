from skspatial.objects import Line

class Track:
    def __init__(self,point=None,vector=None,line=None, nClusters=None):
        if point : self.point = point
        else : self.point = [0,0,0]

        if vector : self.vector = vector
        else : self.vector = [1,0,0]

        if line : self.line = line
        else : self.line = Line(point=self.point, direction=self.vector)

        if nClusters : self.nClusters = nClusters
        else : self.nClusters = 0
    
    def fromClusters(self,clusters):
        nClusters = len(clusters)
        if nClusters > 1:
            self.nClusters = nClusters
            clusterPositions = [cluster.globalPos for cluster in clusters]
            line = Line.best_fit(clusterPositions)
            self.line = line
            self.point = line.point
            self.vector = line.vector
        else:
            raise Exception("Not enough clusters to construct track: #clusters = "+len(clusters))