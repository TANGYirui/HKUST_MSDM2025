import numpy as np
import matplotlib.pyplot as plt

epsilon=10E-10; Z=1; N=3
def func_px(x,y,z):
    r=np.sqrt(x**2+y**2+z**2)
    if r<epsilon:
        return 0
    rho=2*Z*r/N
    R2p=(1/2/np.sqrt(6))*rho*Z**3/2*np.exp(-rho/2)
    Y2px=np.sqrt(3)*x/r/np.sqrt(4*np.pi)
    return R2p*Y2px

x_min=-10; x_max=10; y_min=-10; y_max=10;z=0

def func(x,y):
    return x**2+np.sin(y)


num_x=100; num_y=100
px=np.zeros([num_x,num_y],float)
xx=np.zeros([num_x,num_y],float)
yy=np.zeros([num_x,num_y],float)
for nx in range(num_x):
    for ny in range(num_y):
        px[nx,ny]=func_px(nx/(num_x-1)*(x_max-x_min)+x_min,ny/(num_y-1)*(y_max-y_min)+y_min,z)
        
        # zz[nx,ny]=func((nx-20)/100,(ny-20)/10)     
        xx[nx,ny]=nx
        yy[nx,ny]=ny
        
plt.figure()
# # zz[2,5]=100
# plt.subplot(121)
# plt.imshow(px.transpose())
# plt.imshow(px)
plt.imshow(px,interpolation='bicubic')
# plt.axis('square') ### cannot use

# plt.subplot(122)
# # plt.imshow(px.transpose(),interpolation='bicubic')
# # plt.pcolormesh(xx,yy,px,shading='gouraud')
# # plt.pcolor(xx,yy,px,cmap='Greys')
# plt.axis('square')
