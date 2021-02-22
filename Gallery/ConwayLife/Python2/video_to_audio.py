'''
To use this, first:
1) Open supercollider
2) Type:
SynthDef(\sine, { |out = 0, freq = 440.0, gain = 0.0|
    Out.ar(out, SinOsc.ar(freq) * gain.dbamp);
}).store;
3) select it and command + enter
4) command + b (boot server)
'''

from supercollider import Server, Synth
from math import log10, hypot
import numpy as np

class Synths:
    def __init__(self, synth_count = 20, gain = -18):
        server = Server()
        self.synths = []
        self.shape = None
        for f in range(synth_count):
            freq = 150*(1000/150)**(f/(synth_count-1))
            synth_gain = gain - 10*log10(synth_count)
            self.synths.append(Synth(server, 'sine',
                                     {'freq': freq, 'gain': synth_gain}))

    def set_gains(self, gains):
        try:
            for synth, gain in zip(self.synths, gains):
                synth.set('gain', gain-10*log10(len(self.synths)))
        except TypeError:
            for synth in self.synths:
                synth.set('gain', gain-10*log10(len(self.synths)))

    def release(self):
        for synth in self.synths:
            synth.free()    

    def set_regions(self, shape):
        self.shape = shape
        x = (np.zeros(shape[::-1])+np.arange(-shape[0]/2,shape[0]/2)).T
        y = np.zeros(shape)+np.arange(-shape[1]/2,shape[1]/2)
        r2 = (x**2+y**2)
        k = (shape[0]**2+shape[1]**2)/4/(len(self.synths))
        self.regions = [np.where((i*k<=r2) & (r2<(i+1)*k))
                        for i in range(len(self.synths))]

    def set_by_frame(self, frame):
        if frame.shape != self.shape:
            self.set_regions(frame.shape)
        self.set_gains([np.average(frame[region]) for region in self.regions])

if __name__ == '__main__':
    s = Synths(gain=-18)
