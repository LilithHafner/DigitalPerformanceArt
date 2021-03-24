from ScreenDisplay import Writer
import numpy as np

#Parameters
timespan = 16
depth = np.log(255)*timespan
width = 640
height = 480
margin = 0
frame_rate = 25
ticks_per_frame = 1
def cadence(t):
    return np.sin(t*np.pi*2/60/3)*.5+.5

#TODO: Spatily change light and laws of physics

boarders = {}
def boarder(shape):
    if shape not in boarders:
        sheet = np.zeros(shape)
        sheet[1:-1,1:-1] = 1
        out = np.where(sheet == 0)
        boarders[shape] = out
    return boarders[shape]

def tick(world, light):
    slices = slice(2, None), slice(1,-1), slice(None, -2)
    self = world[slices[1],slices[1]]
    neighbors = np.zeros(self.shape)
    for x in slices:
        for y in slices:
            neighbors += world[x,y]
    world[slices[1],slices[1]] = (
        neighbors == 4) | ((self == 0) & (neighbors == 2))
    
    world[boarder(world.shape)] = \
        np.random.rand(len(boarder(world.shape)[0])) < light

from ScreenDisplay import Writer
w = Writer('Conway Life', frame_rate = frame_rate)
world = np.zeros((height+margin*2, width+margin*2), np.uint8)
time = 0
slc = slice(margin, -margin) if margin else slice(None)
while w.write(world[slc, slc]*255) == -1:
    time += 1/frame_rate
    tick(world, cadence(time))
w.release()
