import cv2 as cv, numpy as np

class Writer:
    def __init__(self, name='untitiled', frame_rate=30):
        self.name = name
        self.frame_rate = frame_rate
        self.writer = None
    def write(self, frame):
        if self.writer is None:
            self.writer = cv.VideoWriter(self.name+'.avi',
                                        cv.VideoWriter_fourcc(*"MJPG"),
                                        self.frame_rate,
                                        (frame.shape[1], frame.shape[0]))
        self.writer.write(frame.astype(np.uint8))

    def release(self):
        self.writer.release()

if __name__ == '__main__':
    w = Writer()
    for i in range(100):
       w.write(np.random.randint(0, 255, (480, 640, 3)))
    w.release()
