import numpy as np
from time import time
from video_to_audio import Synths

#Parameters
width = 640//4#1280#
height = 480//4#720#
timespan = .5
margin = 0
video = 0#np.inf
frame_rate = 30 if video else 18
ticks_per_frame = 3
frames_per_audio = 3
depth = int(timespan*frame_rate)#int(np.log(255)*timespan)
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
    
tt = [0]*6
class HistoryWorld:
    def __init__(self, shape, depth):
        self.future = np.full(shape, -2, np.uint16)
        self.past = np.full(shape, depth, np.uint32)
        self.worlds = np.zeros((depth,)+shape, np.uint8)
        self.depth = depth
#        self.ones = np.ones((1,)+shape)
        
    def tick(self, light, count=1):
        tt[0] -= time()
        #Update worlds
        tick(self.worlds[-1], light, self.worlds[0])#7.5%
        for i in range(count-1):
            tick(self.worlds[0], light)
        tt[0] += time()
        tt[1] -= time()        
        self.worlds = np.roll(self.worlds, -1, axis=0)#4% \/
        #Increment counters since life last departed
        self.past += 1
        #...and reset where life is now
        self.past[self.worlds[0]==1] = 0

        #Decrement counters till the next life arives (if life has been spotted)
        self.future[self.future+2 != 0] -= 1
        self.future[(self.future+2 == 0) & (self.worlds[-1] == 1)] = depth-1
        #...and re-spot once last spotting has departed
        respot = self.future+1 == 0#4% /\
        #This is amortized O((proporiton of liveness)(depth)(board_size)). Slow.
        #53%
#        self.future[respot] = np.argmax(
#            np.concatenate((self.worlds,self.ones)).transpose(1,2,0)[respot],1)

        tt[1] += time()
        tt[2] -= time()        
        self.future[respot]=np.argmax((self.worlds).transpose(1,2,0)[respot],axis=1)
        self.future[(self.future == 0) & (self.worlds[0] == 0)] = -2

        #print(self.future, self.past, self.worlds[0])
        #print('\n')

        tt[2] += time()
        tt[3] -= time()     
        out = (np.minimum(self.future, self.depth).astype(np.int16)
                -np.minimum(self.past, self.depth))/self.depth
        tt[3] += time()
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
a = Synths(synth_count=40, gain=-100)

world = HistoryWorld((height+margin*2, width+margin*2), depth)
sim_time = 0
slc = slice(margin, -margin) if margin else slice(None)
keep_going = True
try:
    while keep_going:
        diff = world.worlds[2].astype(np.float16)-world.worlds[1]*2+world.worlds[0]
        audio_frame = diff*300-30
        a.set_by_frame(audio_frame, func = lambda val,freq:val+freq/100)
        
        for i in range(frames_per_audio):
            frame = world.tick(cadence(sim_time), ticks_per_frame)[slc, slc]
            video_frame = np.dstack(((frame+1)*127,)*3)
            if not (w.write(video_frame) == -1 or (video and sim_time < video)):
                keep_going = False
                break
            
            sim_time += 1/frame_rate/ticks_per_frame
            if video and time() > t0 + next_print:
                t = time()-t0
                next_print += last_print
                last_print = next_print-last_print
                print('Time: {:2.0f}s, Sim_Time: {:3.1f}s, Progress: {:2.0f}%, Speed: {:.2f}'
                      .format(t, sim_time, sim_time/video*100, sim_time/t))
                print(['{:.1f}%'.format(ttt/t*100) for ttt in tt])
        
finally:
    print([s.get('gain') for s in a.synths])
    print(np.log(np.sum(np.exp(np.array([s.get('gain') for s in a.synths])))))
    a.release()
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

