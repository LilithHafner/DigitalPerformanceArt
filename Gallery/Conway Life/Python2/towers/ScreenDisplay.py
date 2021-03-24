import cv2 as cv, numpy as np
from time import time
record = []
class Writer:
    def __init__(self, name='untitiled', frame_rate=30, buffer=10):
        self.name = name
        self.delay = 1/frame_rate
        self.next_tick = None
        self.buffer = buffer*self.delay
        self.lags = 0
    def write(self, frame):
        cv.imshow(self.name, frame.astype(np.uint8))
        t = time()
        if self.next_tick is None:
            self.next_tick = t
        self.next_tick += self.delay
        if self.next_tick < t-self.buffer:
            self.next_tick = t-self.buffer
            self.lags += 1
            if self.lags == 1:
                print("Warning: screen display '{}' expirenced lag."
                      .format(self.name))
        record.append(self.next_tick-t)
        return cv.waitKey(max(1, int((self.next_tick-t)*1000)))
    def release(self):
        cv.destroyWindow(self.name)
        
##if __name__ == '__main__':
##    w = Writer(frame_rate = 30, buffer = 3)
##    for i in range(640):
##        x = np.random.randint(0, 255, (480, 640, 3))
##        x[:,:i] = 0
##        from time import sleep
##        sleep(np.random.random()*(w.delay*1.9-.03*2))
##        if w.write(x) != -1:
##            break
##    w.release()
    
if __name__ == '__main__':
    w = Writer(frame_rate = 1)
    while w.write(np.random.randint(0, 255, (480, 640, 3))) == -1:
        pass
    w.release()
