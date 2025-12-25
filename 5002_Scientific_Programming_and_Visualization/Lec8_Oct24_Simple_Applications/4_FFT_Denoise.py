# -*- coding: utf-8 -*-
"""
Created on Sun May  2 17:50:14 2021

@author: cmt
"""
import numpy as np
import matplotlib.pyplot as plt

allcolor= plt.cm.Blues(np.linspace(0,1,8))

def func1(x):
    return np.sin(x)+np.sin(10*x)+np.sin(5*x)
    # if x>-np.pi/2 and x<np.pi/2:
    #     # return np.exp(x)
    #     # return x+np.random.rand()*np.sin(5*np.pi*x)
    #     # return 1+np.random.rand()
    #     # return 1
    #     # return abs(x)
    #     return np.sin(x)+np.sin(10*x)
    # else:
    #     return 0

x=np.linspace(-np.pi,np.pi,1000)
FF0=np.zeros(len(x))
for ni in range(len(x)):
    FF0[ni]=func1(x[ni])

FF=FF0+(np.random.random(len(x))-0.5)*10

# FF=FF0

SS=np.zeros(len(x))+sum(FF)/len(x)

################################################
# do FFT by hand
plot_more=0
if plot_more==1:
    plt.figure();    nplot=0;
    ax1=plt.subplot(121);    ax2=plt.subplot(122); 
    ax1.plot(x,FF,'r-',label='orgin')

max_k=20
Ak=np.zeros(max_k); Bk=np.zeros(max_k)
for nk in range(1,max_k):
    Ak[nk]=sum(np.cos(nk*x)*FF)*(2/len(x))
    Bk[nk]=sum(np.sin(nk*x)*FF)*(2/len(x))
    if Ak[nk]**2+Bk[nk]**2>0.1:
        SS=SS+Ak[nk]*np.cos(nk*x)+Bk[nk]*np.sin(nk*x)
    if (nk-int(max_k/5)+5)%int(max_k/5)==0 and plot_more==1:
        ax1.plot(x,SS+(max(FF)-min(FF))*nplot,'-.',label=str(nk),color=allcolor[nplot])
        ax2.plot(x,abs(SS-FF),'-',label=str(nk),color=allcolor[nplot])
        nplot += 1    
if plot_more==1:
    ax1.plot(x,SS,'-',label=str(nk),color=allcolor[nplot])
    ax2.plot(x,abs(SS-FF),'-.',label=str(nk))    
    ax1.legend(); ax2.legend(); ax2.set_yscale('log')

plt.figure()

plt.plot(x,FF,'k.',label='with noise')
plt.plot(x,FF0,'r-',linewidth=2,label='no noise')
plt.plot(x,SS,'b.',label='denoise')
plt.legend()

plt.figure()
plt.subplot(131)
plt.plot(Ak,'r-*',label='Ak');
plt.plot(Bk,'b-o',label='Bk');
plt.legend()

ax32=plt.subplot(132); 
plt.title('Ak')

ax33=plt.subplot(133)
plt.title('Bk')
for nk in range(1,max_k):
    ax32.plot(x,np.sin(nk*x)*Ak[nk]+nk*0.5,'r-')
    ax33.plot(x,np.cos(nk*x)*Bk[nk]+nk*0.5,'b-')



##################################################
#Use FFT to do denoise
FFk=np.fft.fft(FF)
PSD=abs(FFk)**2//len(x)
FFk_filtered=FFk*(PSD>100)
FF_S=np.fft.ifft(FFk_filtered)

plt.figure()

plt.plot(x,FF,'k.',label='with noise')
plt.plot(x,FF0,'r-',linewidth=2,label='no noise')
plt.plot(x,np.real(FF_S),'b.',label='denoise_real')
plt.plot(x,np.imag(FF_S),'k.',label='denoise_imag')
plt.legend()


