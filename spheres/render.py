from numpy import *
import builtins
from PIL import Image, ImageDraw
from cv2 import imshow, waitKey

def adjust_for_camera(spheres, x,y,z,pitch):
    out = []
    for zi,xi,yi,r,color in spheres:
        xi -= x
        yi -= y
        zi -= z
        r2 = hypot(yi, zi)
        t = arctan2(yi, zi)+pitch*pi/180
        out.append([r2*cos(t), xi, r2*sin(t), r, color])
    return out

def render(spheres, shape=(600,400), fov=150*pi/180, bg=None, n=10):
    from time import time
    '''A sphere is (z,x,y,r,color)
color is (r,g,b) or None for a white outline.'''

    out = zeros(shape+(3,)) if bg is None else bg.copy()
    shape = out.shape[:2] if bg is None else shape
    assert out.shape == shape+(3,)
    U = mgrid[0:1, 0:shape[0], 0:shape[1]].reshape((3,)+shape).astype(float32)
    U[0] = shape[0]/2/tan(fov/2)
    U[1] -= (shape[0]-1)/2
    U[2] -= (shape[1]-1)/2
    UoUU = U/sum(U*U,0)
    for z,x,y,r,color in sorted(spheres, reverse=True):
        if z < -r:
            continue
        V = array([z,x,y]).reshape((3,1,1))
        R = V-(sum(UoUU*V, 0)*U)
        r2 = sum(R*R, 0)
        o = r2 < r**2
        color = color if color is not None else (1,)*3
        if all(o):
            out[o] = (out[o]+color)/2
        else:
            out[o] = color

    return out

def show(img, name=''):
    imshow(name, img[:,::-1].transpose(1,0,2))
    
if __name__ == '__main__':
    for i in range(-100, 100):
        x = render([[100,i,40,50,None]])
        show(x, 'Sphere')
        if waitKey(10) != -1:
            break
