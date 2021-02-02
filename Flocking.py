from math import sqrt
from random import random

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __abs__(self):
        return sqrt(self.x*self.x+self.y*self.y)
    def __invert__(self):
        return self/abs(self)

    def __add__(self, other):
        return Vector(self.x+other.x, self.y+other.y)
    def __sub__(self, other):
        return Vector(self.x-other.x, self.y-other.y)
    def __mul__(self, other):
        return Vector(self.x*other, self.y*other)
    def __rmul__(self, other):
        return self*other
    def __truediv__(self, other):
        return Vector(self.x/other, self.y/other)

class Obsticle:
    def __init__(self, pos):
        self.pos = pos

class Bird:
    def __init__(self, pos, vel):
        self.pos, self.vel = pos, vel

    def tick(self, neighbors, obsticles, distance, a, b, c):
        vel = Vector(0, 0)
        if neighbors:
            for n in neighbors:
                vel += n.pos-self.pos#Clustering
            vel = a*~vel
            for n in neighbors:
                vel += b*n.vel/len(neighbors)#Allignment
        for o in neighbors+obsticles:
            vel -= c*~(o.pos-self.pos)/abs(o.pos-self.pos)#Collision avoidence
        if abs(vel) > 0:
            self.vel = ~vel#Constant speed
        self.pos += self.vel*distance#Position adjustment
        
class Flock:
    def __init__(self, width, height, sightRange, birdcount=100, a=1, b=1, c=1):
        self.birds = []
        for i in range(birdcount):
            self.birds.append(Bird(Vector(width*random(), height*random()),
                ~Vector(random(), random())))
        self.width, self.height, self.sightRange = width, height, sightRange
        self.a, self.b, self.c = a, b, c

    def __iter__(self):
        return iter(self.birds)

    def tick(self, distance):
        for b in self.birds:
            neighbors = []#Find neighbors (BOTTLENECK: O(n^2) per tick)
            for o in self.birds:
                if 0 < abs(o.pos-b.pos) <= self.sightRange:
                    neighbors.append(o)
                    
            obsticles = []#Find obsticles
            for pos in [Vector(b.pos.x, 0), Vector(b.pos.x, self.height),
                        Vector(0, b.pos.y), Vector(self.width, b.pos.y)]:
                if 0 < abs(pos-b.pos) <= self.sightRange:
                    obsticles.append(Obsticle(pos))

            b.tick(neighbors, obsticles, distance, self.a, self.b, self.c)
