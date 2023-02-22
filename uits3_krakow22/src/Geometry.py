import math
import random

class ALPIDE:
    def __init__(self,position=None,rotation=None,radius=None):
        if position : self.position = position
        else : self.position = [0,0,0]

        if rotation : self.rotation = rotation
        else : self.rotation = [0,0,0]

        if radius : self.radius = position
        else : self.position = [0,0,0]

class Fiber:
    def __init__(self,center=[0,0,0],radius=1,height=10):
        self.center = center
        self.radius = radius
        self.height = height
    
    def getRandomPoint(self):
        R = random.random()*self.radius
        Y = (random.random()-0.5)*self.height
        theta = random.random()*2*math.pi
        coordinate = [self.center[0]+R*math.cos(theta),self.center[1]+Y,self.center[2]+R*math.sin(theta)]
        return coordinate