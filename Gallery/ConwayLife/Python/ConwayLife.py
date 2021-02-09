import random
from collections import deque
from math import sin

class Life:
    def __init__(self, width, height):
        self.i = 0
        self.r = random.Random()
        self.state = list([False]*height for i in range(width))
        self.oldstate = list([False]*height for i in range(width))
    
    def result(state, neighbors):
        if state:
            return 3 <= neighbors <= 4
        return neighbors == 3

    def getstate(self):
        self.i += 1
        self.oldstate = list(map(list, self.state))
        for x in range(len(self.state)):
            for y in range(len(self.state[0])):
                neighbors = 0
                for xi in range(x-1, x+2, 1):
                    for yi in range(y-1, y+2, 1):
                        neighbors += self.oldstate[xi][yi] \
                                     if (0 <= xi < len(self.state) and 0 <= yi < len(self.state[0])) \
                                     else self.r.random() < sin(self.i/70)*.6+.34 
                self.state[x][y] = (self.oldstate[x][y] and neighbors == 4) or neighbors == 3
        return self.state

class LifePlus:
    '''keeps track of time since last white and time till next white'''
    def __init__(self, width, height, forsight):
        self.forsight = forsight
        self.present = Life(width, height)
        self.present.i = -forsight
        self.future = Life(width, height)
        self.future.r.setstate(self.present.r.getstate())
        self.lastwhite = list([-1]*height for i in range(width))
        self.nextwhite = list([-1]*height for i in range(width))
        self.futurewhitenings = list(list(deque() for j in range(height)) for i in range(width))

    def getstate(self):
        if self.present.i >= 0:
            present = self.present.getstate()
            for x in range(len(present)):
                for y in range(len(present[0])):
                    if present[x][y]:
                        self.lastwhite[x][y] = self.present.i
        else:
            self.present.i += 1
                        
        prefuture = list(map(list,self.future.state))
        future = self.future.getstate()
        for x in range(len(future)):
            for y in range(len(future[0])):
                if future[x][y] and not prefuture[x][y]:
                    self.futurewhitenings[x][y].append(self.future.i)
                        
        for x in range(len(self.nextwhite)):
            for y in range(len(self.nextwhite[0])):
                if self.futurewhitenings[x][y]:
                    self.nextwhite[x][y] = self.futurewhitenings[x][y][0]
                    if self.futurewhitenings[x][y][0] == self.present.i:
                        self.futurewhitenings[x][y].popleft()
                else:
                    self.nextwhite[x][y] = -1
                
        return self.lastwhite, self.nextwhite
        
