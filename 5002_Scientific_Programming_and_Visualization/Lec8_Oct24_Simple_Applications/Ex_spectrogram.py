#https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.spectrogram.html

from scipy import signal
from scipy.fft import fftshift
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
import numpy as np


tpi=2*np.pi

#Generate a test signal, a 2 Vrms sine wave whose frequency is slowly modulated around 3kHz,
#corrupted by white noise of exponentially decreasing magnitude sampled at 10 kHz.

fs = 10 #Sampling frequency of the x time series
N = 1000


time = np.arange(N) / float(fs)

amp = 2 * np.sqrt(2)
mod = 500*np.cos(tpi*time/4)
carrier = amp * np.sin(tpi*3e3*time + mod)

noise_power = 0.01 * fs / 2
noise = np.random.normal(scale=np.sqrt(noise_power), size=time.shape)
noise *= np.exp(-time/5)

x = carrier + noise

# carrier = amp * np.sin(tpi*time) + amp * np.sin(tpi*time*3)*10+  amp * np.sin(tpi*time*20)*5
# x = carrier

wav.write('x.wav', int(fs), x.astype(np.float32))

plt.figure()
plt.subplot(131)
plt.plot(carrier)

plt.subplot(132)
f, t, Sxx = signal.spectrogram(x, fs)
plt.pcolormesh(t, f, Sxx, shading='gouraud')
# plt.pcolormesh(t, fftshift(f), fftshift(Sxx, axes=0), shading='gouraud')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()

# f, t, Sxx = signal.spectrogram(x, fs, return_onesided=False)
# plt.pcolormesh(t, fftshift(f), fftshift(Sxx, axes=0), shading='gouraud')
# plt.ylabel('Frequency [Hz]')
# plt.xlabel('Time [sec]')
# plt.show()




data=x
rate=fs
ll=N

fft_range=1
num_fft=int(N/fs*4)
nl=int(ll/num_fft)
num_fft=len(range(0,ll-int(fft_range*nl),nl))+1
bgn=0
end=int(rate*fft_range)
freq=np.fft.fftfreq(data[bgn:end].shape[0])*rate
all_fft=np.zeros([freq.shape[0],num_fft])
all_t=np.zeros(num_fft)

ntp=0
for tp in range(0,ll-int(fft_range*rate),nl):
    bgn=tp
    end=int(rate*fft_range+tp)
    ff1=np.fft.fft(data[bgn:end])
    all_fft[:,ntp]=abs(ff1)
    all_t[ntp]=tp/fs
    ntp += 1

# plt.figure()
plt.subplot(133)
num_fh=int(freq.shape[0]/2)
# plt.pcolor(all_t, freq[0:int(freq.shape[0]/2):10], all_fft[0:int(freq.shape[0]/2):10,:])
plt.pcolor(all_t, freq[:num_fh], all_fft[:num_fh])
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()




