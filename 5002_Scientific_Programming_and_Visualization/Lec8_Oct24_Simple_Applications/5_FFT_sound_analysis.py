#https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.read.html
#https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.wavfile.write.html
#https://vimsky.com/zh-tw/examples/detail/python-method-scipy.io.wavfile.read.html

import scipy.io.wavfile as wav
import numpy as np
import matplotlib.pyplot as plt
# from scipy import signal
from matplotlib.colors import LogNorm
from matplotlib.animation import FuncAnimation
import os

tpi=2*np.pi

# rate,data=wav.read('The Sounds of Silence.wav')
rate,data=wav.read('test_float32.wav')
#Data is 1-D for 1-channel WAV, or 2-D of shape (Nsamples, Nchannels) otherwise

half_rate=int(rate/2)

plt.figure()
plt.plot(data[:,0],label='left channel')
plt.plot(data[:,1],label='right channel')

ll,tmp=data.shape
freq = np.fft.fftfreq(data.shape[0])*rate #frequency in Hz


max_t=ll/rate
t=np.linspace(0,ll-1,ll)/rate  ## the unit is second

# #random noise is very difficult to handle
# noise=np.random.random(ll)

noise=np.sin(tpi*t)**0
for ni in range(2,20,4):
    noise += np.sin(tpi*t/ni)**2*ni

wav.write('noise.wav', rate, noise.astype(np.float32))
# os.system('noise.wav')

freq_noise=10

## do the FFT for the noise
n_fft=np.fft.fft(noise)
plt.figure
plt.subplot(121); plt.title('noise')
plt.plot(noise)
plt.subplot(122); plt.title('FFT of noise')
plt.plot(freq[0:freq_noise],abs(n_fft[0:freq_noise])); 


data_w_noise=np.copy(data)
data_de_noise=np.copy(data_w_noise)*0

data_w_noise[:,0]+=noise

wav.write('test_with_noise.wav', rate, data_w_noise)

l_fft=np.fft.fft(data[:,0])

ln_fft=np.fft.fft(data_w_noise[:,0])
ln_fft_filtered=np.copy(ln_fft)
ln_fft_filtered[0:freq_noise]=0
ln_fft_filtered[-freq_noise:-1]=0

# rn_fft=np.fft.fft(data_w_noise[:,1])
# rn_fft_filtered=np.copy(rn_fft)
# rn_fft_filtered[0:200]=0
# rn_fft_filtered[-200:-1]=0

data_de_noise[:,0]=np.real(np.fft.ifft(ln_fft_filtered))
# data_de_noise[:,1]=np.fft.ifft(rn_fft_filtered)

wav.write('test_dn.wav', rate, data_de_noise)
wav.write('test_dn_halfrate.wav', half_rate, data_de_noise)

# ### get the FFT for different part

fft_range=2
num_fft=int(ll/rate)-fft_range
bgn=rate*1
end=rate*(1+fft_range)
freq=np.fft.fftfreq(data[bgn:end,0].shape[0])*rate
all_fft=np.zeros([freq.shape[0],num_fft])
all_t=np.zeros(num_fft)
for tp in range(num_fft):
    bgn=rate*tp
    end=rate*(tp+fft_range)
    ff1=np.fft.fft(data[bgn:end,0])
    all_fft[:,tp]=abs(ff1)
    all_t[tp]=tp


## plot the FFT with time
plt.figure()
plt.pcolor(all_t, freq[0:3000:10], all_fft[0:3000:10,:],norm=LogNorm(vmin=5))
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()

fig_example, ax = plt.subplots()
# xdata, ydata = [], []

#prepare something you want to update
ln, = plt.plot([], [], 'r.-')
text_step=plt.text(1000, 6000, 't',color='black',fontsize=20)

def init():
    ax.set_xlim(0, 3000);ax.set_ylim(0, np.max(all_fft)*1.1);
    return ln,text_step

#The function to update what you want to plot
def update(t):
    tp=t   
    ln.set_data(freq,abs(all_fft[:,tp]))
    text_step.set_text('t='+str(tp))
    return ln,text_step

ani = FuncAnimation(fig=fig_example, 
                    init_func=init, 
                    func=update, 
                    frames=num_fft,
                    interval=10,  #the larger, the slower
                    blit=False)
plt.show()

