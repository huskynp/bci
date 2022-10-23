import os
import numpy as np
import mne

sample_data_folder = mne.datasets.sample.data_path()
sample_data_raw_file = os.path.join(sample_data_folder, 'MEG', 'sample',
                                    'sample_audvis_raw.fif')
raw = mne.io.read_raw_fif(sample_data_raw_file)
raw.crop(0, 60).load_data()  # just use a fraction of data for speed here
raw.info['bads'] = ['MEG 2443', 'EEG 053'] #bads    
picks = mne.pick_types(raw.info, meg='mag', eeg=False, eog=False, stim=False, exclude = 'bads')
ssp_projectors = raw.info['projs']
raw.del_proj()
mag_channels = mne.pick_types(raw.info, meg='mag')
raw.plot(duration=60, order=mag_channels, n_channels=len(mag_channels),
         remove_dc=False)

# mag_channels = mne.pick_types(raw.info, meg='mag')
# raw.plot(duration=60, order=mag_channels, n_channels=len(mag_channels),
#          remove_dc=False)


# raw.plot_psd(area_mode = 'range', tmax = 60, average=False)

spectrum0 = raw.compute_psd()
spectrum0.plot(average=False)
freqs=(60, 120, 180, 240)
raw.notch_filter(np.arange(60, 241, 60), picks=picks, filter_length='auto', phase='zero')
# raw.plot_psd(area_mode='range', picks=picks, average=False)
spectrum1 = raw.compute_psd()
spectrum1.plot(average=False)
# raw_notch = raw.copy().notch_filter(freqs=freqs)

raw.filter(1, 60., fir_design='firwin') #band pass under 1 - 60hz
#raw.plot_psd(area_mode='range', picks=picks, average=False)

spectrum = raw.compute_psd()
spectrum.plot(average=False)