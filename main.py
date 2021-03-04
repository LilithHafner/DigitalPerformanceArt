from physics import fibaranged_spheres
from render import render, show

def physics_to_render(spheres, colors):
    return [(z, x, y, r, color) for
            (([x,y,z],v,r,m), color) in zip(spheres, colors)]

show(render(physics_to_render(fibaranged_spheres(10), [None]*10)))
