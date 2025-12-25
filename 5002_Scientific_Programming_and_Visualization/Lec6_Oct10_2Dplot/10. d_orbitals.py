import numpy as np
import matplotlib.pyplot as plt
def fun_dxy(x,y,z):    
    r2=x**2+y**2+z**2    
    a0=1
    Rr=4/81/np.sqrt(30)*r2/a0/a0*np.exp(-r2/3/a0)
    if r2==0:
        return 0
    return Rr*np.sqrt(15/4/np.pi)*x*y/r2

x_min=-3; x_max=3; z=0
y_min=-3; y_max=3

num_x=50; num_y=50
dxy=np.zeros([num_x,num_y],float); xx=np.zeros([num_x,num_y],float); yy=np.zeros([num_x,num_y],float)
for nx in range(num_x):
    for ny in range(num_x):
        xx[nx,ny]=nx/(num_x-1)*(x_max-x_min)+x_min
        yy[nx,ny]=ny/(num_y-1)*(y_max-y_min)+y_min
        dxy[nx,ny]=fun_dxy(nx/(num_x-1)*(x_max-x_min)+x_min,ny/(num_y-1)*(y_max-y_min)+y_min,z)
plt.figure()
plt.subplot(121)
plt.pcolor(xx,yy,dxy)
plt.axis('square')
# plt.imshow(xx,yy,dxy)
plt.subplot(122)
plt.contourf(xx,yy,dxy,20)
plt.axis('square')
#plt.axis([x_min, x_max, y_min, y_max])
