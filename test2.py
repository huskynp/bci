import os
import numpy as np
import mne

arr = np.loadtxt("good.txt")

NUM_CHANNELS, FS = 1, 256

info = mne.create_info(NUM_CHANNELS, FS, ch_types='eeg')  # num channels, fs
obj = mne.io.RawArray(np.array([arr]), info)

# graphing
fig = obj.compute_psd(tmax=np.inf, average='mean').plot()
obj.plot(duration=10, block=True)
