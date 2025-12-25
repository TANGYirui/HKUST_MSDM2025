#here we use some particular transformation to 
#realize homogeneous sphere
#http://mathworld.wolfram.com/SpherePointPicking.html

from mpl_toolkits import mplot3d

import numpy as np
import matplotlib.pyplot as plt

ax = plt.axes(projection='3d',proj_type='ortho')


Num_points=101
radius=10

xdata=[]
ydata=[]
zdata=[]

u_points=np.random.rand(Num_points)
v_points=np.random.rand(Num_points)

all_phi = np.arccos(2*u_points - 1)
all_theta = 2*np.pi*v_points

for phi in all_phi:
    for theta in all_theta:
        z=np.cos(phi)*radius
        x=np.sin(phi)*np.cos(theta)*radius
        y=np.sin(phi)*np.sin(theta)*radius
        xdata.append(x)
        ydata.append(y)
        zdata.append(z)


# u_points=np.linspace(-1, 1, Num_points)
# v_points=np.linspace(0, 1, Num_points)

# for u in u_points:
#     for theta in v_points*2*np.pi:
#         z=u*radius
#         x=np.sqrt(1-u**2)*np.cos(theta)*radius
#         y=np.sqrt(1-u**2)*np.sin(theta)*radius
#         xdata.append(x)
#         ydata.append(y)
#         zdata.append(z)


ax.scatter3D(xdata, ydata, zdata, s=1, c='red');

plt.title('sample angles')

#ensure the aspect is correct
ax.set_box_aspect([1,1,1])

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

phi=0
theta=0
ax.view_init(phi, theta)
#ax.set_title('phi=30,theta=60')
plt.draw()


