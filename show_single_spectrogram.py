from tqdm import tqdm
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

axisFontSize  = 14
titleFontSize = 20
Trace_Path = '/Users/sungbin/Downloads/Real'

# parameter
samplingFrequency = int(5e9)      # unit: Hz
windowLength      = int(1e3)      # unit: point
trigger_threshold = 1.5
x_index = 5
y_index = 7
trace_index = 2

triggers = np.load(f'{Trace_Path}/cpu_trigger_{x_index}_{y_index}.npy')
traces = np.load(f'{Trace_Path}/cpu_trace_{x_index}_{y_index}.npy')
print("({}, {}, {})".format(x_index, y_index, trace_index))
trigger = triggers[trace_index]
trace = traces[trace_index]

# 전체 트레이스에 대해 Spectrogram 계산
f, t, Sxx = signal.spectrogram(trace, fs=samplingFrequency, window=signal.get_window(window='hamming', Nx=windowLength))

# Plot
plt.figure(figsize=(10, 10))

# 원 신호 시각화
plt.subplot(2, 1, 1)
plt.title('Original Signal (Full)', fontsize=titleFontSize)
plt.plot(np.linspace(0, trace.shape[0] / samplingFrequency, len(trace)), trace, linewidth=0.5)
plt.plot(np.linspace(0, trigger.shape[0] / samplingFrequency, len(trigger)), trigger / 3000, color='red')
plt.ylabel('Voltage (V)', fontsize=axisFontSize)

# Spectrogram
plt.subplot(2, 1, 2)
plt.title('Spectrogram', fontsize=titleFontSize)
plt.pcolormesh(t, f, Sxx)
plt.ylabel('Frequency [Hz]', fontsize=axisFontSize)

plt.tight_layout()
plt.show()