import tkinter as tk
from math import *
from heapq import heappush, heappop
import random
import time

class Para:
    def __init__(self, dct={}):
        self.__dict__.update(dct)
g = Para()
g.size=700
g.sigma = 1
g.eat_efficiency = .5
g.dt = .5

c = tk.Canvas(width=g.size, height=g.size, highlightthickness=0)
c.pack()

def pos_to_pix(x,y):
    r = hypot(x,y)
    if r == 0:
        return g.size/2, g.size/2
    ratio = g.size/2*(1-exp(-r/g.sigma))/r
    return g.size/2+x*ratio, g.size/2-y*ratio

def light_at(x,y):
    return exp(-(x*x+y*y)/g.sigma**2)

def plot_poly(x,y,r,pts,offset=0,**kwargs):
    c.create_polygon(sum(
        (list(pos_to_pix(x+r*cos(2*pi*(t+offset)/pts),
                         y+r*sin(2*pi*(t+offset)/pts)))
        for t in range(pts)), start=[]), **kwargs)
    
def draw_light():
    global a
    global b
    k = .14
    n = 30
    for x in range(-n, n):
        x *= k
        for y in range(-n, n):
            y *= k
            light = int(light_at(x,y)*255) if (x or y) else 255
            if light:
                plot_poly(x,y,k/sqrt(2)+.01,4,.5,
                          fill='#{0:02x}{0:02x}{0:02x}'.format(light))


c.create_rectangle(0,0,g.size,g.size,fill='black')
draw_light()

class Entity:
    def __init__(self,x,y,size):
        self.x = x
        self.y = y
        self.size = size
def draw_entity(e):
    plot_poly(e.x, e.y, e.size, 10, fill='#1f1')

entities = []
while True:
    entities.append(Entity(random.gauss(0,1), random.gauss(0,1),.01))
    for e in entities:#Growth
        light = light_at(e.x, e.y)
        size = e.size
        e.size += g.dt*size*(light-size)
    for e in entities:
        for f in entities:
            if e is not f and e.size <= f.size and \
               hypot(e.x-f.x, e.y-f.y) < e.size+f.size:
                e.size = e.size+.5*f.size
                f.size = 0
    entities = [e for e in entities if e.size > 0]
   
    draw_light()
    for e in entities:
        draw_entity(e)

    c.update()
    time.sleep(g.dt)
    
print("Complete")
