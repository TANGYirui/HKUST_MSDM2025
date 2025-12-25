#here, we plot the sphere using the spherical coordinates
from mpl_toolkits import mplot3d

import numpy as np
import matplotlib.pyplot as plt

ax = plt.axes(projection='3d',proj_type='ortho')


Num_points=41
radius=10

xdata=[]
ydata=[]
zdata=[]


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

ax.scatter3D(xdata, ydata, zdata,s=1, c='red');

plt.title('sample angles')

#ensure the aspect is correct
ax.set_box_aspect([1,1,1])


ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

phi=45
theta=50
ax.view_init(phi, theta)

plt.draw()



