from skspatial.objects import Line

class Track:
    def __init__(self,point=None,vector=None,line=None):
        if point : self.point = point
        else : self.point = [0,0,0]

        if vector : self.vector = vector
        else : self.vector = [1,0,0]

        if line : self.line = line
        else : self.line = Line(point=self.point, direction=self.vector)
    
    def fromClusters(self,clusters):
        if len(clusters) > 1:
            clusterPositions = [cluster.globalpos for cluster in clusters]
            line = Line.best_fit(clusterPositions)
            self.line = line
            self.point = line.point
            self.vector = line.vector
        else:
            raise Exception("Not enough clusters to construct track: #clusters = "+len(clusters))