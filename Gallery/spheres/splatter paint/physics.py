from numpy import *

'''[([x,y,z], [xv,yv,zv], r, m)]'''
phi = (sqrt(5)+1)/2
def fibaranged_spheres(n, radius=1, mass=1, spacing=2, symetrical=False):
    theta = 2*pi/phi if symetrical else pi/phi
    rts = [(spacing*sqrt(i), theta*i) for i in range(n)]
    return [([r*cos(t), radius, r*sin(t)], [0]*3, radius, mass) for r,t in rts]

class World:
    def __init__(self, spheres, control_input):
        pass
