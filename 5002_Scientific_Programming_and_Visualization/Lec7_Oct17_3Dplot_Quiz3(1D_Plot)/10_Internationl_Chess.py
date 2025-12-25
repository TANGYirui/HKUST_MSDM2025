import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits import mplot3d

num_x=8; num_y=8
pannel=np.zeros([num_x,num_y],int); 
xx=np.zeros([num_x,num_y],int); 
yy=np.zeros([num_x,num_y],int); 
colors=np.zeros([num_x,num_y],dtype=str); 
colortuple=('b','y')

for nx in range(num_x):
    for ny in range(num_y):
        xx[nx,ny]=nx
        yy[nx,ny]=ny
        pannel[nx,ny]=0
        colors[nx,ny]=colortuple[(nx + ny)%len(colortuple)]

ax=plt.axes(projection='3d')
ax.plot_surface(xx, yy, pannel, facecolors=colors, linewidth=0,shade=False)

phi=90
theta=-90
ax.view_init(phi, theta)
ax.set_proj_type('ortho')

plt.axis('off')
#ensure the aspect is correct
ax.set_box_aspect([1,1,1])

plt.draw()

