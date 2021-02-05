import tkinter as tk
from math import *

class Para:
    def __init__(self, dct={}):
        self.__dict__.update(dct)
g = Para()
g.size=700
g.sigma = 1

c = tk.Canvas(width=g.size, height=g.size, highlightthickness=0)
c.pack()

def pos_to_pix(x,y):
    r = hypot(x,y)
    if r == 0:
        return g.size/2, g.size/2
    ratio = g.size/2*(1-exp(-r/g.sigma))/r
    return g.size/2+x*ratio, g.size/2-y*ratio

def plot_poly(x,y,r,pts,offset=0,**kwargs):
    c.create_polygon(sum(
        (list(pos_to_pix(x+r*cos(2*pi*(t+offset)/pts),
                         y+r*sin(2*pi*(t+offset)/pts)))
        for t in range(pts)), start=[]), **kwargs)

def texture():
    k = .5
    s = .2
    n = 100
    for x in range(-n, n):
        for y in range(-n, n):
            plot_poly(x*k,y*k,s,8,fill="",outline="#997")

def light():
    k = .1
    n = 100
    for x in range(-n, n):
        x *= k
        for y in range(-n, n):
            y *= k
            light = exp(-(hypot(x,y)/g.sigma)**2) if (x or y) else 1
            #print(x,y,light)
            plot_poly(x,y,k/2,4,.5,
                      fill='#{0:02x}{0:02x}{0:02x}'.format(int(light*255)))


c.create_rectangle(0,0,g.size,g.size,fill='black')
light()
#texture()
tk.mainloop()