import numpy as np
from time import time

#Parameters
timespan = 4
depth = int(np.log(255)*timespan)
width = 1280#640
height = 720#480
margin = 0
video = 0#np.inf
frame_rate = 30 if video else 18
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

def tick(world, light, out=None):
    slices = slice(2, None), slice(1,-1), slice(None, -2)
    self = world[slices[1],slices[1]]
    neighbors = np.zeros(self.shape)
    for x in slices:
        for y in slices:
            neighbors += world[x,y]

    if out is None:
        out = world
    out[slices[1],slices[1]] = (
        neighbors == 3) | ((self == 1) & (neighbors == 4))
    
    out[boarder(world.shape)] = \
        np.random.rand(len(boarder(world.shape)[0])) < light
    
respot_time = 0
class HistoryWorld:
    def __init__(self, shape, depth):
        self.future = np.full(shape, depth, np.uint16)
        self.past = np.full(shape, depth, np.uint32)
        self.worlds = np.zeros((depth,)+shape, np.uint8)
        self.depth = depth
        self.ones = np.ones((1,)+shape)
        
    def tick(self, light):
        #Update worlds
        global respot_time
        respot_time -= time()
        tick(self.worlds[-1], light, self.worlds[0])#7.5%
        self.worlds = np.roll(self.worlds, -1, axis=0)#4% \/
        
        #Increment counters since life last departed
        self.past += 1
        #...and reset where life is now
        self.past[self.worlds[0]==1] = 0

        #Decrement counters till the next life arives (if life has been spotted)
        self.future[(self.future != self.depth) | (self.worlds[-1] == 1)] -= 1
        #...and re-spot once last spotting has departed
        respot = self.future == -1#4% /\
        #This is amortized O((proporiton of liveness)(depth)(board_size)). Slow.
        #53%
        #self.future[respot] = np.argmax(
        #    np.concatenate((self.worlds,self.ones)).transpose(1,2,0)[respot],1)

        out = np.exp(-(self.future/timespan)) - np.exp(-(self.past/timespan))
        
        respot_time += time()
        return out
        
if video:
    from VideoWriter import Writer
    from time import time
    t0 = time()
    last_print = 1
    next_print = 1
else:
    from ScreenDisplay import Writer
w = Writer('Conway Life', frame_rate = frame_rate)

t0 = time()
world = HistoryWorld((height+margin*2, width+margin*2), depth)
sim_time = 0
slc = slice(margin, -margin) if margin else slice(None)
try:
    while w.write(np.dstack(((world.tick(cadence(sim_time))[slc, slc]+1)* \
        np.exp(1/timespan)*127,)*3)) == -1 or (video and sim_time < video):
        if np.random.random() < .1:
            print(time()-t0, respot_time, respot_time/(time()-t0))
        for _ in range(ticks_per_frame-1):
            sim_time += 1/frame_rate/ticks_per_frame
            tick(world, cadence(sim_time))
        if video and time() > t0 + next_print:
            t = time()-t0
            next_print += last_print
            last_print = next_print-last_print
            print('Time: {:2.0f}s, Sim_Time: {:3.1f}s, Progress: {:2.0f}%, Speed: {:.2f}'
                  .format(t, sim_time, sim_time/video*100, sim_time/t))
finally:
    w.release()


##world = np.zeros((height+margin*2, width+margin*2), np.uint8)
##sim_time = 0
##slc = slice(margin, -margin) if margin else slice(None)
##try:
##    while w.write(np.dstack((world[slc, slc]*255,)*3)) == -1 \
##          or (video and sim_time < video):
##        for _ in range(ticks_per_frame):
##            sim_time += 1/frame_rate/ticks_per_frame
##            tick(world, cadence(sim_time))
##        if video and time() > t0 + next_print:
##            t = time()-t0
##            next_print += last_print
##            last_print = next_print-last_print
##            print('Time: {:2.0f}s, Sim_Time: {:3.1f}s, Progress: {:2.0f}%, Speed: {:.2f}'
##                  .format(t, sim_time, sim_time/video*100, sim_time/t))
##finally:
##    w.release()
##
