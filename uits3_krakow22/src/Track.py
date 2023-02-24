from skspatial.objects import Line,Vector

class Track:
    def __init__(self,point=None,vector=None,line=None, nClusters=None, rms=None):
        if point : self.point = point
        else : self.point = [0,0,0]

        if vector : self.vector = vector
        else : self.vector = [1,0,0]

        if line : self.line = line
        else : self.line = Line(point=self.point, direction=self.vector)

        if nClusters : self.nClusters = nClusters
        else : self.nClusters = 0

        if rms : self.rms = rms
        else : self.rms = 0
    
    def fromClusters(self,clusters):
        nClusters = len(clusters)
        if nClusters > 1:
            self.nClusters = nClusters
            clusterPositions = [cluster.globalPos for cluster in clusters]
            line = Line.best_fit(clusterPositions)
            self.line = line
            self.point = line.point
            self.vector = line.vector
            if self.vector[2] < 0: self.vector  = Vector([axis*-1 for axis in self.vector])

            rms = lambda self,clusters: (sum(self.line.distance_point(cluster.globalPos)**2 for cluster in clusters)/len(clusters))**(1/2)
            self.rms = rms(self,clusters)
        else:
            raise Exception("Not enough clusters to construct track: #clusters = "+len(clusters))

    def propagate2point(self,point):
        return self.line.project_point(point)