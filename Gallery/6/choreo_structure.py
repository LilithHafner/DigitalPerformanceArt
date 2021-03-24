unique = True
#1 indexing!
from time import time
t00 = time()
print('Choreographing, please wait. This may take 5-15 minutes...')
t_import = -time()
import cv2
import numpy as np
from subprocess import check_output
from ScreenDisplay import Writer
import os
t_import += time()
t_negl = -time()
n = 6
if unique:
    np.random.seed()
    seed = 0
else:
    np.random.seed(2)
    seed = np.random.get_state()[1][0]
    
def rand():
    return np.random.randint(n)+1
def randp():
    return np.random.randint(n-1)+3

titles = '''How many baloons?
Needle in a haystack
Broken sticks and twigs
Fresh glass
Sparks'''.split('\n')
source = 'set1'
destination = '{}_{}.mp4'
def capture(file, max_frames=-1):
    cap = cv2.VideoCapture(source+'/'+file)
    while cap.isOpened():
        if unique:
            cap.read()
        ret, frame = cap.read()
        if not ret:
            break
        yield frame

t_negl += time()
t_load = -time()
source_names = check_output(['ls','set1']).decode().strip('\n').split('\n')
shots = [list(capture(file)) for file in source_names]
weights = np.array([float(name.split('|')[0].strip()) for name in source_names])
weights /= np.sum(weights)
shot_length = min(map(len, shots))
for i in range(len(shots)):
    shots[i] = shots[i][:shot_length]
shots = np.array(shots)
t_load += time()
t_negl -= time()

t_round = 0
def _round(frames, axes=[0], margin=10):
    global t_round
    t_round -= time()
    for axis in axes:
        frames[(slice(None),)*axis+(0,...)] = 0
        frames[(slice(None),)*axis+(-1,...)] = 0
        for i in range(1, margin):
            frames[(slice(None),)*axis+(i,...)] //= margin//i
            frames[(slice(None),)*axis+(-i-1,...)] //= margin//i
    t_round += time()
def rounded(frames, axes=[1,2], margin=5):
    global t_round
    t_round -= time()
    frames = frames.copy()
    t_round += time()
    _round(frames, axes, margin)
    return frames


#conviniance shape names
scene_shape = list(shots.shape[1:])
scene_shape[1] *= 2
scene_shape[2] *= 2

file = destination.format(seed, round(time()-1614567930))
writer = cv2.VideoWriter(file,
                        cv2.VideoWriter_fourcc(*"MP4V"),
                        29.387754/(2 if unique else 1),
                        (scene_shape[2], scene_shape[1]))

t_write = 0
def write(frames):
    global t_write    
    t_write -= time()
    for frame in frames:
        writer.write(frame)
        #out.append(frame)
    t_write += time()
t_negl += time()
t_create = -time()
t_n = 0
name = ''
for act in range(randp()):
    if act:
        write(np.zeros(scene_shape, shots.dtype)[::2])
        name += " "
    for scene in range(rand()):
        if scene:
            name += ' '
        selection_idxs = [np.random.choice(range(len(weights)), p=weights) for i in range(rand())]
        name += ''.join(map(str, selection_idxs))
        selections = np.array([shots[idx] for idx in selection_idxs])
        out = np.zeros(scene_shape, selections.dtype)
        h,w = shots[0].shape[1:3]
        if len(selections) <= 3:
            for a in range(2):
                for b in range(2):
                    if len(selections) == 1:
                        out[:,a::2,b::2] = rounded(selections[0])
                    elif len(selections) == 2:
                        out[:,a::2,b:w:2] = rounded(selections[0,:,:,w//4:-w//4])
                        out[:,a::2,b+w::2] = rounded(selections[1,:,:,w//4:-w//4])
                    elif len(selections) == 3:
                        out[:,a::2,b:w*2//3:2] = rounded(selections[0,:,:,w//3:-w//3])
                        out[:,a::2,b+w*2//3:w*4//3:2] = rounded(selections[1,:,:,w//3:-w//3])
                        out[:,a::2,b+w*4//3::2] = rounded(selections[2,:,:,w//3:-w//3])
                    else:
                        assert False
        elif len(selections) == 4:
            out[:,:h,:w] = rounded(selections[0])
            out[:,:h,w:] = rounded(selections[1])
            out[:,h:,:w] = rounded(selections[2])
            out[:,h:,w:] = rounded(selections[3])
        elif len(selections) == 6:
            out[:,:h,:w*2//3] = rounded(selections[0,:,:,w//6:-w//6])
            out[:,:h,w*2//3:w*4//3] = rounded(selections[1,:,:,w//6:-w//6])
            out[:,:h,w*4//3:] = rounded(selections[2,:,:,w//6:-w//6])
            out[:,h:,:w*2//3] = rounded(selections[3,:,:,w//6:-w//6])
            out[:,h:,w*2//3:w*4//3] = rounded(selections[4,:,:,w//6:-w//6])
            out[:,h:,w*4//3:] = rounded(selections[5,:,:,w//6:-w//6])
        elif len(selections) == 5:
            out[:,:h,:w] = rounded(selections[0])
            out[:,:h,w:] = rounded(selections[1])
            out[:,h:,:w] = rounded(selections[2])
            out[:,h:,w:] = rounded(selections[3])
            out[:,h//2:-h//2,w//2:-w//2] = rounded(selections[4])
        else:
            assert False
        t_n += 1
        _round(out)
        write(out)
    name += '.'
t_create += time()-t_write-t_round
t_negl -= time()
writer.release()
t_negl += time()
if not unique:
    print(name)
else:
    input("Loaded. Press enter to display.")
    reader = cv2.VideoCapture(file)
    title = np.random.choice(titles)
    writer = Writer(title, 29.387754/2)
    while reader.isOpened():
        ret, frame = reader.read()
        if not ret or writer.write(frame) != -1:
            break
    cv2.destroyWindow(title)
    if unique:
        os.remove(file)
        for g in list(globals()):
            globals().pop(g)
    print("Permanently Erased")
