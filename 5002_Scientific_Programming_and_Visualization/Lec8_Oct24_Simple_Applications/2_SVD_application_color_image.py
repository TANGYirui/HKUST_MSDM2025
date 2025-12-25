from scipy import misc
import matplotlib.pyplot as plt
from numpy import linalg
import numpy as np

plt.figure()
img = misc.face()
img_array=img/img.max()
la,lb,lc=img.shape

noise=np.random.rand(la,lb,lc)
img_noise=img_array+noise*0
img_noise=img_noise/img_noise.max()

plt.subplot(2,3,1)
plt.imshow(img_noise)

#If our array has more than two dimensions, then the SVD can be applied to 
#all axes at once. However, the linear algebra functions in NumPy expect to 
#see an array of the form (N, :, :), where the first axis represents 
#the number of matrices
#img_array_transposed = np.transpose(img_array, (2, 0, 1))

img_array_transposed = np.transpose(img_noise, (2, 0, 1))
Ua, sa, Vta = linalg.svd(img_array_transposed)

Sigmaa = np.zeros((3, 768, 1024))
for j in range(3):
    np.fill_diagonal(Sigmaa[j,:,:], sa[j,:])

nplot=0
for k in (10,20,50,100,200):
    approx_img = Ua @ Sigmaa[:,:,0:k] @ Vta[:, 0:k, :]
    
    new_img2=np.transpose(approx_img, (1, 2, 0))
    new_img2=new_img2-new_img2.min()
    new_img2=new_img2/new_img2.max()
    nplot=nplot+1
    plt.subplot(2,3,nplot+1)
    plt.imshow(new_img2)
    plt.title('K='+str(k))
    plt.imsave('k'+str(k)+'.png', new_img2)
    
    
    