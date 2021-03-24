import tkinter as tk
import random as r
import time

scale = 300
c = tk.Canvas(width=2*scale, height=2*scale)
c.pack()

def init():
    return 1, c.create_oval(0,0,2*scale,2*scale)

def tick(world):
    return (world+(r.random()-.5)*.1)*.995+.001

def render(world, graphics):
    c.coords(graphics, scale-scale*world, scale-scale*world, scale+scale*world, scale+scale*world)
    
world, graphics = init()
while True:
    world = tick(world)
    render(world, graphics)
    c.update()
    #time.sleep(.01)
