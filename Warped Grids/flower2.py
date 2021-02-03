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
    ratio = g.size/2*(exp(-r/g.sigma))/r
    return g.size/2+x*ratio, g.size/2-y*ratio

def grid():
    k = .1
    s = .02
    n = 100
    for x in range(-n, n):
        for y in range(-n, n):
            if x or y:
                c.create_polygon(
                    pos_to_pix(x*k-s,y*k-s)+
                    pos_to_pix(x*k-s,y*k+s)+
                    pos_to_pix(x*k+s,y*k+s)+
                    pos_to_pix(x*k+s,y*k-s))

grid()
