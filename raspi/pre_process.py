import pandas as pd

print("Opening file...")

TEST_FILENAME = "1675044441-raw.csv"
# ask for file
"""
import easygui
path = easygui.fileopenbox(filetypes=['.csv'], title="Open Data")

if path is None:
    print("Error: No file chosen")
    quit()
"""
df = pd.read_csv(TEST_FILENAME)

df.set_index("time", inplace=True)

# PGA gain
df /= 8

print("File opened and read")

import matplotlib.pyplot as plt
f, a = plt.subplots(nrows = 4, ncols = 1)

df.plot(ax=a[0], use_index=True, y='ch1')
df.plot(ax=a[1], use_index=True, y='ch2')

#SOURCE: Makoto's preprocessing pipeline, sccn.ucsd.edu

samples = len(df['ch1'])
filt_df = df.copy()
fs = samples/(filt_df.index[-1])

print("SAMPLE RATE", fs)

from scipy import signal
import numpy as np

#Step 1: High-pass filter at 1Hz
hp = signal.butter(5, 1, 'highpass', output='sos', fs=fs)
ch1 = signal.sosfilt(hp, filt_df['ch1'])
ch2 = signal.sosfilt(hp, filt_df['ch2'])

#Step 2: Low-pass at 60hz
lp = signal.butter(5, 60, 'lowpass', output='sos', fs=fs)
ch1 = signal.sosfilt(lp, ch1)
ch2 = signal.sosfilt(lp, ch2)

#END
filt_df['ch1'] = ch1
filt_df['ch2'] = ch2

filt_df.plot(ax=a[2], use_index=True, y='ch1')
filt_df.plot(ax=a[3], use_index=True, y='ch2')

plt.show()


