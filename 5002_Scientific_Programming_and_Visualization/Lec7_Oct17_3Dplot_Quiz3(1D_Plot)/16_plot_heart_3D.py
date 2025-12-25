from mpl_toolkits import mplot3d

import numpy as np
import matplotlib.pyplot as plt

xx=[]
yy=[]
zz=[]
tt=[]
for q in np.linspace(-0.8,0.8,20):
#for q in np.random.random(10):
    for t in np.linspace(0,np.pi*2,50):
        z=1-q**2
        x=16*np.sin(t)**3
        y=13*np.cos(t)-5*np.cos(2*t)-2*np.cos(3*t)-np.cos(4*t)
        xx.append(x*z)
        yy.append(y*z)
        zz.append(q*5)
        tt.append(z)
    
plt.figure()
ax = plt.axes(projection='3d',proj_type='ortho')
# ax.plot_surface(xx,yy,zz)
# ax.plot_trisurf(yy,xx,zz)
ax.scatter3D(xx,yy,zz)
# plt.axis('square')
#plt.plot(zz,tt)