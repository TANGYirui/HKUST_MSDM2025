#here we can realize the homogeneous plot by using
#random sampling for x, y and z, and collecting these
#points with distance equal to th radius
from mpl_toolkits import mplot3d

import numpy as np
import matplotlib.pyplot as plt

ax = plt.axes(projection='3d',proj_type='ortho')


Num_points=200
radius=10

epslon=0.0005
xdata=[]
ydata=[]
zdata=[]
negative_zdata=[]


#x_value=np.random.rand(Num_points)*2-1
#y_value=np.random.rand(Num_points)*2-1
#z_value=np.random.rand(Num_points)*2-1

x_value=np.linspace(-1, 1, Num_points)
y_value=np.linspace(-1, 1, Num_points)
z_value=np.linspace(-1, 1, Num_points)

for x in x_value:
    for y in y_value:
        for z in z_value:
            if np.abs(x**2+y**2+z**2-1) < epslon:
                xdata.append(x*radius)
                ydata.append(y*radius)
                zdata.append(z*radius)
            
ax.scatter3D(xdata, ydata, zdata, s=1, c='red');

#ensure the aspect is correct
ax.set_box_aspect([1,1,1])

plt.title('homogeneous sphere')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

theta=45
alpha=50
ax.view_init(theta, alpha)
#ax.set_title('theta=30,alpha=60')
plt.draw()


