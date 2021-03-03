from numpy import *
from PIL import Image, ImageDraw
from cv2 import imshow, waitKey

def render(spheres, size=(600,400), fov=150*pi/180, bg=(0,0,0), n=100):
    '''A sphere is (z,x,y,r,color)
color is (r,g,b) or None for a white outline.'''
    out = Image.new('RGB', size, bg)
    draw = ImageDraw.Draw(out)

    sincoss = [(sin(2*pi*i/n), cos(2*pi*i/n)) for i in range(n)]
    for z,x,y,r,color in sorted(spheres, reverse=True):
        xt, yt = arctan2(x,z), arctan2(y,z)
        rt = arctan2(r, sqrt(x**2+y**2+z**2))
        scale = size[0]/tan(fov/2)
        pts = __builtins__.sum([[size[0]/2+scale*tan(xt+rt*cos),
                                 size[1]/2-scale*tan(yt+rt*sin)]
                                for sin, cos in sincoss],[])
        draw.polygon(pts, fill=color)
        

    return out

#x,d = render([[10,3,4,5,None]])
#x.show()

for i in range(-100, 100):
    x = render([[100,i,40,50,None]])
    imshow('Sphere', array(x))
    if waitKey(10) != -1:
        break
