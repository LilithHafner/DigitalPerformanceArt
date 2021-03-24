from time import time
t_ = time()
from physics import fibaranged_spheres
from render import render, show, adjust_for_camera

def physics_to_render(spheres, colors):
    return [(z, x, y, r, color) for
            (([x,y,z],v,r,m), color) in zip(spheres, colors)]

t0 = time()-t_
x = fibaranged_spheres(10)
t1 = time()-t_
x = physics_to_render(x, [None]*10)
x = adjust_for_camera(x, 0,3,0,0)
t2 = time()-t_
x = render(x)
t3 = time()-t_
show(x)
t4 = time()-t_
