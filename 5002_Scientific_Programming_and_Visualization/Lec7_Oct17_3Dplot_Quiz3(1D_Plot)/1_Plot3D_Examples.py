from mpl_toolkits import mplot3d

import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(10,10), dpi=100)
ax = plt.axes(projection='3d',proj_type='ortho')

Num_period=8
Num_points=100
Amp_Rand=0.1

# Data for a three-dimensional line
zline = np.linspace(0, np.pi*Num_period, Num_points)
xline = np.sin(zline)
yline = np.cos(zline)


# Data for three-dimensional scattered points
zdata = np.linspace(0, np.pi*Num_period, Num_points)
xdata = np.sin(zdata) + Amp_Rand * np.random.rand(Num_points)
ydata = np.cos(zdata) + Amp_Rand * np.random.rand(Num_points)

#Example 1, plot 3D lines and 3D points
ax.plot3D(xline, yline, zline, 'gray')
ax.scatter3D(xdata, ydata, zdata, c=zdata, s=20, cmap='Reds');

# #Example 2, change the size of dots
ax.scatter3D(xdata, ydata, zdata, c=zdata, s=zdata*10, cmap='Reds');

#Example 3, change the view points
phi=30
theta=40
ax.view_init(phi, theta)
ax.set_title('phi='+str(phi)+',theta='+str(theta))

#Example 4, change the projection type
ax.set_proj_type('ortho')
ax.set_title('ortho')
# ax.set_proj_type('persp')
# ax.set_title('persp')
plt.draw()

# # #Example 5, set up the parameters of axis
ax.set_xlabel('x',fontsize=25)
ax.set_ylabel('y',fontsize=25)
ax.set_zlabel('z',fontsize=25)
ax.set_xlabel('x',fontsize=15,labelpad=10)
ax.set_ylabel('y',fontsize=25,labelpad=15)
ax.set_zlabel('z',fontsize=45,labelpad=10)
ax.xaxis.set_tick_params(labelsize=20)
ax.yaxis.set_tick_params(labelsize=20)
ax.zaxis.set_tick_params(labelsize=20)



# # plt.savefig('3D.pdf')
# # plt.savefig('3D.png')
