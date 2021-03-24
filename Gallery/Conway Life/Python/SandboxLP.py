from ConwayLife import *
from LEDWall import *
from math import exp, inf
from time import sleep

def run():
    m = 49
    w = Wall(m, m, 17)
    lp = LifePlus(m, m, 30)

    while True:
        w.root.update()
        lastwhite, nextwhite = lp.getstate()
        for x in range(m):
            for y in range(m):
                i = lp.present.i
                a = inf if lastwhite[x][y] == -1 else i-lastwhite[x][y]
                b = inf if nextwhite[x][y] == -1 else nextwhite[x][y]-i
                A, B = exp(-a/8)*.8, exp(-b/8)*.8
                if a == 0:
                    w.setcolor(x, y, 0, 0, 0)
                else:
                    w.setcolor(x, y, max(B-A*1, 0), 0, max(A-B*1, 0))
run()
