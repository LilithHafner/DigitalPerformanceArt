import tkinter as tk
import random as r
import time
from math import *
import db

px = 300
c = tk.Canvas(width=2*px+1, height=2*px+1)
def topx(x):
    return px+x*px+3
c.pack()

def scale(pos):
    return 1-pos[0]**2-pos[1]**2

def init():
    db.record('init', locals())
    coords = topx(-1),topx(-1),topx(1),topx(1)
    return [(0,0,cos(2*pi*i/3),sin(2*pi*i/3),.001*i) for i in [-1,0,1]], \
        (c.create_oval(*coords), [c.create_oval(*coords, outline='') for i in range(3)])

def tick(world):
    new_world = []
    for entity in world:
        x, y, dx, dy, de = entity
        speed0 = hypot(dx,dy)/scale((x,y))
        x = (x+dx*.03)*.9999
        y = (y+dy*.03)*.9999
        dist = hypot(x, y)
        if dist > .9999:
            x *= .9999/dist
            y *= .9999/dist
        dx += r.gauss(0, scale((x,y))*.1)
        dy += r.gauss(0, scale((x,y))*.1)
        speed1 = hypot(dx,dy)/scale((x,y))
        rescale = (max(speed0**2/2+de, 0)/(speed1**2/2))**.5
        dx *= rescale
        dy *= rescale
        for other in world:
            if other != entity:
                diff = other[0]-x, other[1]-y
                dist = hypot(*diff)*(1/scale((x,y))+1/scale(other[:2]))
                force = (dist-1)*.01
                vdiff = other[2]-dx, other[3]-dy
                speed = hypot(*vdiff)*(1/scale((x,y))+1/scale(other[:2]))
                force += speed*.001
                dx += force*diff[0]/dist
                dy += force*diff[1]/dist
        new_world.append((x,y,dx,dy,de))
    db.record('tick', locals())
    return new_world

def color(args):
    return'#%02x%02x%02x'%tuple(int(max(0,min(1,a))*255) for a in args)
def norm(x, xs):
    return (x-min(xs))/(max(xs)-min(xs))

def render(world, graphics, recolor=lambda x:x):
    radial = [(x*dx+y*dy)/hypot(x,y)/scale((x,y)) for x, y, dx, dy, _ in world]
    rotary = [(y*dx-x*dy)/hypot(x,y)/scale((x,y)) for x, y, dx, dy, _ in world]
    des = [i for x, y, dx, dy, i in world]
    for entity, sprite, rad, rot in zip(world, graphics[1], radial, rotary):
        x, y, dx, dy, de = entity
        size = scale((x,y))*.3
        c.coords(sprite, topx(x-size), topx(y-size), topx(x+size), topx(y+size))
        c.itemconfig(sprite, fill=color([recolor(norm(x, xs)) for x, xs in \
                                          [(rad, radial), (rot, rotary), (de, des)]]))
    energy = sum((rot**2+rad**2)/2 for rot, rad in zip(rotary, radial))
    energy_color = 1-.01*energy
    c.itemconfig(graphics[0], fill=color(3*[recolor(energy_color)]))
    c.configure(bg = color(3*[recolor(1)]))
    db.record('render', locals())
    if energy_color < -10:
        raise StopIteration

def end(world, graphics):
    render(world, graphics, recolor=lambda x:1-x)
    
world, graphics = init()
while True:
    try:
        world = tick(world)
        render(world, graphics)
        c.update()
        db.record('loop', locals())
        #time.sleep(.01)
    except StopIteration:
        try:
            end(world, graphics)
        except StopIteration:
            time.sleep(.1)
        break

