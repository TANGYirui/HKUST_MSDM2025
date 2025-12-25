#plot the sphere surface

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np


fig = plt.figure()
#compare the difference between the following two methods. 
#The second one may not give you correct results
# method 1
ax = fig.add_subplot(111, projection='3d',proj_type='ortho')

# ##method 2
# ax = fig.add_subplot(111, projection='3d')
# # ax = plt.axes(projection='3d')
# ax.set_proj_type('ortho')
# # ax.set_proj_type('persp')

#ensure the aspect is correct
ax.set_box_aspect([1,1,1])

num_points=100
# Make data
u = np.linspace(0, 2 * np.pi, num_points)
v = np.linspace(0, np.pi, num_points)

XX=np.zeros([num_points,num_points],float)
YY=np.zeros([num_points,num_points],float)
ZZ=np.zeros([num_points,num_points],float)

nnu=-1
for nu in u:
    nnu=nnu+1
    nnv=-1
    for nv in v:
        nnv=nnv+1
        XX[nnu,nnv]=np.sin(nv)*np.sin(nu)
        YY[nnu,nnv]=np.sin(nv)*np.cos(nu)
        ZZ[nnu,nnv]=np.cos(nv)

# Plot the surface
ax.plot_surface(XX, YY, ZZ, color='r',edgecolor='b',shade=False)

phi=30
theta=60
ax.view_init(phi, theta)

plt.draw()