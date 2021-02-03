from Flocking import *
import tkinter as tk
frame = tk.Tk()
width, height, buttonHeight = 1440-20, 900-55, 50

sliders = []
vals = [500, 500, 500]
for i in range(len(vals)):
    sliders.append(tk.Scale(frame, from_=1000,to=0, length=height-buttonHeight))
    sliders[i].set(vals[i])
    sliders[i].grid(row=0, column=i)
    width -= 49

def restart():
    global flock
    flock = Flock(width, height, 40)
    
button = tk.Button(frame, text='Restart', command=restart)
button.grid(row=1, column=0, columnspan=len(sliders))
canvas = tk.Canvas(master = frame, width=width, height=height)
canvas.grid(row=0, column=5, rowspan=2)

def tick(distance, n):
    flock.sightRange = (sliders[0].get()/1000)**4*min(width,height)
    flock.a = 10**(500/250)
    flock.b = 10*10**(sliders[1].get()/350)
    flock.c = 30*10**(sliders[2].get()/250)
    
    for i in range(n):
        flock.tick(distance/n)
    canvas.delete(tk.ALL)
    for bird in flock:
        x, y = int(bird.pos.x), int(bird.pos.y)
        canvas.create_oval(x-4, y-4, x+4, y+4)
    frame.update()
    
restart()
while True:
    tick(2, 1)
