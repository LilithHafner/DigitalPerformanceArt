import tkinter as tk
class Wall:
    def __init__(self, width, height, size=20, fill=.8, backgroundcolor=(0,0,0), startcolor=(.2,.2,.2), backlight=False):
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=(width+1-fill)*size, height=(height+1-fill)*size, highlightthickness=0)
        self.canvas.pack()
        self.offset = (1-fill)/2
        self.size, self.height, self.width, self.backlight = size, height, width, backlight
        self.ids = []
        self.canvas.create_rectangle(0,0,(width+1-fill)*size,(height+1-fill)*size,fill=self.color(*backgroundcolor),outline='')
        for x in range(width):
            self.ids.append([])
            for y in range(height):
                back = None
                if backlight:
                    back = self.canvas.create_rectangle(*self.coords(x,y,1), fill=self.color(*backgroundcolor),outline='')
                fore = self.canvas.create_rectangle(*self.coords(x,y,fill), fill=self.color(*startcolor),outline='')
                self.ids[-1].append((fore, back))

    def coords(self, x, y, fill):
        return (x+1/2-fill/2+self.offset)*self.size, (self.height-y-1/2-fill/2+self.offset)*self.size, (x+1/2+fill/2+self.offset)*self.size, (self.height-y-1/2+fill/2+self.offset)*self.size
    def color(self, red, green, blue):
        return '#'+hex((int(red*255)<<16) + (int(green*255)<<8) + (int(blue*255)))[2:].zfill(6)

    def setcolor(self, x, y, red, green, blue):
        self.canvas.itemconfig(self.ids[x][y][0], fill=self.color(red, green, blue))
    def setbackgroundcolor(self, x, y, red, green, blue):
        assert self.backlight
        self.canvas.itemconfig(self.ids[x][y][1], fill=self.color(red, green, blue))
