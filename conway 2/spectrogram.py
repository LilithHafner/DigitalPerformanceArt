#https://www.kaggle.com/jamesrequa/convert-wav-to-spectogram
from scipy import signal
from scipy.io import wavfile
import matplotlib.pyplot as plt
from ScreenDisplay import Writer

sample_rate, samples = wavfile.read('Mishma with intro2.wav')
frequencies, times, spectrogram = signal.spectrogram(samples, sample_rate, nperseg=2048)

w = Writer()
w.write(spectrogram[:,:])

##raise ValueError()
##
##fig = plt.figure(figsize = (10,10))
##ax1 = fig.add_subplot(111)
##ax1.set_xticks([])
##ax1.set_yticks([])
##
##ax1.set_title('Spectrogram - House')
##ax1.imshow(spectrogram)
