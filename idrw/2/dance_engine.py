import tkinter as tk
import random as r
import time
from math import *
import db

px = 300
c = tk.Canvas(width=2*px, height=2*px)
c.pack()

def scale(pos):
    return 1-pos[0]**2-pos[1]**2

def init():
    c.create_oval(0,0,2*px,2*px)
    db.record('init', locals())
    return (0,0,0,0), c.create_oval(0,0,2*px,2*px)

def tick(world):
    x, y, dx, dy = world
    dx += r.gauss(0,.1)
    dy += r.gauss(0,.1)
    rescale = scale((x,y))/hypot(dx,dy)
    dx *= rescale
    dy *= rescale
    x = (x+dx*.03)*.9999
    y = (y+dy*.03)*.9999
    db.record('tick', locals())
    return x, y, dx, dy

def render(world, graphics):
    x, y, dx, dy = world
    size = scale((x,y))*.3
    c.coords(graphics, px+px*(x-size), px+px*(y-size), px+px*(x+size), px+px*(y+size))
    db.record('render', locals())
    
world, graphics = init()
while True:
    world = tick(world)
    render(world, graphics)
    c.update()
    db.record('loop', locals())
    #time.sleep(.01)
