import wave
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

DEFAULT_FS = 44100
DEFAULT_WINDOW_SIZE = 4096
DEFAULT_OVERLAP_RATIO = 0.5
DEFAULT_FAN_VALUE = 15
DEFAULT_AMP_MIN = 10

"""
Function that converts a byte string into a numpy array
"""
def _wav2array(nchannels, sampwidth, data):
    num_samples, remainder = divmod(len(data), sampwidth * nchannels)
    if remainder > 0:
        raise ValueError('The length of data is not a multiple of '
                         'sampwidth * num_channels.')
    if sampwidth > 4:
        raise ValueError("sampwidth must not be greater than 4.")

    if sampwidth == 3:
        a = np.empty((num_samples, nchannels, 4), dtype=np.uint8)
        raw_bytes = np.fromstring(data, dtype=np.uint8)
        a[:, :, :sampwidth] = raw_bytes.reshape(-1, nchannels, sampwidth)
        a[:, :, sampwidth:] = (a[:, :, sampwidth - 1:sampwidth] >> 7) * 255
        result = a.view('<i4').reshape(a.shape[:-1])
    else:
        dt_char = 'u' if sampwidth == 1 else 'i'
        a = np.fromstring(data, dtype='<%s%d' % (dt_char, sampwidth))
        result = a.reshape(-1, nchannels)
    return result

"""
Function to convert stereo to mono
"""

def stereo2mono(audiodata):
	audiodata = audiodata.astype(float)
	d = audiodata.sum(axis=1) / 2
	return d

"""
Class containing details of the wav file that has been read.
Sample use:
	song_x = song("abc.wav")
"""
class song:
	def __init__(self, file):
		wav = wave.open(file)
		self.rate = wav.getframerate()
		self.nchannels = wav.getnchannels()
		self.sampwidth = wav.getsampwidth()
		self.nframes = wav.getnframes()
		self.data = wav.readframes(self.nframes)
		self.array = stereo2mono(_wav2array(self.nchannels, self.sampwidth, self.data))
		wav.close()

file = "./Songs_Wav/Ricky Martin - Livin La Vida Loca.wav"
song1 = song(file)
print(song1.array.shape)	
# #fft_array = mlab.specgram(song1.array,
#         NFFT=DEFAULT_WINDOW_SIZE,
#         Fs=DEFAULT_FS,
#         window=mlab.window_hanning,
#         noverlap=int(DEFAULT_WINDOW_SIZE * DEFAULT_OVERLAP_RATIO))
fft_array = np.fft.fft(song1.array)
print(fft_array.shape)
plt.scatter(fft_array[:0], fft_array[:1])
plt.show()