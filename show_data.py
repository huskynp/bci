

# read numbers from new_data.txt
import matplotlib.mlab as mlab
from mpl_toolkits.mplot3d import Axes3D
import scipy.signal as signal
from scipy.fft import fft, ifft, fftfreq, rfft, rfftfreq, fftshift
import numpy as np
import math
import matplotlib.pyplot as plt

SAMPLE_RATE = 6

f = open('good.txt', 'r')
content = f.read()
lines = content.split('\n')
numbers = [float(x) * (10**6/8) for x in lines]
x_values = [(1/SAMPLE_RATE)*i for i in range(len(numbers))]

avg = sum(numbers)/len(numbers)
vrms = (math.pi)/(2*(math.sqrt(2))) * avg

print("uvrms:", vrms)  # * 10**6)

sampleNum = len(numbers)

yf = rfft(numbers)
xf = rfftfreq(sampleNum, 1 / 60)
# xf = fftshift(xf)
# yf = fftshift(yf)


# First, design the Buterworth filter
N = 2   # Filter order
# Wn = [59, 61]  # Cutoff frequency
B, A = signal.butter(N, 1/(SAMPLE_RATE/2), btype="highpass",
                     output='ba')
smooth_data = signal.lfilter(B, A, numbers, 0)

# filter test
yf[0] = 0

# plot the numbers on a line graph
fig, axs = plt.subplots(3)
fig.suptitle("Brainwaves, FFT")


axs[0].plot(x_values, numbers)
axs[0].set_xlabel("Time (s)")
axs[0].set_ylabel("Voltage (uV)")
axs[0].axhline(y=vrms, color='g', linestyle='-')

# notch filter @ 60
filtered_plot = axs[2]
b, a = signal.iirnotch(60.0, 30, fs=100)
filtered_data = signal.filtfilt(b, a, numbers)
filtered_plot.plot(x_values, filtered_data)


# fourier transform
fft = axs[1]
fft.plot(xf, np.abs(yf)*(2/len(numbers)), 'b')
# axs[1].plot(smooth_data, 'g')
# print(xf)
fft.set_xlabel("Frequency (Hz)")
fft.set_ylabel("Voltage")


plt.show()
