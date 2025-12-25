from mpl_toolkits import mplot3d

import numpy as np
import matplotlib.pyplot as plt

ax = plt.axes(projection='3d',proj_type='ortho')


Num_points=41
len_edge=10

center_cube=[0,0,0]

linear_points=np.linspace(0, 1, Num_points)

const1=linear_points*0+len_edge/2
const2=linear_points*0-len_edge/2
line=linear_points*len_edge-len_edge/2
height1=-len_edge/2
height2=len_edge/2

ax.scatter(center_cube[0],center_cube[1],center_cube[2],c='r',marker='*')

ax.plot(const1+center_cube[0], line+center_cube[1], height1+center_cube[2], zdir='z',c='b')
ax.plot(const2+center_cube[0], line+center_cube[1], height1+center_cube[2], zdir='z',c='b')
ax.plot(line+center_cube[0], const1+center_cube[1], height1+center_cube[2], zdir='z',c='b')
ax.plot(line+center_cube[0], const2+center_cube[1], height1+center_cube[2], zdir='z',c='b')

ax.plot(const1+center_cube[0], line+center_cube[1], height2+center_cube[2], zdir='z',c='b')
ax.plot(const2+center_cube[0], line+center_cube[1], height2+center_cube[2], zdir='z',c='b')
ax.plot(line+center_cube[0], const1+center_cube[1], height2+center_cube[2], zdir='z',c='b')
ax.plot(line+center_cube[0], const2+center_cube[1], height2+center_cube[2], zdir='z',c='b')

ax.plot(const1+center_cube[1], line+center_cube[2], height2+center_cube[0], zdir='x',c='b')
ax.plot(const2+center_cube[1], line+center_cube[2], height2+center_cube[0], zdir='x',c='b')
ax.plot(const1+center_cube[1], line+center_cube[2], height1+center_cube[0], zdir='x',c='b')
ax.plot(const2+center_cube[1], line+center_cube[2], height1+center_cube[0], zdir='x',c='b')


# #make the interval of different axis equal. Only work for some versions.
# #if it does not work, you can only tune it by hand
# #work for matplotlib2.1 and 3.0, but does not work for matplotlib3.1 
# plt.axis('square')

# # You can use the following setup to ensure the aspect 
# is correct
ax.set_box_aspect([1,1,1])

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

theta=45
alpha=50
ax.view_init(theta, alpha)
plt.draw()


