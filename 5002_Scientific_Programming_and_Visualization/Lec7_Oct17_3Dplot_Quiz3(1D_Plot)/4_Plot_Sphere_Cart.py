#here, we plot the sphere using the Cartesian coordinates

from mpl_toolkits import mplot3d

import numpy as np
import matplotlib.pyplot as plt

plt.figure()

ax = plt.axes(projection='3d',proj_type='ortho')


Num_points=50
radius=20


xdata=[]
ydata=[]
zdata=[]
negative_zdata=[]

#u_points=np.linspace(-1, 1, 4)
u_points=np.linspace(-1, 1, Num_points)
#v_points=np.linspace(-1, 1, 5)
v_points=np.linspace(-1, 1, Num_points)
#u_points=np.random.rand(Num_points)*2-1
#v_points=np.random.rand(Num_points)*2-1

for x1 in u_points:
    for x2 in v_points:
        if x1**2+x2**2 <= 1:
            # # method 1, not homogeneous
            # x=x1*radius
            # y=x2*radius
            # z=np.sqrt(1-x1**2-x2**2)*radius
            
            # method 2, homogeneous
            # https://mathworld.wolfram.com/SpherePointPicking.html
            x=2*x1*np.sqrt(1-x1**2-x2**2)*radius
            y=2*x2*np.sqrt(1-x1**2-x2**2)*radius
            z=(1-2*(x1**2+x2**2))*radius
            
            xdata.append(x)
            ydata.append(y)
            zdata.append(z)
            negative_zdata.append(-z)

ax.scatter3D(xdata, ydata, zdata,s=4, c='red');
#ax.plot_trisurf(xdata,ydata,zdata,edgecolor='none');
ax.scatter3D(xdata, ydata, negative_zdata, s=1, c='red');

#ensure the aspect is correct
ax.set_box_aspect([1,1,1])

plt.title('sample xy plane')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

theta=45
alpha=50
ax.view_init(theta, alpha)
#ax.set_title('theta=30,alpha=60')
plt.draw()
# plt.savefig('sphere.pdf')




#
#ax.set_xlabel('x',fontsize=15)
#ax.set_ylabel('y',fontsize=15)
#ax.set_zlabel('z',fontsize=15)
#ax.xaxis.set_tick_params(labelsize=15)
#ax.yaxis.set_tick_params(labelsize=15)
#ax.zaxis.set_tick_params(labelsize=15)
#
#theta=30
#alpha=60
#ax.view_init(theta, alpha)
#ax.set_title('theta=30,alpha=60')
#plt.draw()
#
#ax.set_proj_type('ortho')
#plt.draw()
#
#plt.axis('square')
