from scipy import misc
import matplotlib.pyplot as plt
from numpy import linalg
import numpy as np



img = misc.face()

plt.figure()
plt.imshow(img)


##check the detailed information of the image
print(type(img))
print(img.shape)
print(img.ndim)
print(img.dtype)
print(img.max(),img.min())

# ##plot different parts of the image
# plt.imshow(img)
# plt.matshow(img)
# plt.matshow(img[:,:,0])
# plt.matshow(img[:,:,1])
# plt.imshow(img[:,:,2]/255,cmap='seismic')
# plt.imshow(img[:,:,0:3]/255,cmap='BrBG')
# plt.contour(img[:,:,:],2)


img_array = img/255
# print(img_array.max(),img_array.min())

# according to colorimetry, it is possible to obtain a 
# fairly reasonable grayscale version of our color image 
# if we apply the formula Y=0.2126R+0.7152G+0.0722B

# @ operator, the matrix multiplication
img_gray = img_array @ [0.2126, 0.7152, 0.0722]
# img_gray = img_array @ [1, 0, 0]

U, s, Vt = linalg.svd(img_gray)
print(U.shape, s.shape, Vt.shape)

# to check the singular value decomposition
Sigma = np.zeros((768, 1024))
for i in range(len(s)):
    Sigma[i,i] = s[i]
ttt = U @ Sigma @ Vt - img_gray
# computes the norm of a vector or matrix represented in a NumPy array
print(linalg.norm(ttt))

# # plot the singular value


### numpy.allclose function to make sure the reconstructed product is 
### close to our original matrix (the difference between two arrays is small):
# print(np.allclose(img_gray, U @ Sigma @ Vt))

# we can only use the frist k singular value to reproduce the image
k=5
new_img=U @ Sigma[:,0:k] @ Vt[0:k,:]
# #whether the following one is the same as the one above
# new_img2=U[:,0:k] @ Sigma[0:k,0:k] @ Vt[0:k,:]

plt.figure()
plt.subplot(131)
plt.imshow(img_gray, cmap="gray")
plt.title('orginal_image')
plt.subplot(132)
plt.plot(s,'.')
plt.title('Singular values')
plt.subplot(133)
plt.title('image_with_K='+str(k))
plt.imshow(new_img, cmap="gray")


#######################################################
# we can do the trick for all different colors
U0, s0, Vt0 = linalg.svd(img_array[:,:,0])
U1, s1, Vt1 = linalg.svd(img_array[:,:,1])
U2, s2, Vt2 = linalg.svd(img_array[:,:,2])

Sigma0 = np.zeros((768, 1024))
Sigma1 = np.zeros((768, 1024))
Sigma2 = np.zeros((768, 1024))
for i in range(len(s)):
    Sigma0[i,i]=s0[i]
    Sigma1[i,i]=s1[i]
    Sigma2[i,i]=s2[i]
    
new_img_array=img_array*0
new_img_array[:,:,0]=U0 @ Sigma0[:,0:k] @ Vt0[0:k,:]
new_img_array[:,:,1]=U1 @ Sigma1[:,0:k] @ Vt1[0:k,:]
new_img_array[:,:,2]=U2 @ Sigma2[:,0:k] @ Vt2[0:k,:]

plt.figure()
plt.subplot(131)
plt.imshow(img_array, cmap='BrBG')
plt.title('orginal_image')
plt.subplot(132)
plt.plot(s0,'.r-')
plt.plot(s1,'.k-')
plt.plot(s2,'.b-')
plt.title('Singular values')
plt.subplot(133)
plt.title('image_with_K='+str(k))
plt.imshow(new_img_array,cmap='BrBG')

#######################################################
###we can also directly use the broadcast in Python to do it
##
###If our array has more than two dimensions, then the SVD can be applied to 
###all axes at once. However, the linear algebra functions in NumPy expect to 
###see an array of the form (N, :, :), where the first axis represents 
###the number of matrices
##
##img_array_transposed = np.transpose(img_array, (2, 0, 1))
##
##Ua, sa, Vta = linalg.svd(img_array_transposed)
##
##
##Sigmaa = np.zeros((3, 768, 1024))
##for j in range(3):
##    np.fill_diagonal(Sigmaa[j,:,:], sa[j,:])
##    
##reconstructed = Ua @ Sigmaa @ Vta
##
# for k in (10,20,30,40,100):
#     approx_img = Ua @ Sigmaa[:,:,0:k] @ Vta[:, 0:k, :]
    
#     new_img2=np.transpose(approx_img, (1, 2, 0))
#     new_img2=new_img2-new_img2.min()
#     new_img2=new_img2/new_img2.max()
    
#     plt.figure()
#     plt.imshow(new_img2)
#     plt.imsave('k'+str(k)+'.pdf', new_img2)


