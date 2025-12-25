#here, we plot the sphere using the polar coordiation
from mpl_toolkits import mplot3d

import numpy as np
import matplotlib.pyplot as plt

ax = plt.axes(projection='3d',proj_type='ortho')
ax.set_box_aspect([1,1,1])



Num_points=20
radius=10

xdata=[]
ydata=[]
zdata=[]
udata=[]
vdata=[]
wdata=[]


all_phi=np.linspace(0, np.pi, Num_points)
all_theta=np.linspace(-np.pi, np.pi, Num_points)

for phi in all_phi:
    for theta in all_theta:
        z=np.cos(phi)*radius
        x=np.sin(phi)*np.cos(theta)*radius
        y=np.sin(phi)*np.sin(theta)*radius
        xdata.append(x)
        ydata.append(y)
        zdata.append(z)
        udata.append(y)
        vdata.append(x)
        wdata.append(z*0)

ax.scatter3D(xdata, ydata, zdata,s=10, c='red');
ax.quiver3D(xdata, ydata, zdata, udata, vdata, wdata,
            length=2,arrow_length_ratio=0.3, 
            normalize=True, pivot='middle')
# pivot='tail','tip','middle'
ax.set_box_aspect([1,1,1])


ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()