from scipy import signal
from scipy.fft import rfft, rfftfreq, fft, fftfreq, irfft
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import numpy as np

fs = 256


i = 0
IP = "http://10.1.29.67"

app = Dash(__name__)

f = open('betterdataset.txt', 'r')
content = f.read()
lines = content.split('\n')
numbers = np.array([float(x) for x in lines])

e, f = signal.iirnotch(60, 30, fs=fs)  # bandstop
filtered_data = signal.filtfilt(e, f, numbers)

d, c = signal.butter(2, 0.1, 'highpass', analog=False, fs=fs)  # lowcut
filtered_data = signal.filtfilt(d, c, filtered_data)

g, h = signal.butter(2, 80, 'lowpass', fs=fs)  # highcut
filtered_data = signal.filtfilt(g, h, filtered_data)

#b, a = signal.butter(2, [60, 60], 'bandstop', analog=False, fs=fs)  # bandstop
#filtered_data = signal.filtfilt(b, a, filtered_data)

g, h = signal.butter(2, [1, 3], 'bandpass', analog=False, fs=fs)  # Delta Waves
delta_waves = signal.filtfilt(g, h, filtered_data)

i, j = signal.butter(2, [4, 7], 'bandpass', analog=False, fs=fs)  # Theta Waves
theta_waves = signal.filtfilt(i, j, filtered_data)

k, l = signal.butter(2, [8, 12], 'bandpass',
                     analog=False, fs=fs)  # Alpha Waves
alpha_waves = signal.filtfilt(k, l, filtered_data)

m, n = signal.butter(2, [8, 14], 'bandpass', analog=False, fs=fs)  # Mu Waves
mu_waves = signal.filtfilt(m, n, filtered_data)

o, p = signal.butter(2, [13, 25], 'bandpass',
                     analog=False, fs=fs)  # Beta Waves
beta_waves = signal.filtfilt(o, p, filtered_data)

q, r = signal.butter(2, [25, 75], 'bandpass',
                     analog=False, fs=fs)  # Gamma Waves
gamma_waves = signal.filtfilt(q, r, filtered_data)


df = pd.DataFrame({
    'Raw Data': numbers,
    'Filtered Data': filtered_data,
    'Delta Waves': delta_waves,
    'Theta Waves': theta_waves,
    'Alpha Waves': alpha_waves,
    'Mu Waves': mu_waves,
    'Beta Waves': beta_waves,
    'Gamma Waves': gamma_waves,
})
fig = px.line(df)


# rms = np.sqrt(np.mean(numbers**2)).tolist()
# print(rms)

# df = pd.DataFrame({
#     'Voltage': rms
# })

N = len(filtered_data)

yf = rfft(filtered_data)  # fft MAYconfimedBE??!?!?
xf = rfftfreq(N, 1/fs)


fft_df = pd.DataFrame(np.abs(yf), xf)
fft_fig = px.line(fft_df)


#power_spectral_density = signal.welch(x=filtered_data, fs=fs)

dp = pd.DataFrame(signal.welch(filtered_data))

psd_fig = px.line(dp)


if __name__ == "__main__":
    app.layout = html.Div(children=[
        html.Div(id="dummy1"),
        html.H1("Current Dataset: FP1 Alcholic Data"),
        dcc.Graph(id="graph", animate=True, figure=fig),
        html.H2("FFT"),
        dcc.Graph(id="fft", figure=fft_fig),
        html.H2("PSD"),
        dcc.Graph(id="psd", figure=psd_fig)
    ])

    app.run_server(debug=True)

    # column name
    # array
