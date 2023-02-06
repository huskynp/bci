import pandas as pd
import mne
import numpy as np

print("Opening file...")

TEST_FILENAME = "rawData.csv"
# ask for file
"""
import easygui
path = easygui.fileopenbox(filetypes=['.csv'], title="Open Data")

if path is None:
    print("Error: No file chosen")
    quit()
"""
csv = pd.read_csv(TEST_FILENAME)
#rawdata = [csv[' ch1'],csv[' ch2']]
rawdata = [csv[' ch1']/8 - csv[' ch2']/8]
info = mne.create_info(1,240, 'eeg')
data = mne.io.RawArray(rawdata, info)

notched = data.copy().notch_filter(freqs=[60], picks=mne.pick_types(data.info, eeg=True), method="spectrum_fit", filter_length="10s")
#data.plot(scalings='auto')
#notched.plot(scalings='auto')

#SOURCE: Makoto's preprocessing pipeline, sccn.ucsd.edu
import numpy as np
#spectrum.plot_topomap(ch_type='eeg', agg_fun=np.median)
#Step 1: Add a 60hz notch filter
notched.plot_psd(average=True)
#Step 2: High Pass at 0.2 Hz
highpassed = notched.copy().filter(h_freq=None, l_freq=0.2)
#Step 3: Low Pass 20hz
lowpassed = highpassed.copy().filter(l_freq=None, h_freq=20)
#Step 4: graph
end = lowpassed.copy()

end.plot(scalings="auto")
end.plot_psd()