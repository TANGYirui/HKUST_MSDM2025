import numpy as np
import matplotlib.pyplot as plt

#import matplotlib as mpl
#mpl.rc('image', cmap='jet')

def fun_dxy(x,y,z):    
    r2=x**2+y**2+z**2    
    a0=1
    Rr=4/81/np.sqrt(30)*r2/a0/a0*np.exp(-r2/3/a0)
    if r2==0:
        return 0
    return Rr*np.sqrt(15/4/np.pi)*x*y/r2


x_min=-3; x_max=3;
y_min=-3; y_max=3

num_x=100
num_y=100
dxy=np.zeros([num_x,num_y],float)
xx=np.zeros([num_x,num_y],float)
yy=np.zeros([num_x,num_y],float)
z=0
for nx in range(num_x):
    for ny in range(num_x):
        xx[nx,ny]=nx/(num_x-1)*(x_max-x_min)+x_min
        yy[nx,ny]=ny/(num_y-1)*(y_max-y_min)+y_min
        dxy[nx,ny]=fun_dxy(nx/(num_x-1)*(x_max-x_min)+x_min,ny/(num_y-1)*(y_max-y_min)+y_min,z)


        
plt.figure()


plt.subplot(221)
plt.title('imshow(),cmap="Greys"')
plt.imshow(dxy,cmap=plt.cm.Greys)

plt.subplot(222)
plt.title('pcolor(),cmap="seismic"')
plt.pcolor(xx,yy,dxy,cmap=plt.cm.seismic)
plt.axis('square')
plt.axis([x_min, x_max, y_min, y_max])

plt.subplot(223)
plt.title('contour(),cmap="Set1"')
#plt.contour(xx,yy,dxy,cmap=plt.cm.seismic)
#plt.contour(xx,yy,dxy,cmap=plt.cm.jet)
plt.contour(xx,yy,dxy,cmap=plt.cm.Set1)
#plt.contour(xx,yy,dxy,cmap=plt.cm.Greys)
plt.axis('square')
plt.axis([x_min, x_max, y_min, y_max])

plt.subplot(224)
plt.title('contourf(),cmap="jet"')
#plt.contourf(xx,yy,dxy,cmap=plt.cm.seismic)
plt.contourf(xx,yy,dxy,cmap=plt.cm.jet)
#plt.contourf(xx,yy,dxy,cmap=plt.cm.Set1)
#plt.contourf(xx,yy,dxy,cmap=plt.cm.Greys)
#plt.contourf(xx,yy,dxy)
#plt.set_cmap('jet')


#cbar = plt.colorbar(ticks=[dxy.min(), 0, dxy.max()], orientation='vertical')
#cbar.ax.set_yticklabels(['Low', 'Medium', 'High'])

plt.axis('square')
plt.axis([x_min, x_max, y_min, y_max])


    