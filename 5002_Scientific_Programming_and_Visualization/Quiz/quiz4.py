import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from matplotlib import cm


z = np.linspace(-10*np.pi, 0, 5000)
x = z * np.sin(z)
y = z * np.cos(z)

fig = plt.figure()
ax = plt.axes(projection='3d',proj_type='persp')
ax.scatter3D(x, y, z , s=2, c=-z, cmap='jet')
ax.plot(x,y,5,c='r')
ax.plot([0, 0], [0, 0], [-100, 0], c='blue')

ax.set_box_aspect(aspect=(0.5,1,1))
plt.title('spiral arrow',x=0.5, y=0.4,color="black",size=14)

phi=0
theta=90
ax.view_init(phi, theta)

ax.set_xlabel('X',fontsize=10,labelpad=8)
ax.set_ylabel('Y',fontsize=10,labelpad=8)
ax.set_zlabel('Z',fontsize=10,labelpad=8)

plt.axis("off")

plt.draw()
plt.show()

