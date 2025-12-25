#http://scipy-lectures.org/intro/scipy/auto_examples/solutions/plot_fft_image_denoise.html

import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np
from PIL import Image

def fft_R(R, plot_result=0):
    
    R_fft = np.fft.fft2(R)

    R_fft2 = R_fft.copy()
    
    # Set r and c to be the number of rows and columns of the array.
    r, c = R_fft2.shape
    
    ## set the mask
    
    # Define the fraction of coefficients (in each direction) we keep
    keep_fraction_r = 0.1
    keep_fraction_c = 0.1
    # Set to zero all rows with indices between r*keep_fraction and
    # r*(1-keep_fraction):
    if keep_fraction_r<0.5:
        R_fft2[int(r*keep_fraction_r):int(r*(1-keep_fraction_r)),:] = 0
    
    # Similarly with the columns:
    if keep_fraction_c<0.5:
        R_fft2[:, int(c*keep_fraction_c):int(c*(1-keep_fraction_c))] = 0
    
    
    # ###mask 2
    # Remove_fraction_r = 0
    # Remove_fraction_c = 0.4
    
    # R_fft2[0:int(r*Remove_fraction_r),:]=0
    # R_fft2[int(r*(1-Remove_fraction_r)):r,:]=0
    
    # R_fft2[:,0:int(c*Remove_fraction_c)]=0
    # R_fft2[:,int(c*(1-Remove_fraction_c)):c]=0
    
    
    R_new = np.fft.ifft2(R_fft2).real
    
    if plot_result:
        plt.figure()
        plt.subplot(221)
        plt.pcolor(abs(R_fft), norm=LogNorm(vmin=5));     plt.colorbar()
        plt.title('Original Spectrum')
        plt.subplot(222)
        plt.pcolor(abs(R_fft2), norm=LogNorm(vmin=5));     plt.colorbar()
        plt.title('Filtered Spectrum')
        
        
        plt.subplot(223)
        plt.pcolor(R); plt.colorbar()
        plt.title('Original image')
        plt.subplot(224)
        plt.pcolor(R_new); plt.colorbar()
        plt.title('Filtered image')
        
    return R_new

img_import=Image.open('moonlanding.png') #read a new image
img=np.asarray(img_import) # convert the image to be a matrix
new_img=fft_R(img)
plt.figure()
plt.subplot(121)
plt.imshow(img,plt.cm.gray)
plt.subplot(122)
plt.imshow(new_img,plt.cm.gray)



##############################################
#for the colorful image
img_import=Image.open('test.png') #read a new image
img=np.asarray(img_import) # convert the image to be a matrix

a,b,c=img.shape
noise=np.zeros([a,b,c])
bb=np.linspace(1,b,b)
for ni in range(a):
    noise[ni,:,0]=np.sin(ni)*np.sin(ni*bb)*np.random.random(b)
    noise[ni,:,1]=np.sin(ni)*np.sin(ni*5*bb)*np.random.random(b)
    noise[ni,:,2]=np.sin(ni)*np.sin(ni*10*bb)*np.random.random(b)
    
    # noise[ni,:,0]=np.sin(5*ni)*np.sin(ni*bb)
    # noise[ni,:,1]=np.sin(10*ni)*np.sin(ni*5*bb)
    # noise[ni,:,2]=np.sin(15*ni)*np.sin(ni*10*bb)
    
img_noise=img+noise*200
img_noise=abs(img_noise)
img_noise=img_noise/np.max(img_noise)


new_img=np.copy(img_noise)*0
new_img[:,:,0]=fft_R(img_noise[:,:,0])
new_img[:,:,1]=fft_R(img_noise[:,:,1])
new_img[:,:,2]=fft_R(img_noise[:,:,2])

new_img=(new_img-np.min(new_img))
new_img=new_img/np.max(new_img)

plt.figure()
plt.subplot(121)
plt.imshow(img_noise)
plt.subplot(122)
plt.imshow(new_img)


