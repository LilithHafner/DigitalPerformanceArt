import tkinter as tk
from math import *

class Para:
    def __init__(self, dct={}):
        self.__dict__.update(dct)
g = Para()
g.size=700
g.sigma = 1

c = tk.Canvas(width=g.size, height=g.size)
c.pack()

def pos_to_pix(x,y):
    r = hypot(x,y)
    if r == 0:
        return g.size/2, g.size/2
    ratio = g.size*exp(-r/g.sigma)/r
    return g.size/2+x*ratio, g.size/2-y*ratio

def grid():
    k = .1
    n = 100
    for x in range(-n, n):
        for y in range(-n, n):
            c.create_line(pos_to_pix(x*k,y*k)+pos_to_pix((x+1)*k,y*k))
            c.create_line(pos_to_pix(x*k,y*k)+pos_to_pix(x*k,(y+1)*k))

grid()
tk.mainloop()