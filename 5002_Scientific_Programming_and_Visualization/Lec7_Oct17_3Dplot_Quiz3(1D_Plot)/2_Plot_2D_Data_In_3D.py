from mpl_toolkits import mplot3d

import numpy as np
import matplotlib.pyplot as plt

# ax = plt.axes(projection='3d')

ax = plt.axes(projection='3d',proj_type='ortho')

Num_period=5
Num_points=300

# Data for a three-dimensional line
zline = np.linspace(0, np.pi*Num_period, Num_points)
xline = np.sin(zline)*Num_period
yline = np.cos(zline)*Num_period
ax.plot3D(xline, yline, zdir='z', label='circle in (x,y)')
ax.scatter3D(xline, yline, xline*0, label='circle in (x,y)')


ax.plot3D(zline, yline, zdir='x', label='y=cos(z) in (y,z)')
ax.plot3D(zline, xline, zdir='y', label='x=sin(z) in (x,z)')

ax.plot3D(zline, yline, xline, label='spiral line')

ax.legend()

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

phi=45
theta=50
ax.view_init(phi, theta)
#plt.axis('square')
#ax.set_title('phi=30,theta=60')
plt.draw()


